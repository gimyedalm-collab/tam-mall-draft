"""Loopback-only HTTP fixture with shared download cap; not a real mobile network.

Use the approved browser connection for UI checks. This server only serves files.
"""
import argparse
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
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
            super().end_headers()

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
            while block := source.read(8192):
                with lock:
                    now = time.monotonic()
                    next_send = max(now, next_send) + len(block) / args.bytes_per_second
                    delay = next_send - now
                time.sleep(delay)
                outputfile.write(block)
                self.sent += len(block)

    print(json.dumps({'host': '127.0.0.1', 'port': args.port, 'shared_bytes_per_second': args.bytes_per_second,
                      'server_delay_ms_per_request': args.latency_ms, 'cache': 'no-store'}), flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()


if __name__ == '__main__':
    main()
