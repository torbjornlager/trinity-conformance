"""Read-only RPC fixture with explicit guard-entry and response barriers."""
import http.server
import threading
import time


class GuardPeer:
    def __init__(self):
        self.arrived = threading.Event()
        self.release = threading.Event()
        self.requests = []
        self.body = b'success([v],false).\n'
        peer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                item = dict(path=self.path, arrived=time.monotonic())
                peer.requests.append(item)
                peer.arrived.set()
                if not peer.release.wait(20):
                    item['fixture_error'] = 'release deadline'
                    return
                item['released'] = time.monotonic()
                try:
                    self.send_response(200)
                    self.send_header('Content-Length', str(len(peer.body)))
                    self.end_headers()
                    self.wfile.write(peer.body)
                except (BrokenPipeError, ConnectionResetError):
                    item['client_closed'] = True

        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.release.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)

    def require_held_entry(self):
        if not self.arrived.wait(5) or len(self.requests) != 1 or self.release.is_set():
            raise AssertionError('missing unique held guard entry')
