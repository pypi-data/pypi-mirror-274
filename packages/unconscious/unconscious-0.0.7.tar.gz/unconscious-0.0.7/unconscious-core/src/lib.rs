use axum::extract::ConnectInfo;
use axum::response::sse::{Event, Sse};
use axum::response::IntoResponse;
use axum::response::Response;
use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::Html,
    routing::{get, post},
    Json, Router,
};
use bb8::{Pool, PooledConnection};
use bb8_redis::bb8;
use bb8_redis::RedisConnectionManager;
use futures::stream::Stream;
use redis::AsyncCommands;
use serde_derive::{Deserialize, Serialize};
use serde_json::Value;
use std::{convert::Infallible, net::SocketAddr, time::Duration};
use tokio_stream::StreamExt as _;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

pub const DEFAULT_THREAD: &str = "k1";
// static import of the html file
const INDEX_HTML: &str = include_str!("../static/index.html");

pub async fn inner_main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "unconscious_core=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    tracing::debug!("connecting to redis");
    let manager = RedisConnectionManager::new("redis://localhost").unwrap();
    let pool = bb8::Pool::builder().build(manager).await.unwrap();

    {
        // ping the database before starting
        let mut conn = pool.get().await.unwrap();
        conn.set::<&str, &str, ()>("foo", "bar").await.unwrap();
        let result: String = conn.get("foo").await.unwrap();
        assert_eq!(result, "bar");
        conn.del::<&str, ()>("foo").await.unwrap();

        // also create a stream
        conn.xgroup_create::<&str, &str, &str, ()>(DEFAULT_THREAD, "group-1", "0")
            .await
            .unwrap_or(());
    }
    tracing::debug!("successfully connected to redis and pinged it");

    // build our application with some routes
    let app = Router::new()
        .route("/", get(index_page))
        .route("/sse", get(sse_handler))
        .route("/get", get(get_messages))
        .route("/add", post(add_message_with_body))
        .route("/threads", get(get_threads))
        .route("/subscriptions", get(subscriptions_sse))
        .route("/flush", get(flush_messages))
        .with_state(pool)
        .into_make_service_with_connect_info::<SocketAddr>();

    let port = std::env::var("PORT").unwrap_or_else(|_| "3000".to_string());
    let host = std::env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let listener = tokio::net::TcpListener::bind(format!("{}:{}", host, port))
        .await
        .unwrap();
    tracing::debug!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

pub async fn index_page() -> Html<String> {
    Html(INDEX_HTML.to_string())
}

type ConnectionPool = Pool<RedisConnectionManager>;

#[derive(Deserialize, Debug)]
struct Params {
    #[serde(default)]
    start: Option<String>,
    #[serde(default)]
    end: Option<String>,
    #[serde(default)]
    thread: Option<String>,
    #[serde(default)]
    identifier: Option<String>,
}

#[derive(Serialize, Deserialize)]
struct Message {
    message: String,
    client_id: String,
}

