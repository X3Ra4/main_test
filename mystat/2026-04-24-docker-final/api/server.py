from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json


class Api(BaseHTTPRequestHandler):
    def do_GET(self):
        status = 200 if self.path == "/api/notes" else 404
        payload = [{"title": "Docker", "body": "Вебінтерфейс читає API через Nginx."}] if status == 200 else {"error": "Not found"}
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with ThreadingHTTPServer(("0.0.0.0", 8000), Api) as server:
        server.serve_forever()
