#!/usr/bin/env python3
"""
Processador de leads Chaves na Mão

Arquitetura:
  Claude (cron) → Outlook via Rube MCP → extrai leads → chama este script com JSON

Uso:
  python3 check_chaves_na_mao_leads.py --leads '[{"nome":"...","telefone":"...","ref":"...","received_at":"...","resumo":"..."}]'
  python3 check_chaves_na_mao_leads.py --lead-json '{"nome":...}'   # lead único

Saídas:
  logs/chaves-na-mao-processed.json  — deduplicação (24h por telefone)
  logs/chaves-na-mao-check.log       — log de execuções
  planilha leads_marketplace_captura.csv — linha adicionada por lead novo
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOGS_DIR = BASE / "logs"
LOGS_DIR.mkdir(exist_ok=True)

STATE_FILE = LOGS_DIR / "chaves-na-mao-processed.json"
LOG_FILE = LOGS_DIR / "chaves-na-mao-check.log"

KIT_ROOT = Path(__file__).resolve().parent.parent.parent
PLANILHA_CSV = (
    KIT_ROOT / "05_WORKSPACE" / "clientes" / "impar-imoveis" / "automacoes"
    / "facebook-marketplace" / "leads_marketplace_captura.csv"
)

NOTIFY_SCRIPT = (
    BASE.parent / "impar-facebook-marketplace-posting" / "notificar_lead_whatsapp.py"
)

CHECKPOINT_FILE = Path.home() / ".local" / "impar-automation" / "chaves-na-mao" / "checkpoint.json"


def log(msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} | {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_processed() -> dict:
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE) as f:
        return json.load(f)


def save_processed(data: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def update_checkpoint():
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"alerted_leads_24h": {}, "last_checked": datetime.now(timezone.utc).isoformat()}
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(data, f)


def normalize_phone_br(raw: str) -> str | None:
    d = re.sub(r"\D+", "", raw or "")
    if not d:
        return None
    d = d.lstrip("0")
    if d.startswith("55") and len(d) >= 12:
        pass
    elif len(d) == 11:
        d = "55" + d
    elif len(d) == 10:
        d = "55" + d
    elif len(d) in (8, 9):
        d = "5547" + d  # padrão Joinville
    else:
        return None
    if len(d) == 12 and d[4] in "6789":
        d = d[:4] + "9" + d[4:]
    if len(d) not in (12, 13):
        return None
    return d


def is_duplicate(telefone_norm: str, received_at: str, processed: dict) -> bool:
    key = f"{telefone_norm}_{received_at}"
    return key in processed


def add_to_planilha(nome: str, telefone: str, ref: str, resumo: str, data_contato: str) -> bool:
    if not PLANILHA_CSV.exists():
        log(f"ERRO: Planilha não encontrada em {PLANILHA_CSV}")
        return False
    try:
        with open(PLANILHA_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nome, telefone, "Venda", ref, "[A PREENCHER]",
                             "Telefone Capturado", data_contato, "Chaves na Mão", resumo])
        log(f"✅ {nome} adicionado à planilha")
        return True
    except Exception as e:
        log(f"ERRO ao adicionar {nome} à planilha: {e}")
        return False


def send_notification(nome: str, telefone: str, ref: str, resumo: str) -> bool:
    if not NOTIFY_SCRIPT.exists():
        log(f"AVISO: script de notificação não encontrado em {NOTIFY_SCRIPT}")
        return False
    try:
        result = subprocess.run(
            [sys.executable, str(NOTIFY_SCRIPT),
             "--nome", nome, "--telefone", telefone,
             "--resumo", resumo, "--link-imovel", ref or "",
             "--origem", "chaves_na_mao"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            log(f"✅ WhatsApp enviado: {nome} ({telefone})")
            return True
        else:
            log(f"⚠️ WhatsApp falhou para {nome}: {result.stderr.strip()}")
            return False
    except Exception as e:
        log(f"ERRO ao enviar WhatsApp para {nome}: {e}")
        return False


def process_lead(lead: dict, processed: dict) -> bool:
    nome = (lead.get("nome") or "").strip()
    telefone_raw = (lead.get("telefone") or "").strip()
    ref = (lead.get("ref") or "").strip()
    resumo = (lead.get("resumo") or "").strip()
    received_at = lead.get("received_at") or datetime.now(timezone.utc).isoformat()

    if not nome or not telefone_raw:
        log(f"⚠️ Dados incompletos — nome='{nome}' tel='{telefone_raw}' — pulando")
        return False

    telefone = normalize_phone_br(telefone_raw)
    if not telefone:
        log(f"⚠️ Telefone inválido: {telefone_raw} — pulando {nome}")
        return False

    key = f"{telefone}_{received_at}"
    if key in processed:
        log(f"ℹ️  {nome} ({telefone}) já processado — pulando")
        return False

    data_contato = received_at[:10]  # YYYY-MM-DD
    if not add_to_planilha(nome, telefone, ref, resumo, data_contato):
        return False

    send_notification(nome, telefone, ref, resumo)

    processed[key] = {
        "nome": nome, "telefone": telefone, "ref": ref,
        "processado_em": datetime.now(timezone.utc).isoformat(),
    }
    return True


def main():
    parser = argparse.ArgumentParser(description="Processador de leads Chaves na Mão")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--leads", help="JSON array de leads")
    group.add_argument("--lead-json", help="JSON de um único lead")
    parser.add_argument("--dry-run", action="store_true", help="Não grava nada, só loga")
    args = parser.parse_args()

    log("🔄 Iniciando processamento de leads Chaves na Mão...")

    if args.leads:
        leads = json.loads(args.leads)
    elif args.lead_json:
        leads = [json.loads(args.lead_json)]
    else:
        log("ℹ️  Nenhum lead passado — encerrando (use --leads '[...]' com dados do Outlook via Rube MCP)")
        update_checkpoint()
        return

    if not leads:
        log("✅ Lista de leads vazia — nenhum novo lead")
        update_checkpoint()
        return

    processed = load_processed()
    novos = 0

    for lead in leads:
        if args.dry_run:
            log(f"[DRY-RUN] lead: {lead}")
            continue
        if process_lead(lead, processed):
            novos += 1

    if not args.dry_run:
        save_processed(processed)
        update_checkpoint()

    log(f"✅ Concluído — {novos} lead(s) novo(s) processado(s) de {len(leads)} recebido(s)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERRO CRÍTICO: {e}")
        sys.exit(1)