// handle get requests and filter by the supplied start and end times
async fn get_messages(
    params: Query<Params>,
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<Message>>, (StatusCode, String)> {
    let key = params.thread.as_deref().unwrap_or(DEFAULT_THREAD);
    let mut conn = pool.get().await.map_err(internal_error)?;
    let start = params.start.as_deref().unwrap_or("-");
    let end = params.end.as_deref().unwrap_or("+");
    let results: redis::RedisResult<redis::streams::StreamRangeReply> =
        conn.xrange(key, start, end).await;
    match results {
        Ok(reply) => {
            let typed_messages: Vec<Message> = reply
                .ids
                .into_iter()
                .map(|value| Message {
                    message: value.get("message").unwrap_or_default(),
                    client_id: value.get("client_id").unwrap_or_default(),
                })
                .collect();
            Ok(Json(typed_messages))
        }
        Err(err) => {
            println!("Error: {:?}", err);
            Err(internal_error(err))
        }
    }
}

async fn get_threads(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<String>>, (StatusCode, String)> {
    let mut conn = pool.get().await.map_err(internal_error)?;
    let keys: Vec<String> = conn.keys("*").await.map_err(internal_error)?;
    // filter out the subscriptions key
    let keys: Vec<String> = keys
        .into_iter()
        .filter(|key| !key.ends_with("_subscriptions"))
        .collect();
    Ok(Json(keys))
}

// Handle long-lived connections and check and send new messages every second
async fn sse_handler(
    params: Query<Params>,
    State(pool): State<ConnectionPool>,
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let key = params
        .thread
        .clone()
        .unwrap_or_else(|| DEFAULT_THREAD.to_string());
    let start = params.start.clone().unwrap_or_else(|| "-".to_string());
    let pool_clone = pool.clone();
    let async_stream = async_stream::stream! {
        let mut conn: PooledConnection<RedisConnectionManager> = pool_clone.get().await.unwrap();

        // Ensure stream exists
        conn.xgroup_create_mkstream::<&str, &str, &str, ()>(&key, "group-1", "0")
            .await
            .unwrap_or(());

        let subscription_key = format!("{}_subscriptions", key);
        let client_id = params.identifier.clone().unwrap_or_else(|| addr.to_string());

        // Add client to the subscription set
        conn.sadd::<&str, &str, ()>(&subscription_key, &client_id).await.unwrap();

        // Clean up subscription on disconnect
        let _guard = scopeguard::guard((), |_| {
            let pool = pool.clone();
            let subscription_key = subscription_key.clone();
            let client_id = client_id.clone();
            tokio::spawn(async move {
                let mut conn = pool.get().await.unwrap();
                conn.srem::<&str, &str, ()>(&subscription_key, &client_id).await.unwrap();
            });
        });

        let mut last_id = start;
        loop {
            let results: redis::RedisResult<redis::streams::StreamRangeReply> =
                conn.xrange(&key, last_id.as_str(), "+").await;
            match results {
                Ok(reply) => {
                    for value in reply.ids.into_iter() {
                        if value.id == last_id {
                            continue;
                        }
                        last_id.clone_from(&value.id);
                        let raw_message: String = value.get("message").unwrap_or_default();
                        // parse into json object
                        let value2: Value = serde_json::from_str(&raw_message).unwrap_or_default();
                        let data = Message {
                            message: value2.to_string(),
                            client_id: value.get("client_id").unwrap_or_default(),
                        };
                        yield Event::default().data(serde_json::to_string(&data).unwrap_or_default());
                    }
                }
                Err(_err) => {
                   // TODO: handle error
                }
            }

            tokio::time::sleep(Duration::from_secs(1)).await;
        }
    };
    let stream = async_stream.map(Ok);
    Sse::new(stream).keep_alive(
        axum::response::sse::KeepAlive::new()
            .interval(Duration::from_secs(1))
            .text("keep-alive-text"),
    )
}

async fn subscriptions_sse(
    params: Query<Params>,
    State(pool): State<ConnectionPool>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let key = params
        .thread
        .clone()
        .unwrap_or_else(|| DEFAULT_THREAD.to_string());
    let subscription_key = format!("{}_subscriptions", key);
    let pool_clone = pool.clone();

    let async_stream = async_stream::stream! {
        let mut conn: PooledConnection<RedisConnectionManager> = pool_clone.get().await.unwrap();
        tokio::time::sleep(Duration::from_millis(200)).await;
        loop {
            let subscribers: Vec<String> = conn
                .smembers(&subscription_key)
                .await
                .unwrap_or_default();
            let data = serde_json::to_string(&subscribers).unwrap_or_default();
            yield Event::default().data(data);
            tokio::time::sleep(Duration::from_secs(5)).await;
        }
    };

    let stream = async_stream.map(Ok);
    Sse::new(stream).keep_alive(
        axum::response::sse::KeepAlive::new()
            .interval(Duration::from_secs(1))
            .text("keep-alive-text"),
    )
}

#[derive(Debug, Deserialize, Serialize)]
struct BaseMessage {
    room: String,
    message: String,
    score: i32,
}

#[derive(Debug, Deserialize, Serialize)]
#[serde(untagged)]
enum MyEnum {
    String(String),
    Value(Value),
}

// add_message_with_body
async fn add_message_with_body(
    params: Query<Params>,
    State(pool): State<ConnectionPool>,
    ConnectInfo(addr): ConnectInfo<SocketAddr>,
    Json(body): Json<MyEnum>,
) -> Result<Response, (StatusCode, String)> {
    let key = params
        .thread
        .clone()
        .unwrap_or_else(|| DEFAULT_THREAD.to_string());

    let body = match body {
        MyEnum::String(s) => MyEnum::Value(serde_json::json!({
            "simple_message": {
                "room": "default",
                "message": s,
                "score": 0
            }
        })),
        _ => body,
    };

    let mut conn = pool.get().await.map_err(internal_error)?;
    let json_response = serde_json::to_string(&body).map_err(internal_error)?;

    let mut client_id = params
        .identifier
        .clone()
        .unwrap_or_else(|| addr.to_string());

    // replace any : with _
    client_id = client_id.replace(':', "_");

    // Ensure stream exists
    conn.xgroup_create_mkstream::<&str, &str, &str, ()>(&key, "group-1", "0")
        .await
        .unwrap_or(());

    conn.xadd(
        &key,
        "*",
        &[
            ("message", json_response.as_str()),
            ("client_id", client_id.as_str()),
        ],
    )
    .await
    .map_err(internal_error)?;

    Ok((StatusCode::OK, Json(body)).into_response())
}

async fn flush_messages(
    params: Query<Params>,
    State(pool): State<ConnectionPool>,
) -> Result<Response, (StatusCode, String)> {
    let key = params
        .thread
        .clone()
        .unwrap_or_else(|| DEFAULT_THREAD.to_string());
    let mut conn = pool.get().await.map_err(internal_error)?;
    conn.del(&key).await.map_err(internal_error)?;
    Ok((StatusCode::OK, "Messages flushed".to_string()).into_response())
}

/// Utility function for mapping any error into a `500 Internal Server Error`
/// response.
fn internal_error<E>(err: E) -> (StatusCode, String)
where
    E: std::error::Error,
{
    println!("Error: {:?}", err);
    (StatusCode::INTERNAL_SERVER_ERROR, err.to_string())
}
