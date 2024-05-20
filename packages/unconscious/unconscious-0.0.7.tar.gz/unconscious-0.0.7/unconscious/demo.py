import asyncio
import threading
import time
from py_unconscious import rust_sleep, rust_server


class Client:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_server)
        self.thread.start()

    def run_server(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.main())

    async def main(self):
        await rust_server()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()


# Instantiate the client
client = Client()

# Run the server in the background
time.sleep(1000)

# Stop the server and exit the script
client.stop()
