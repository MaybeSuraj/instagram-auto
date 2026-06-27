from pyrogram import idle
from logger import LOGGER
from app import bot, botname, loop, initiate_tg_bot, initiate_ig_client
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Only respond if the request path is exactly "/"
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello World\n")
        else:
            # Send a 404 error for any other URL path
            self.send_error(404, "Page Not Found")

    def log_message(self, format, *args):
        pass  # disables default HTTP request logging


def run():
    server_address = ("0.0.0.0", 10000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server running on port 10000...")
    httpd.serve_forever()


async def main():
    """Single async entry-point that starts both clients on the uvloop loop."""
    LOGGER(__name__).info("Starting Bot")
    await initiate_tg_bot()
    await initiate_ig_client()
    await idle()
    await bot.stop()
    LOGGER(__name__).info(f"{botname} IS STOPPED")


if __name__ == "__main__":
    # Start the HTTP server in a separate thread
    server_thread = Thread(target=run)
    server_thread.daemon = True  # This makes sure the thread will exit when the main
    # program exits
    server_thread.start()
    loop.run_until_complete(main())
    LOGGER(__name__).info(f"{botname} IS STOPPED")
