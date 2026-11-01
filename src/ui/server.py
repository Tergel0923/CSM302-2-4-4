#!/usr/bin/env python3
"""Loopback-only UI; explicit demo/live selection, token and origin checks on writes."""
import argparse
import json
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from backend import DemoBackend, KernelBackend


def serve(mode, port):
    backend = DemoBackend() if mode == 'demo' else KernelBackend()
    token = secrets.token_urlsafe(32)
    origin = f'http://127.0.0.1:{port}'
    page = (Path(__file__).parent / 'index.html').read_text().replace('__TOKEN__', token)

    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, content, mime='application/json'):
            body = content.encode()
            self.send_response(status)
            self.send_header('Content-Type', mime + '; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self):
            return self.headers.get('Host') == f'127.0.0.1:{port}'

        def do_GET(self):
            if not self.valid_host():
                return self.reply(403, '{"error":"Хандалтын хаяг буруу"}')
            if self.path == '/':
                return self.reply(200, page, 'text/html')
            if self.path != '/api/state':
                return self.reply(404, '{"error":"Олдсонгүй"}')
            try:
                self.reply(200, json.dumps(backend.state()))
            except (OSError, ValueError) as exc:
                self.reply(400, json.dumps({'error': str(exc)}))

        def do_POST(self):
            if not self.valid_host() or self.headers.get('Origin') != origin or self.headers.get('X-KDS-Token') != token:
                return self.reply(403, '{"error":"Хүсэлт зөвшөөрөгдсөнгүй"}')
            if self.path != '/api/command':
                return self.reply(404, '{"error":"Олдсонгүй"}')
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 1024:
                    raise ValueError('Хүсэлтийн хэмжээ буруу.')
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError('JSON объект шаардлагатай.')
                backend.execute(data)
                self.reply(200, json.dumps(backend.state()))
            except (OSError, ValueError, TypeError) as exc:
                self.reply(400, json.dumps({'error': str(exc)}))

    print(f'{backend.mode}\n{origin} хаягийг нээнэ үү (зогсоох: Ctrl+C)', flush=True)
    server = HTTPServer(('127.0.0.1', port), Handler)
    server.timeout = 5
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Цөмийн өгөгдлийн бүтцийн вэб интерфейс')
    parser.add_argument('--mode', choices=('kernel', 'demo'), default='kernel', help='Горим: kernel = бодит цөм; demo = дадлага')
    parser.add_argument('--port', type=int, default=8765, help='Локал серверийн порт (анхны утга: 8765)')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('1024–65535 завсрын порт сонгоно уу.')
    serve(args.mode, args.port)
