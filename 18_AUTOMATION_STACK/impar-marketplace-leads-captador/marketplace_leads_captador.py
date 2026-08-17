#!/usr/bin/env python3
"""
marketplace_leads_captador.py
Detecta novas conversas no Facebook Marketplace da Página Impar Imóveis,
adiciona o lead ao CSV de follow-up e notifica o grupo "NOVOS LEADS" no WhatsApp nativo macOS.

Custo: 0 tokens — usa osascript + lclick diretamente, sem chamar Claude.

Fonte no kit: 18_AUTOMATION_STACK/impar-marketplace-leads-captador/marketplace_leads_captador.py
Destino na máquina: ~/.local/impar-automation/marketplace-leads/marketplace_leads_captador.py
"""
import csv
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ── Configuração ───────────────────────────────────────────────────────────────
KIT_DIR  = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
ENV_FILE = KIT_DIR / "18_AUTOMATION_STACK/facebook-mcp/.env"
CSV_PATH = KIT_DIR / "05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv"
LOG_DIR  = KIT_DIR / "07_LOGS"

STATE_DIR  = Path.home() / ".local/impar-automation/marketplace-leads"
CHECKPOINT = STATE_DIR / "checkpoint.json"
LOG        = LOG_DIR / "marketplace-leads-captador.log"
LCLICK     = STATE_DIR / "lclick"
MSG_TMP    = Path("/tmp/wa_msg_utf8.txt")

GRUPO      = "NOVOS LEADS"
FB_VERSION = "v20.0"

