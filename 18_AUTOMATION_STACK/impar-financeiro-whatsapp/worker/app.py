#!/usr/bin/env python3
"""Finance WhatsApp worker.

Reads the native WhatsApp macOS database and media folder, extracts daily
expense signals from the group "COMPROVANTE PAGAMENTO", classifies them,
deduplicates them, and writes confirmed expenses into the local finance app.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import sqlite3
import subprocess
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET


APP_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = Path(os.getenv("IMPAR_WORKSPACE_ROOT", "/workspace"))
STATE_DIR = Path(
    os.getenv(
        "IMPAR_FINANCE_STATE_DIR",
        WORKSPACE_ROOT / "05_WORKSPACE" / "clientes" / "jonata-impar" / "whatsapp",
    )
)
STATE_FILE = Path(os.getenv("IMPAR_FINANCE_STATE_FILE", STATE_DIR / ".capture-state.json"))
RUN_LOG = Path(os.getenv("IMPAR_FINANCE_RUN_LOG", STATE_DIR / "capture-runs.jsonl"))

WA_SHARED = Path(
    os.getenv(
        "IMPAR_WA_SHARED_DIR",
        "/Users/usuario/Library/Group Containers/group.net.whatsapp.WhatsApp.shared",
    )
)
WA_APP_CONTAINER = Path(
    os.getenv(
        "IMPAR_WA_CONTAINER_DIR",
        "/Users/usuario/Library/Containers/net.whatsapp.WhatsApp/Data/Library/Application Support/net.whatsapp.WhatsApp",
    )
)
CHAT_DB = Path(os.getenv("IMPAR_WA_DB", WA_SHARED / "ChatStorage.sqlite"))
MEDIA_ROOT = Path(os.getenv("IMPAR_WA_MEDIA_ROOT", WA_SHARED / "Message" / "Media"))

GROUP_NAME = os.getenv("IMPAR_WA_GROUP_NAME", "COMPROVANTE PAGAMENTO")
GROUP_JID = os.getenv("IMPAR_WA_GROUP_JID", "120363426404057193@g.us")
FINANCE_API = os.getenv("IMPAR_FINANCE_API", "http://host.docker.internal:4173/api/transactions")
FINANCE_STATE_FILE = Path(
    os.getenv(
        "IMPAR_FINANCE_STATE_JSON",
        WORKSPACE_ROOT / "05_WORKSPACE" / "clientes" / "impar-imoveis" / "financeiro" / "financeiro.json",
    )
)
WEBHOOK_KEY = os.getenv("IMPAR_WEBHOOK_KEY", "")
PORT = int(os.getenv("IMPAR_WORKER_PORT", "8091"))
HOST = os.getenv("IMPAR_WORKER_HOST", "0.0.0.0")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
PDF_EXTS = {".pdf"}
DOCX_EXTS = {".docx"}
AUDIO_EXTS = {".ogg", ".opus", ".mp3", ".m4a", ".aac", ".wav", ".caf"}
SKIP_EXTS = {".thumb", ".mmsthumb"}

KEYWORDS_PJ = {
    "obra",
    "empresa",
    "fornecedor",
    "cliente",
    "nota",
    "nf",
    "pj",
    "projeto",
    "material",
    "servico",
    "serviço",
    "condominio",
    "condomínio",
    "imobiliaria",
    "imobiliária",
}
KEYWORDS_PF = {
    "mercado",
    "farmacia",
    "farmácia",
    "gasolina",
    "uber",
    "ifood",
    "casa",
    "pessoal",
    "lazer",
    "transporte",
}
CARD_BANK_INTER_HINTS = (
    " banco inter",
    "banco inter",
    " inter ",
    "inter ",
    " inter",
)
CATEGORY_RULES = [
    ({"mercado", "supermercado", "hortifruti"}, "Alimentação"),
    ({"gasolina", "etanol", "posto", "combustivel", "combustível"}, "Transporte"),
    ({"farmacia", "farmácia", "medicamento"}, "Saúde"),
    ({"uber", "99", "taxi", "táxi"}, "Transporte"),
    ({"ifood", "restaurante", "lanchonete", "alimentacao", "alimentação"}, "Alimentação"),
    ({"material", "obra", "cimento", "tinta", "pedreiro"}, "Obras e manutenção"),
    ({"software", "assinatura", "serviço", "servico", "sistema"}, "Serviços"),
]

AMOUNT_RE = re.compile(
    r"(?:R\$|BRL)?\s*([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2}|[0-9]+(?:,[0-9]{2})?)",
    re.IGNORECASE,
)
DATE_RE = re.compile(r"(\d{2}/\d{2}(?:/\d{2,4})?)")
WHITESPACE_RE = re.compile(r"\s+")

STATE_LOCK = threading.Lock()


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def now_ts() -> float:
    return dt.datetime.now().timestamp()


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)


def normalize_text(value: str) -> str:
    value = html.unescape(value or "")
    value = value.replace("\u200e", " ").replace("\u200f", " ")
    return WHITESPACE_RE.sub(" ", value).strip()


def normalize_digits(value: str) -> str:
    return re.sub(r"\D+", "", value or "")


def parse_amount(text: str) -> float | None:
    if not text:
        return None
    match = AMOUNT_RE.search(text.replace(" ", ""))
    if not match:
        return None
    raw = match.group(1).replace(".", "").replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return None


def parse_date(text: str) -> str | None:
    if not text:
        return None
    match = DATE_RE.search(text)
    if not match:
        return None
    raw = match.group(1)
    parts = raw.split("/")
    today = dt.date.today()
    if len(parts) == 2:
        return f"{parts[0]}/{parts[1]}/{today.year}"
    if len(parts) == 3 and len(parts[2]) == 2:
        return f"{parts[0]}/{parts[1]}/20{parts[2]}"
    return raw


def classify_entity(text: str) -> str:
    lowered = text.lower()
    if any(hint in lowered for hint in CARD_BANK_INTER_HINTS):
        return "pj"
    score_pj = sum(1 for kw in KEYWORDS_PJ if kw in lowered)
    score_pf = sum(1 for kw in KEYWORDS_PF if kw in lowered)
    if score_pj > score_pf:
        return "pj"
    return "pf"


def classify_category(text: str) -> str:
    lowered = text.lower()
    for keywords, category in CATEGORY_RULES:
        if any(kw in lowered for kw in keywords):
            return category
    if classify_entity(text) == "pj":
        return "Despesas operacionais"
    return "Outras despesas"


def finance_month(date_text: str | None) -> str:
    if not date_text:
        return dt.date.today().strftime("%Y-%m")
    parts = date_text.split("/")
    if len(parts) == 3:
        return f"{parts[2]}-{parts[1]}"
    return dt.date.today().strftime("%Y-%m")


def fingerprint(*parts: str) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update((part or "").encode("utf-8", "ignore"))
        h.update(b"\0")
    return h.hexdigest()


def load_state() -> dict[str, Any]:
    ensure_dirs()
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "version": 1,
        "last_run_at": None,
        "last_message_ts": 0.0,
        "last_media_mtime": 0.0,
        "seen_fingerprints": [],
        "runs": [],
    }


def save_state(state: dict[str, Any]) -> None:
    ensure_dirs()
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(STATE_FILE)


def append_run(entry: dict[str, Any]) -> None:
    ensure_dirs()
    with RUN_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def db_connection() -> sqlite3.Connection:
    if not CHAT_DB.exists():
        raise FileNotFoundError(f"WhatsApp DB nao encontrada: {CHAT_DB}")
    conn = sqlite3.connect(f"file:{CHAT_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def find_chat_session(conn: sqlite3.Connection) -> sqlite3.Row:
    rows = conn.execute(
        """
        SELECT Z_PK, ZCONTACTJID, ZPARTNERNAME, ZLASTMESSAGEDATE, ZLASTMESSAGETEXT
        FROM ZWACHATSESSION
        WHERE lower(COALESCE(ZPARTNERNAME, '')) = lower(?)
           OR ZCONTACTJID = ?
        ORDER BY ZLASTMESSAGEDATE DESC
        """,
        (GROUP_NAME, GROUP_JID),
    ).fetchall()
    if not rows:
        raise RuntimeError(f"Grupo nao encontrado: {GROUP_NAME} / {GROUP_JID}")
    return rows[0]


def cocoa_to_iso(ts_value: float | int | None) -> str:
    if not ts_value:
        return ""
    unix_ts = float(ts_value) + 978307200
    return dt.datetime.fromtimestamp(unix_ts).astimezone().isoformat(timespec="seconds")


def fetch_messages(conn: sqlite3.Connection, chat_pk: int, last_message_ts: float) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT Z_PK, ZISFROMME, ZMESSAGEDATE, ZSENTDATE, ZFROMJID, ZPUSHNAME, ZTEXT, ZMESSAGETYPE, ZMEDIAITEM
        FROM ZWAMESSAGE
        WHERE ZCHATSESSION = ? AND ZMESSAGEDATE > ?
        ORDER BY ZMESSAGEDATE ASC, Z_PK ASC
        """,
        (chat_pk, last_message_ts),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        text = normalize_text(row["ZTEXT"] or "")
        if not text and int(row["ZMESSAGETYPE"] or 0) not in {1, 3, 5, 6, 10}:
            continue
        result.append(
            {
                "kind": "message",
                "message_id": int(row["Z_PK"]),
                "is_from_me": bool(row["ZISFROMME"]),
                "ts": float(row["ZMESSAGEDATE"] or 0),
                "sent_ts": float(row["ZSENTDATE"] or 0) if row["ZSENTDATE"] else None,
                "sender": normalize_text(row["ZPUSHNAME"] or row["ZFROMJID"] or ""),
                "text": text,
                "message_type": int(row["ZMESSAGETYPE"] or 0),
                "media_item": int(row["ZMEDIAITEM"]) if row["ZMEDIAITEM"] is not None else None,
            }
        )
    return result


