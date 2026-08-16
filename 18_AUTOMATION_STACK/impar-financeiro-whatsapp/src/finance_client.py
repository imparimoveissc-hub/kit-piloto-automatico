from __future__ import annotations

import json
from urllib import request, error


class FinanceApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:4173") -> None:
        self.base_url = base_url.rstrip("/")

    def create_transaction(self, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api/transactions",
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"finance_api_http_{exc.code}: {body}") from exc
