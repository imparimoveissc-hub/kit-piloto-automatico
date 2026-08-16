#!/usr/bin/env python3
"""Facebook Marketplace MCP — stdio, zero extra deps (stdlib + httpx)."""
import json
import os
import sys
from pathlib import Path

import httpx

# ── config ────────────────────────────────────────────────────────────────────
_ENV = Path(__file__).parent / ".env"
for line in _ENV.read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

PAGE_ID = os.environ["FB_PAGE_ID"]
TOKEN   = os.environ["FB_PAGE_TOKEN"]
BASE    = f"https://graph.facebook.com/{os.environ.get('FB_API_VERSION','v20.0')}"

# ── Graph API helpers ─────────────────────────────────────────────────────────
def _get(path: str, **params) -> dict:
    params["access_token"] = TOKEN
    r = httpx.get(f"{BASE}{path}", params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def _post(path: str, payload: dict) -> dict:
    payload["access_token"] = TOKEN
    r = httpx.post(f"{BASE}{path}", json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

# ── tools ─────────────────────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "facebook_get_marketplace_conversations",
        "description": "Lista conversas da caixa de entrada do Marketplace da página Impar Imóveis. Filtra por não-lidas com unread_only=true.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "unread_only": {"type": "boolean", "default": False, "description": "Retorna apenas conversas com mensagens não lidas."},
                "limit": {"type": "integer", "default": 20, "maximum": 25, "description": "Quantidade de conversas (máx 25)."},
            },
        },
    },
    {
        "name": "facebook_get_conversation_messages",
        "description": "Retorna as mensagens de uma conversa do Marketplace pelo conversation_id.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "conversation_id": {"type": "string", "description": "ID da conversa (ex: t_4451176731593068)."},
                "limit": {"type": "integer", "default": 10, "maximum": 25},
            },
            "required": ["conversation_id"],
        },
    },
    {
        "name": "facebook_send_marketplace_reply",
        "description": "Envia uma resposta de texto para uma conversa do Marketplace.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "conversation_id": {"type": "string", "description": "ID da conversa."},
                "message": {"type": "string", "description": "Texto da resposta."},
            },
            "required": ["conversation_id", "message"],
        },
    },
]


def _call_tool(name: str, args: dict) -> str:
    if name == "facebook_get_marketplace_conversations":
        limit = min(int(args.get("limit", 20)), 25)
        data = _get(
            f"/{PAGE_ID}/conversations",
            folder="marketplace",
            fields="id,participants,updated_time,unread_count,snippet",
            limit=limit,
        )
        convs = data.get("data", [])
        if args.get("unread_only"):
            convs = [c for c in convs if c.get("unread_count", 0) > 0]
        return json.dumps(convs, ensure_ascii=False, indent=2)

    if name == "facebook_get_conversation_messages":
        cid = args["conversation_id"]
        limit = min(int(args.get("limit", 10)), 25)
        data = _get(
            f"/{cid}/messages",
            fields="id,message,from,created_time",
            limit=limit,
        )
        return json.dumps(data.get("data", []), ensure_ascii=False, indent=2)

    if name == "facebook_send_marketplace_reply":
        cid = args["conversation_id"]
        # Extrai recipient_id da conversa
        conv = _get(f"/{cid}", fields="participants")
        participants = conv.get("participants", {}).get("data", [])
        recipient = next((p for p in participants if p["id"] != PAGE_ID), None)
        if not recipient:
            return json.dumps({"error": "recipient não encontrado"})
        result = _post(
            f"/{PAGE_ID}/messages",
            {"recipient": {"id": recipient["id"]}, "message": {"text": args["message"]}},
        )
        return json.dumps(result, ensure_ascii=False)

    return json.dumps({"error": f"tool desconhecida: {name}"})


# ── MCP stdio loop ─────────────────────────────────────────────────────────────
def _send(obj: dict):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _handle(req: dict):
    method = req.get("method", "")
    rid    = req.get("id")

    if method == "initialize":
        _send({"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "facebook-marketplace-mcp", "version": "1.0.0"},
        }})

    elif method == "notifications/initialized":
        pass  # no response needed

    elif method == "tools/list":
        _send({"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}})

    elif method == "tools/call":
        tool_name = req["params"]["name"]
        tool_args = req["params"].get("arguments", {})
        try:
            result = _call_tool(tool_name, tool_args)
            _send({"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": result}]
            }})
        except Exception as e:
            _send({"jsonrpc": "2.0", "id": rid, "result": {
                "content": [{"type": "text", "text": f"Erro: {e}"}],
                "isError": True,
            }})
    else:
        if rid is not None:
            _send({"jsonrpc": "2.0", "id": rid, "error": {
                "code": -32601, "message": f"Method not found: {method}"
            }})


def main():
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            _handle(json.loads(raw))
        except Exception as e:
            _send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}})


if __name__ == "__main__":
    main()