def list_candidate_files(root: Path, min_mtime: float) -> list[Path]:
    if not root.exists():
        return []
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_EXTS:
            continue
        try:
            if path.stat().st_mtime <= min_mtime:
                continue
        except FileNotFoundError:
            continue
        candidates.append(path)
    candidates.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0)
    return candidates


def run_command(cmd: list[str], timeout: int = 120) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError:
        return ""
    out = (proc.stdout or "") + (proc.stderr or "")
    return out.strip()


def extract_docx_text(path: Path) -> str:
    parts: list[str] = []
    with zipfile.ZipFile(path) as zf:
        with zf.open("word/document.xml") as fp:
            xml = ET.fromstring(fp.read())
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        for para in xml.findall(".//w:p", ns):
            texts = [node.text for node in para.findall(".//w:t", ns) if node.text]
            line = "".join(texts).strip()
            if line:
                parts.append(line)
    return "\n".join(parts)


def extract_pdf_text(path: Path) -> str:
    text = run_command(["pdftotext", "-layout", str(path), "-"], timeout=120)
    if text:
        return text
    with tempfile.TemporaryDirectory() as tmpdir:
        prefix = Path(tmpdir) / "page"
        run_command(["pdftoppm", "-png", str(path), str(prefix)], timeout=180)
        pieces: list[str] = []
        for png in sorted(Path(tmpdir).glob("page-*.png")):
            pieces.append(extract_ocr_text(png))
        return "\n".join(pieces)


