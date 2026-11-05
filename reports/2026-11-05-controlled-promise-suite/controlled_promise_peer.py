"""HTTP answer fixture with explicit request-arrival and release barriers."""
import http.server
import threading
import time


class ControlledPromisePeer:
    def __init__(self):
        self.arrived = threading.Event()
        self.release = threading.Event()
        self.sent = threading.Event()
        self.requests = []
        self.errors = []
        self.started = time.monotonic()
        fixture = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                fixture.requests.append(dict(path=self.path, arrived_ms=fixture.elapsed()))
                fixture.arrived.set()
                if not fixture.release.wait(20):
                    fixture.errors.append('producer release barrier exceeded 20 seconds')
                    self.send_error(504)
                    return
                body = b'success([mark],false).\n'
                try:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Content-Length', str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    self.wfile.flush()
                    fixture.requests[-1]['sent_ms'] = fixture.elapsed()
                    fixture.sent.set()
                except (BrokenPipeError, ConnectionResetError) as error:
                    fixture.errors.append(type(error).__name__)

        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.url = f'http://127.0.0.1:{self.server.server_port}'
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def elapsed(self):
        return round((time.monotonic() - self.started) * 1000, 3)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
