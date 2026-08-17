#!/usr/bin/env python3
"""
leads_watcher.py — substitui impar-notificar-leads-planilha (Claude task a cada 5 min).
Custo: 0 tokens quando não há lead novo. Claude só é chamado quando há novo lead (0-5x/dia).

Fonte no kit: 18_AUTOMATION_STACK/impar-leads-planilha-watcher/leads_watcher.py
Destino na máquina: ~/.local/impar-automation/leads-planilha/leads_watcher.py
Para instalar: bash <kit>/kos-install.sh
"""
import csv
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

KIT_DIR = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
CSV = KIT_DIR / "05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv"
LOG_DIR = KIT_DIR / "07_LOGS"

STATE = Path.home() / ".local/impar-automation/leads-planilha/ultimo-estado.json"
LOG = LOG_DIR / "notificar-leads-planilha.log"
GRUPO = "NOVOS LEADS"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"ultima_linha": 0}


def save_state(n: int):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({
        "ultima_linha": n,
        "atualizado_em": datetime.now().isoformat(timespec="seconds"),
    }))


def log(msg: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def format_message(lead: dict) -> str:
    canal = lead.get("canal_entrada", "site").lower()
    nome = lead.get("nome", "?")
    tel = lead.get("telefone", "")
    imovel = lead.get("descricao_imovel", "")
    ref = lead.get("ref_imovel", "")
    tel_clean = "".join(c for c in tel if c.isdigit())
    tel_display = "+" + (tel_clean if tel_clean.startswith("55") else "55" + tel_clean) if tel_clean else tel
    wa_link = f"https://wa.me/{tel_clean}" if tel_clean else ""

    if "chaves" in canal:
        header = "🔔 NOVO LEAD CHAVES NA MÃO"
    elif "facebook" in canal or "marketplace" in canal:
        header = "🔔 NOVO LEAD MARKETPLACE"
    else:
        header = "🔔 NOVO LEAD SITE"

    msg = f"{header}\nNome: {nome}\nTelefone: {tel_display}\nImovel: {imovel} - Ref: {ref}"
    if wa_link:
        msg += f"\n\nChamar: {wa_link}"
    return msg


def _osascript(script: str) -> subprocess.CompletedProcess:
    return subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)


def send_to_group(message: str) -> bool:
    """Envia mensagem para o grupo via WhatsApp Desktop (nativo macOS).

    Fluxo validado 2026-08-04:
    1. Escreve mensagem em arquivo UTF-8 e copia via AppleScript (garante emojis e acentos)
    2. Ativa WhatsApp, busca grupo na caixa de pesquisa
    3. CGEvent left-click no resultado (y=197) — único método que abre grupos via busca
    4. Aguarda carregamento, re-ativa WhatsApp e envia
    """
    LCLICK = Path.home() / ".local/impar-automation/leads-planilha/lclick"
    MSG_TMP = Path("/tmp/wa_msg_utf8.txt")

    MSG_TMP.write_text(message, encoding='utf-8')
    clip_script = f'''
set f to open for access POSIX file "{MSG_TMP}"
set txt to read f as «class utf8»
close access f
set the clipboard to txt
'''
    r = subprocess.run(['osascript', '-e', clip_script], capture_output=True, text=True, timeout=10)
    if r.returncode != 0:
        log(f"ERROR clipboard: {r.stderr.strip()}")
        return False
    time.sleep(0.3)

    # Cmd+F abre busca global, Cmd+A limpa, digita grupo, espera 3s
    script_open = f'''
tell application "WhatsApp" to activate
delay 1.5
tell application "System Events" to tell process "WhatsApp"
    set frontmost to true
    key code 3 using {{command down}}
    delay 0.8
    keystroke "a" using command down
    delay 0.2
    keystroke "{GRUPO}"
    delay 3.0
end tell
'''
    subprocess.run(['osascript', '-e', script_open], capture_output=True, text=True, timeout=20)

    # CGEvent click no primeiro resultado (hardcoded: 245, 197)
    subprocess.run([str(LCLICK)], capture_output=True, timeout=5)
    time.sleep(4)
    script_send = '''
tell application "WhatsApp" to activate
delay 0.8
tell application "System Events" to tell process "WhatsApp"
    keystroke "a" using command down
    delay 0.3
    key code 51
    delay 0.3
    keystroke "v" using command down
    delay 1
    key code 36
end tell
'''
    result = subprocess.run(['osascript', '-e', script_send], capture_output=True, text=True, timeout=20)
    if result.returncode == 0:
        return True
    log(f"ERROR envio: {result.stderr.strip()}")
    return False


def main():
    if not CSV.exists():
        log(f"CSV não encontrado em {CSV} — abortando")
        sys.exit(0)

    state = load_state()
    prev = state.get("ultima_linha", 0)

    with open(CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)

    # Sai silenciosamente se nada mudou — zero tokens gastos
    if total <= prev:
        sys.exit(0)

    new_leads = [
        r for r in rows[prev:]
        if r.get("opt_out", "nao").strip().lower() == "nao"
        and r.get("status", "").strip().lower() != "encerrado"
    ]

    for lead in new_leads:
        msg = format_message(lead)
        ok = send_to_group(msg)
        status = "OK" if ok else "FALHOU"
        log(f"[{status}] {lead.get('nome','?')} | {lead.get('telefone','?')} | {lead.get('ref_imovel','?')}")

    save_state(total)


if __name__ == "__main__":
    main()
