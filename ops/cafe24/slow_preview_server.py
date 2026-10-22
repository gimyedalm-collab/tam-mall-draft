"""Loopback-only HTTP fixture with shared download cap; not a real mobile network.

Use the approved browser connection for UI checks. This server only serves files.
"""
import argparse
import json
import re
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import TCPServer
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--port', type=int, default=18925)
    parser.add_argument('--bytes-per-second', type=int, default=200000)
    parser.add_argument('--latency-ms', type=int, default=150)
    parser.add_argument('--log', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    lock, log_lock = threading.Lock(), threading.Lock()
    next_send = time.monotonic()
    args.log.parent.mkdir(parents=True, exist_ok=True)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(root), **kw)

        def log_message(self, *a):
            pass

        def end_headers(self):
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Accept-Ranges', 'bytes')
            super().end_headers()

        def send_head(self):
            self.remaining = None
            path = Path(self.translate_path(self.path))
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers.get('Range', ''))
            if not match or not path.is_file() or not any(match.groups()):
                return super().send_head()
            size = path.stat().st_size
            first, last = match.groups()
            start = int(first) if first else max(0, size - int(last))
            end = min(int(last), size - 1) if first and last else size - 1
            if start > end or start >= size:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{size}')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return None
            source = path.open('rb')
            source.seek(start)
            self.remaining = end - start + 1
            self.send_response(206)
            self.send_header('Content-Type', self.guess_type(str(path)))
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.send_header('Content-Length', str(self.remaining))
            self.end_headers()
            return source

        def do_GET(self):
            self.started, self.sent = time.monotonic(), 0
            self.status, self.aborted = None, False
            time.sleep(args.latency_ms / 1000)
            try:
                super().do_GET()
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                self.aborted = True
            finally:
                row = {'path': urlsplit(self.path).path, 'status': self.status,
                       'sent_bytes': self.sent, 'seconds': round(time.monotonic() - self.started, 3),
                       'aborted_by_navigation': self.aborted,
                       'finished_monotonic': time.monotonic()}
                with log_lock, args.log.open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps(row) + '\n')

        def send_response(self, code, message=None):
            self.status = code
            super().send_response(code, message)

        def copyfile(self, source, outputfile):
            nonlocal next_send
            while self.remaining is None or self.remaining > 0:
                block = source.read(8192 if self.remaining is None else min(8192, self.remaining))
                if not block:
                    break
                with lock:
                    now = time.monotonic()
                    next_send = max(now, next_send) + len(block) / args.bytes_per_second
                    delay = next_send - now
                time.sleep(delay)
                outputfile.write(block)
                self.sent += len(block)
                if self.remaining is not None:
                    self.remaining -= len(block)

    class LoopbackServer(ThreadingHTTPServer):
        def server_bind(self):
            # HTTPServer performs reverse DNS during bind. This loopback fixture
            # has a known hostname and must not depend on the runner's resolver.
            TCPServer.server_bind(self)
            self.server_name, self.server_port = self.server_address[:2]

    server = LoopbackServer(('127.0.0.1', args.port), Handler)
    print(json.dumps({'host': '127.0.0.1', 'port': args.port, 'shared_bytes_per_second': args.bytes_per_second,
                      'server_delay_ms_per_request': args.latency_ms, 'cache': 'no-store'}), flush=True)
    server.serve_forever()


if __name__ == '__main__':
    main()