def extract_ocr_text(path: Path) -> str:
    return run_command(["tesseract", str(path), "stdout", "-l", "por+eng", "--psm", "6"], timeout=180)


def extract_audio_text(path: Path) -> str:
    try:
        import whisper  # type: ignore
    except Exception:
        return ""

    model_name = os.getenv("IMPAR_WHISPER_MODEL", "base")
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(str(path), language="pt")
        return normalize_text(result.get("text", ""))
    except Exception:
        return ""


def extract_file_text(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTS:
        return "image", extract_ocr_text(path)
    if suffix in PDF_EXTS:
        return "pdf", extract_pdf_text(path)
    if suffix in DOCX_EXTS:
        return "docx", extract_docx_text(path)
    if suffix in AUDIO_EXTS:
        return "audio", extract_audio_text(path)
    return "unknown", ""


def guess_source_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTS:
        return "image"
    if suffix in PDF_EXTS:
        return "pdf"
    if suffix in DOCX_EXTS:
        return "docx"
    if suffix in AUDIO_EXTS:
        return "audio"
    return "unknown"


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_text_blob(*parts: str) -> str:
    unique_parts: list[str] = []
    seen_parts: set[str] = set()
    for part in parts:
        clean = normalize_text(part or "")
        if not clean or clean in seen_parts:
            continue
        seen_parts.add(clean)
        unique_parts.append(clean)
    text = normalize_text("\n".join(unique_parts))
    return text


def build_candidate(
    *,
    sender: str,
    source_kind: str,
    source_name: str,
    source_text: str,
    raw_text: str,
    timestamp_iso: str,
    source_ts: float | None = None,
    source_mtime: float | None = None,
) -> dict[str, Any]:
    blob = build_text_blob(source_text, raw_text, sender, source_name)
    amount = parse_amount(blob)
    date_text = parse_date(blob)
    category = classify_category(blob)
    entity = classify_entity(blob)
    description = source_name
    if blob:
        first_line = blob.splitlines()[0]
        description = first_line[:120]
    if source_kind == "audio" and not blob:
        description = "Audio sem transcricao"
    if source_kind in {"image", "pdf", "docx"} and "comprovante" in blob.lower():
        description = "Comprovante de pagamento"
    fingerprint_parts = [
        sender,
        source_kind,
        source_name,
        blob[:300],
        str(amount or 0),
        str(date_text or ""),
    ]
    return {
        "sender": sender or GROUP_NAME,
        "source_kind": source_kind,
        "source_name": source_name,
        "text": blob,
        "amount": amount,
        "date_text": date_text,
        "category": category,
        "entity": entity,
        "description": description,
        "timestamp": timestamp_iso,
        "source_ts": source_ts,
        "source_mtime": source_mtime,
        "fingerprint": fingerprint(*fingerprint_parts),
    }


def is_duplicate(candidate: dict[str, Any], state: dict[str, Any]) -> bool:
    seen = set(state.get("seen_fingerprints", []))
    return candidate["fingerprint"] in seen


def mark_seen(candidate: dict[str, Any], state: dict[str, Any]) -> None:
    seen = state.setdefault("seen_fingerprints", [])
    seen.append(candidate["fingerprint"])
    if len(seen) > 1000:
        del seen[:-500]


def finance_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    amount = float(candidate["amount"] or 0)
    date_text = candidate["date_text"] or dt.date.today().strftime("%d/%m/%Y")
    return {
        "type": "expense",
        "source": "whatsapp-group",
        "description": candidate["description"][:120] or "Gasto via WhatsApp",
        "party": candidate.get("sender", GROUP_NAME),
        "document": candidate["source_name"],
        "amount": round(amount, 2),
        "date": date_text,
        "competence": finance_month(date_text),
        "category": candidate["category"],
        "entity": candidate["entity"],
        "expenseKind": "daily",
        "paid": False,
        "note": f"Origem: {GROUP_NAME} | {candidate['source_kind']} | {candidate['source_name']}",
        "sourceRef": candidate["fingerprint"],
    }


def clarification_text(candidate: dict[str, Any]) -> str:
    if candidate["source_kind"] == "audio":
        return "Consigo ouvir o áudio, mas ainda não peguei o valor. Me manda o valor ou escreve em uma frase curta."
    if candidate["source_kind"] in {"image", "pdf", "docx"}:
        return "Consigo ler o comprovante, mas ainda não entendi o valor. Me confirma em uma frase curta?"
    return "Consigo ler a mensagem, mas ainda não entendi o valor. Me confirma em uma frase curta?"


def normalize_finance_transaction(payload: dict[str, Any]) -> dict[str, Any]:
    now = now_iso()
    date_text = normalize_text(str(payload.get("date") or ""))[:10]
    if not date_text:
        date_text = dt.date.today().isoformat()
    entity = "pf" if str(payload.get("entity") or "").lower() == "pf" else "pj"
    expense_kind = str(payload.get("expenseKind") or "one_off")
    if expense_kind not in {"monthly", "daily", "one_off"}:
        expense_kind = "one_off"
    transaction = {
        "id": str(payload.get("id") or f"manual:{hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]}"),
        "type": "expense" if str(payload.get("type") or "expense") == "expense" else "income",
        "source": str(payload.get("source") or "manual"),
        "description": normalize_text(str(payload.get("description") or payload.get("party") or "Lancamento"))[:120],
        "party": normalize_text(str(payload.get("party") or ""))[:120],
        "document": normalize_text(str(payload.get("document") or ""))[:120],
        "amount": round(max(0.0, float(payload.get("amount") or 0)), 2),
        "date": date_text,
        "competence": str(payload.get("competence") or date_text[:7]),
        "category": normalize_text(str(payload.get("category") or ("Outras despesas" if payload.get("type") == "expense" else "Receita de servicos"))),
        "entity": entity,
        "expenseKind": expense_kind,
        "paid": bool(payload.get("paid")),
        "paidAt": payload.get("paidAt") or None,
        "paymentMethod": normalize_text(str(payload.get("paymentMethod") or "")),
        "note": normalize_text(str(payload.get("note") or "")),
        "noteNumber": str(payload.get("noteNumber") or ""),
        "accessKey": str(payload.get("accessKey") or ""),
        "fiscalStatus": str(payload.get("fiscalStatus") or ""),
        "sourceRef": str(payload.get("sourceRef") or ""),
        "createdAt": payload.get("createdAt") or now,
        "updatedAt": now,
    }
    return transaction


def read_finance_state() -> dict[str, Any]:
    if FINANCE_STATE_FILE.exists():
        try:
            return json.loads(FINANCE_STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": 1, "company": {}, "transactions": []}


def save_finance_state(state: dict[str, Any]) -> None:
    FINANCE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = FINANCE_STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(FINANCE_STATE_FILE)


def create_finance_transaction_local(payload: dict[str, Any]) -> dict[str, Any]:
    with STATE_LOCK:
        state = read_finance_state()
        transactions = state.setdefault("transactions", [])
        source_ref = str(payload.get("sourceRef") or "")
        note = str(payload.get("note") or "")
        duplicate = next(
            (
                item
                for item in transactions
                if source_ref and str(item.get("sourceRef") or "") == source_ref
                or (source_ref and source_ref in str(item.get("note") or ""))
                or (note and note == str(item.get("note") or ""))
            ),
            None,
        )
        if duplicate:
            return duplicate
        transaction = normalize_finance_transaction(payload)
        transactions.append(transaction)
        save_finance_state(state)
        return transaction


def post_finance(transaction: dict[str, Any]) -> tuple[bool, str, dict[str, Any] | None]:
    body = json.dumps(transaction).encode("utf-8")
    request = urllib.request.Request(
        FINANCE_API,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return True, "created", payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "ignore") if hasattr(exc, "read") else str(exc)
        try:
            created = create_finance_transaction_local(transaction)
            return True, "created_local", created
        except Exception as local_exc:
            return False, f"http_{exc.code}", {"error": detail, "local_error": str(local_exc)}
    except Exception as exc:
        try:
            created = create_finance_transaction_local(transaction)
            return True, "created_local", created
        except Exception as local_exc:
            return False, "request_failed", {"error": str(exc), "local_error": str(local_exc)}


def process_daily() -> dict[str, Any]:
    ensure_dirs()
    state = load_state()
    started_at = now_iso()
    last_message_ts = float(state.get("last_message_ts") or 0.0)
    last_media_mtime = float(state.get("last_media_mtime") or 0.0)

    conn = db_connection()
    chat = find_chat_session(conn)
    chat_pk = int(chat["Z_PK"])
    chat_name = chat["ZPARTNERNAME"] or GROUP_NAME
    chat_jid = chat["ZCONTACTJID"] or GROUP_JID
    message_rows = fetch_messages(conn, chat_pk, last_message_ts)
    conn.close()

    media_dir = MEDIA_ROOT / chat_jid
    media_files = list_candidate_files(media_dir, last_media_mtime)

    candidates: list[dict[str, Any]] = []
    processed_messages = 0
    processed_files = 0

    for row in message_rows:
        text = row["text"] or ""
        if not text:
            continue
        processed_messages += 1
        ts_iso = cocoa_to_iso(row["ts"])
        candidates.append(
            build_candidate(
                sender=row["sender"] or chat_name,
                source_kind="message",
                source_name=f"mensagem:{row['message_id']}",
                source_text=text,
                raw_text=text,
                timestamp_iso=ts_iso,
                source_ts=row["ts"],
            )
        )

    for path in media_files:
        source_kind = guess_source_kind(path)
        processed_files += 1
        if source_kind == "unknown":
            continue
        extracted_kind, extracted_text = extract_file_text(path)
        candidates.append(
            build_candidate(
                sender=chat_name,
                source_kind=extracted_kind,
                source_name=path.name,
                source_text=extracted_text,
                raw_text=extracted_text,
                timestamp_iso=dt.datetime.fromtimestamp(path.stat().st_mtime).astimezone().isoformat(
                    timespec="seconds"
                ),
                source_mtime=path.stat().st_mtime,
            )
        )

    summary: dict[str, Any] = {
        "ok": True,
        "group": {"name": chat_name, "jid": chat_jid, "chat_pk": chat_pk},
        "started_at": started_at,
        "processed_messages": processed_messages,
        "processed_files": processed_files,
        "considered": len(candidates),
        "confirmed": 0,
        "needs_clarification": 0,
        "duplicate": 0,
        "blocked": 0,
        "transactions": [],
        "questions": [],
        "files": [str(path) for path in media_files[:40]],
    }

    max_message_ts = last_message_ts
    max_media_mtime = last_media_mtime

    for candidate in candidates:
        if candidate["source_kind"] == "message" and candidate.get("source_ts"):
            max_message_ts = max(max_message_ts, float(candidate["source_ts"]))
        if candidate["source_kind"] != "message" and candidate.get("source_mtime"):
            max_media_mtime = max(max_media_mtime, float(candidate["source_mtime"]))

        if is_duplicate(candidate, state):
            summary["duplicate"] += 1
            continue

        if candidate["amount"] is None or candidate["amount"] <= 0:
            summary["needs_clarification"] += 1
            summary["questions"].append(
                {
                    "source": candidate["source_name"],
                    "text": clarification_text(candidate),
                }
            )
            mark_seen(candidate, state)
            continue

        payload = finance_payload(candidate)
        created, status, response = post_finance(payload)
        if created:
            summary["confirmed"] += 1
            summary["transactions"].append(
                {
                    "source": candidate["source_name"],
                    "amount": candidate["amount"],
                    "date": candidate["date_text"] or dt.date.today().strftime("%d/%m/%Y"),
                    "category": candidate["category"],
                    "entity": candidate["entity"],
                    "description": candidate["description"],
                    "finance_status": status,
                }
            )
            mark_seen(candidate, state)
            continue

        summary["blocked"] += 1
        summary["questions"].append(
            {
                "source": candidate["source_name"],
                "text": f"Nao consegui salvar automaticamente: {response.get('error', status)}",
            }
        )

    state["last_run_at"] = started_at
    state["last_message_ts"] = max_message_ts
    state["last_media_mtime"] = max_media_mtime
    state.setdefault("runs", []).append(
        {
            "run_at": started_at,
            "summary": {
                "confirmed": summary["confirmed"],
                "needs_clarification": summary["needs_clarification"],
                "duplicate": summary["duplicate"],
                "blocked": summary["blocked"],
                "considered": summary["considered"],
            },
        }
    )
    save_state(state)
    append_run(summary)
    return summary


def health_payload() -> dict[str, Any]:
    state = load_state()
    return {
        "ok": True,
        "group": {"name": GROUP_NAME, "jid": GROUP_JID},
        "db_exists": CHAT_DB.exists(),
        "media_root_exists": MEDIA_ROOT.exists(),
        "state_file": str(STATE_FILE),
        "last_run_at": state.get("last_run_at"),
    }


def handle_json(request: BaseHTTPRequestHandler, status: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request.send_response(status)
    request.send_header("Content-Type", "application/json; charset=utf-8")
    request.send_header("Cache-Control", "no-store")
    request.send_header("Content-Length", str(len(body)))
    request.end_headers()
    request.wfile.write(body)


class WorkerHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: D401
        return

    def _authorized(self) -> bool:
        if not WEBHOOK_KEY:
            return True
        return self.headers.get("x-impar-key", "") == WEBHOOK_KEY

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/", "/health"}:
            handle_json(self, 200, health_payload())
            return
        handle_json(self, 404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if not self._authorized():
            handle_json(self, 401, {"ok": False, "error": "unauthorized"})
            return

        if self.path == "/run-daily":
            try:
                payload = process_daily()
                handle_json(self, 200, payload)
            except Exception as exc:  # pragma: no cover - operational safety
                handle_json(self, 500, {"ok": False, "error": str(exc)})
            return

        if self.path == "/health":
            handle_json(self, 200, health_payload())
            return

        handle_json(self, 404, {"ok": False, "error": "not_found"})


def main() -> None:
    ensure_dirs()
    server = ThreadingHTTPServer((HOST, PORT), WorkerHandler)
    print(f"Finance worker available on http://{HOST}:{PORT}")
    print(f"Reading DB: {CHAT_DB}")
    print(f"Media root: {MEDIA_ROOT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