# ── Helpers básicos ────────────────────────────────────────────────────────────
def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def log(msg: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return json.loads(CHECKPOINT.read_text())
    return {"processados": []}

def save_checkpoint(data: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT.write_text(json.dumps(data, ensure_ascii=False, indent=2))

# ── Extração de dados do formulário FB ────────────────────────────────────────
def extrair_telefone(texto: str) -> str:
    m = re.search(r"Phone number[:\s]+([^\n]+)", texto, re.IGNORECASE)
    raw = m.group(1).strip() if m else texto
    digitos = re.sub(r"[^\d]", "", raw)
    matches = re.findall(r"(?:55)?[1-9]{2}9?\d{7,8}", digitos)
    if matches:
        tel = matches[0]
        return tel if tel.startswith("55") else "55" + tel
    return ""

def extrair_dados_lead(mensagens: list, page_id: str) -> dict:
    msgs_lead = [m for m in reversed(mensagens) if m.get("from", {}).get("id") != page_id]
    texto = "\n".join(m.get("message", "") for m in msgs_lead)
    telefone = extrair_telefone(texto)
    m_email = re.search(r"Email[:\s]+([^\n]+)", texto, re.IGNORECASE)
    email = m_email.group(1).strip() if m_email else ""
    return {"telefone": telefone, "email": email}

# ── Facebook Graph API ─────────────────────────────────────────────────────────
def get_conversations(page_id: str, token: str, limit: int = 25) -> list:
    r = httpx.get(
        f"https://graph.facebook.com/{FB_VERSION}/{page_id}/conversations",
        params={"fields": "id,participants,updated_time,snippet", "limit": limit, "access_token": token},
        timeout=15,
    )
    r.raise_for_status()
    return r.json().get("data", [])

def get_messages(conv_id: str, token: str, limit: int = 25) -> list:
    try:
        r = httpx.get(
            f"https://graph.facebook.com/{FB_VERSION}/{conv_id}/messages",
            params={"fields": "message,from,created_time", "limit": limit, "access_token": token},
            timeout=15,
        )
        r.raise_for_status()
        return r.json().get("data", [])
    except Exception:
        return []

# ── Formato de mensagem — formato validado 2026-08-10 ─────────────────────────
import urllib.parse as _urlparse

def _build_wa_link(tel_clean: str, nome: str, link_imovel: str) -> str:
    primeiro_nome = nome.split()[0] if nome else "você"
    if link_imovel:
        d0 = (
            f"Oi {primeiro_nome}, tudo bem?\n"
            f"Somos da Impar Imóveis. Vi que você demonstrou interesse no nosso anúncio: {link_imovel}\n\n"
            f"Você gostaria de tirar mais dúvidas ou agendar uma visita?"
        )
    else:
        d0 = (
            f"Oi {primeiro_nome}, tudo bem?\n"
            f"Somos da Impar Imóveis e ficamos sabendo do seu interesse em um dos nossos imóveis. "
            f"Você gostaria de tirar mais dúvidas ou agendar uma visita?"
        )
    return f"https://wa.me/{tel_clean}?text={_urlparse.quote(d0)}"

def format_message(lead: dict) -> str:
    canal  = lead.get("canal_entrada", "marketplace").lower()
    nome   = lead.get("nome", "?")
    tel    = lead.get("telefone", "")
    imovel = lead.get("descricao_imovel", "Marketplace FB")
    link   = lead.get("link_imovel", "")

    tel_clean = "".join(c for c in tel if c.isdigit())
    if tel_clean and not tel_clean.startswith("55"):
        tel_clean = "55" + tel_clean
    # Formata +55 47 99999-9999
    if len(tel_clean) >= 12:
        tel_display = f"+{tel_clean[:2]} {tel_clean[2:4]} {tel_clean[4:9]}-{tel_clean[9:]}"
    elif tel_clean:
        tel_display = f"+{tel_clean}"
    else:
        tel_display = "não informado"

    if "chaves" in canal:
        header = "🔔 NOVO LEAD CHAVES NA MÃO"
    elif "facebook" in canal or "marketplace" in canal:
        header = "🔔 NOVO LEAD FACEBOOK MARKETPLACE"
    else:
        header = "🔔 NOVO LEAD"

    msg = (
        f"{header}\n"
        f"👤 Nome: {nome}\n"
        f"📞 Telefone: {tel_display}\n"
        f"🏠 Imóvel: {imovel}"
    )
    if link:
        msg += f"\n🔗 Anúncio: {link}"

    if tel_clean:
        wa_link = _build_wa_link(tel_clean, nome, link)
        msg += f"\n\n👉 Toque para chamar:\n{wa_link}"

    return msg

# ── Envio WhatsApp — cópia exata do leads_watcher.py ──────────────────────────
def send_to_group(message: str) -> bool:
    MSG_TMP.write_text(message, encoding="utf-8")
    clip_script = f'''
set f to open for access POSIX file "{MSG_TMP}"
set txt to read f as «class utf8»
close access f
set the clipboard to txt
'''
    r = subprocess.run(["osascript", "-e", clip_script], capture_output=True, text=True, timeout=10)
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
    subprocess.run(["osascript", "-e", script_open], capture_output=True, text=True, timeout=20)

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
    result = subprocess.run(["osascript", "-e", script_send], capture_output=True, text=True, timeout=20)
    if result.returncode == 0:
        return True
    log(f"ERROR envio: {result.stderr.strip()}")
    return False

# ── CSV ────────────────────────────────────────────────────────────────────────
def append_lead_to_csv(lead: dict):
    fieldnames = [
        "telefone", "nome", "link_imovel", "ref_imovel", "descricao_imovel",
        "canal_entrada", "data_entrada", "ultimo_passo_enviado", "data_ultimo_passo",
        "proximo_passo", "data_proximo_passo", "respondeu_whatsapp", "opt_out",
        "status", "observacao",
    ]
    escrever_cabecalho = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if escrever_cabecalho:
            writer.writeheader()
        writer.writerow(lead)

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    env     = load_env()
    token   = env.get("FB_PAGE_TOKEN")
    page_id = env.get("FB_PAGE_ID")

    if not token or not page_id:
        log("ERRO: FB_PAGE_TOKEN ou FB_PAGE_ID não encontrados no .env")
        sys.exit(1)

    checkpoint  = load_checkpoint()
    processados = set(checkpoint.get("processados", []))

    try:
        conversas = get_conversations(page_id, token)
    except Exception as e:
        log(f"ERRO ao buscar conversas: {e}")
        sys.exit(1)

    novos = 0
    for conv in conversas:
        conv_id = conv.get("id", "")
        if conv_id in processados:
            continue

        # Participante que não é a página
        nome = "Desconhecido"
        for p in conv.get("participants", {}).get("data", []):
            if p.get("id") != page_id:
                nome = p.get("name", "Desconhecido")
                break

        # Extrai telefone e email do formulário
        msgs    = get_messages(conv_id, token)
        dados   = extrair_dados_lead(msgs, page_id)
        telefone = dados.get("telefone", "")
        email    = dados.get("email", "")

        # Link da conversa como referência do imóvel
        num_conv   = conv_id.replace("t_", "")
        link_conv  = f"https://www.facebook.com/messages/t/{num_conv}"
        data_hoje  = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        lead_row = {
            "telefone":             telefone,
            "nome":                 nome,
            "link_imovel":          link_conv,
            "ref_imovel":           link_conv,
            "descricao_imovel":     "Marketplace FB",
            "canal_entrada":        "marketplace",
            "data_entrada":         data_hoje,
            "ultimo_passo_enviado": "D0",
            "data_ultimo_passo":    data_hoje,
            "proximo_passo":        "D1",
            "data_proximo_passo":   "-",
            "respondeu_whatsapp":   "nao",
            "opt_out":              "nao",
            "status":               "novo",
            "observacao":           f"conv_id: {conv_id}" + (f" | email: {email}" if email else ""),
        }

        append_lead_to_csv(lead_row)
        log(f"[ADICIONADO] {nome} | tel: {telefone or 'vazio'} | {conv_id}")

        msg = format_message(lead_row)
        ok  = send_to_group(msg)
        log(f"[WA {'OK' if ok else 'FALHOU'}] {nome}")

        processados.add(conv_id)
        novos += 1

    if novos == 0:
        sys.exit(0)

    checkpoint["processados"]      = list(processados)
    checkpoint["ultima_execucao"]  = datetime.now().isoformat(timespec="seconds")
    checkpoint["total_capturados"] = checkpoint.get("total_capturados", 0) + novos
    save_checkpoint(checkpoint)
    log(f"[RESUMO] {novos} lead(s) processado(s)")

if __name__ == "__main__":
    main()
