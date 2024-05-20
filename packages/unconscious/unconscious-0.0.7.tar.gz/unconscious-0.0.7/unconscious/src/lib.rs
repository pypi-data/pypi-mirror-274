use pyo3::prelude::*;
use unconscious_core::inner_main;

#[pyfunction]
fn rust_server(py: Python<'_>) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async {
        inner_main().await;
        Ok("Done".to_string())
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn _unconscious(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_server, m)?)?;
    Ok(())
}
