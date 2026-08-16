from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .bridge import WhatsAppFinanceBridge
from .models import Attachment, IncomingMessage


bridge = WhatsAppFinanceBridge()


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/ingest":
            self.send_error(404, "Nao encontrado")
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        attachments = [
            Attachment(**item)
            for item in payload.get("attachments", [])
        ]
        message = IncomingMessage(
            message_id=payload.get("message_id", ""),
            sender=payload.get("sender", ""),
            message_type=payload.get("message_type", "text"),
            text=payload.get("text", ""),
            attachments=attachments,
            timestamp=payload.get("timestamp", ""),
        )
        result = bridge.handle_message(message)
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = HTTPServer(("127.0.0.1", 8787), Handler)
    print("Assistente financeiro bridge em http://127.0.0.1:8787/ingest")
    server.serve_forever()


if __name__ == "__main__":
    main()

