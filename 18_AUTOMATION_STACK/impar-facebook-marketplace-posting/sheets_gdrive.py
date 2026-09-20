#!/usr/bin/env python3
"""
sheets_gdrive.py — Helper para ler/escrever Google Sheets via Drive API.
Usa o token OAuth do rclone (gdrive-impar) — sem nova autenticação necessária.
"""
import configparser
import csv
import io
import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

RCLONE_CONF    = Path.home() / ".config/rclone/rclone.conf"
RCLONE_REMOTE  = "gdrive-impar"

LEADS_SHEET_ID    = "1BQIOSmHAbvZsTCCfo9nHCS7Wa1bGEnRu_xbofRsF95c"
FOLLOWUP_SHEET_ID = "1iBFarUufuNnk83QPd3x0gkM2206rt7ywoqpAYiMstlA"


def get_token() -> str:
    """Rclone renova o token se expirado; retorna o access_token atual."""
    try:
        subprocess.run(
            ["/opt/homebrew/bin/rclone", "about", f"{RCLONE_REMOTE}:", "--json"],
            capture_output=True, timeout=45
        )
    except subprocess.TimeoutExpired:
        pass  # Token provavelmente ainda válido; continua
    conf = configparser.ConfigParser()
    conf.read(RCLONE_CONF)
    return json.loads(conf[RCLONE_REMOTE]["token"])["access_token"]


def export_rows(file_id: str, token: str) -> list:
    """Exporta Google Sheet como lista de linhas."""
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=text/csv"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    content = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    return list(csv.reader(io.StringIO(content)))


def export_dicts(file_id: str, token: str) -> tuple:
    """Retorna (headers: list[str], rows: list[dict])."""
    rows = export_rows(file_id, token)
    if not rows:
        return [], []
    headers = rows[0]
    return headers, [dict(zip(headers, row + [""] * max(0, len(headers) - len(row)))) for row in rows[1:]]


def upload_rows(file_id: str, rows: list, token: str):
    """Faz upload de linhas de volta ao Google Sheet (converte CSV → Sheets)."""
    out = io.StringIO()
    csv.writer(out).writerows(rows)
    csv_bytes = out.getvalue().encode("utf-8")

    boundary = "impar_gdrive_2026"
    metadata = json.dumps({"mimeType": "application/vnd.google-apps.spreadsheet"}).encode()
    body = (
        b"--" + boundary.encode() + b"\r\n"
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n" +
        metadata + b"\r\n"
        b"--" + boundary.encode() + b"\r\n"
        b"Content-Type: text/csv\r\n\r\n" +
        csv_bytes + b"\r\n"
        b"--" + boundary.encode() + b"--"
    )
    url = f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=multipart"
    req = urllib.request.Request(url, data=body, method="PATCH")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    try:
        urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Erro upload Sheet {file_id}: {e.code} — {e.read().decode()}")


def upload_dicts(file_id: str, headers: list, dicts: list, token: str):
    rows = [headers] + [[d.get(h, "") for h in headers] for d in dicts]
    upload_rows(file_id, rows, token)


def append_dict(file_id: str, row_dict: dict, token: str):
    """Adiciona um registro como nova linha."""
    headers, dicts = export_dicts(file_id, token)
    if not headers:
        headers = list(row_dict.keys())
    dicts.append(row_dict)
    upload_dicts(file_id, headers, dicts, token)


def update_rows_by_phone(file_id: str, telefone: str, updates: dict, token: str) -> bool:
    """Atualiza a linha com o telefone informado."""
    headers, dicts = export_dicts(file_id, token)
    updated = False
    for row in dicts:
        if row.get("telefone", "").strip() == telefone.strip():
            row.update(updates)
            updated = True
            break
    if updated:
        upload_dicts(file_id, headers, dicts, token)
    return updated
