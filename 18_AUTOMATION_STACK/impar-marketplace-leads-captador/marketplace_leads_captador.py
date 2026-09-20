#!/usr/bin/env python3
"""
marketplace_leads_captador.py
Detecta novas conversas no Facebook Marketplace da Página Impar Imóveis,
adiciona o lead ao CSV de follow-up e notifica o grupo "Novos leads" no WhatsApp nativo macOS.

Custo: 0 tokens — usa osascript + lclick diretamente, sem chamar Claude.

Fonte no kit: 18_AUTOMATION_STACK/impar-marketplace-leads-captador/marketplace_leads_captador.py
Destino na máquina: ~/.local/impar-automation/marketplace-leads/marketplace_leads_captador.py
"""
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║              ⛔⛔  REGRAS SUPREMAS — LER ANTES DE TUDO  ⛔⛔                ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  REGRA 1 — SOMENTE MARKETPLACE                                              ║
# ║  Este script processa EXCLUSIVAMENTE conversas com link /marketplace/item/  ║
# ║  nos attachments das mensagens. Conversas sem esse link são contatos        ║
# ║  pessoais ou de página — IGNORAR: log [IGNORADO], processados.add(conv_id),║
# ║  continue. Nunca notificar nem gravar CSV fora do Marketplace.              ║
# ║  Guard: extrair_link_marketplace(msgs) → se vazio → IGNORAR.               ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  REGRA 2 — NUNCA RESPONDER "FACEBOOK MARKETPLACE ASSISTANT"                 ║
# ║  Qualquer conversa cujo nome esteja em NOMES_BLOQUEADOS é um bot do         ║
# ║  Facebook — não é um lead real. NUNCA processar, notificar ou gravar.       ║
# ║  Guard: nome.strip().lower() in NOMES_BLOQUEADOS → verificar ANTES da       ║
# ║  extração de mensagens e ANTES do guard de Marketplace.                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
import csv
import json
import re
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ── Configuração ───────────────────────────────────────────────────────────────
# ATENÇÃO: Python 3.9 (CommandLineTools) NÃO tem acesso a iCloud Drive em LaunchAgents.
# Todos os caminhos usados pelo Python são locais. O wrapper run_captador.sh cuida
# da sincronização iCloud ↔ local via cp (bash tem acesso).
STATE_DIR  = Path("/Users/usuario/.local/impar-automation/marketplace-leads")
ENV_FILE   = STATE_DIR / ".env"          # copiado do iCloud pelo wrapper antes da execução
CSV_PATH   = STATE_DIR / "leads-marketplace.csv"  # sincronizado de/para iCloud pelo wrapper
LOG        = STATE_DIR / "captador.log"
CHECKPOINT = STATE_DIR / "checkpoint.json"
LCLICK     = STATE_DIR / "lclick"
MSG_TMP    = Path("/tmp/wa_msg_utf8.txt")

ICLOUD_CSV = Path("/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv")

GRUPO      = "Novos leads"

# ⛔ Nomes que NUNCA devem ser processados como leads.
# "Facebook Marketplace Assistant" é um bot do Facebook — não é um lead real.
# Conversas pessoais do Jonata são bloqueadas pelo guard de link /marketplace/item/.
NOMES_BLOQUEADOS = {
    "facebook marketplace assistant",
    "marketplace assistant",
    "facebook assistant",
    "assistant",
}

# ⛔ Assinaturas de conteúdo do "Facebook Marketplace Assistant" (bot do Facebook).
# Guard de última linha caso o nome venha diferente do esperado.
FRASES_BOT_FACEBOOK = (
    "nao podemos responder a mensagens agora",
    "acesse a nossa central de ajuda",
    "seu classificado nao foi renovado",
    "gostaria de renova-lo agora",
    "renovar classificado",
    "renewed your listing",
    "renew your listing again after",
)

def _norm_txt(v: str) -> str:
    v = unicodedata.normalize("NFKD", str(v or ""))
    v = "".join(c for c in v if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", v.lower()).strip()

def is_nome_bloqueado(nome: str) -> bool:
    n = (nome or "").strip().lower()
    if not n:
        return False
    if n in NOMES_BLOQUEADOS:
        return True
    return any(n in bl for bl in NOMES_BLOQUEADOS)

def is_conteudo_bot_facebook(mensagens: list) -> bool:
    """True se qualquer mensagem contém assinatura do Facebook Marketplace Assistant."""
    for m in mensagens or []:
        t = _norm_txt(m.get("message", "") if isinstance(m, dict) else m)
        if any(f in t for f in FRASES_BOT_FACEBOOK):
            return True
    return False

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
    STATE_DIR.mkdir(parents=True, exist_ok=True)
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
    # Prioriza campo estruturado "Phone number:" (formulário FB)
    m = re.search(r"Phone number[:\s]+([^\n]+)", texto, re.IGNORECASE)
    raw = m.group(1).strip() if m else texto
    digitos = re.sub(r"[^\d]", "", raw)
    # Aceita DDD com ou sem 0 inicial, 9º dígito opcional, 7-8 dígitos finais
    matches = re.findall(r"(?:55)?0?[1-9]\d9?\d{7,8}", digitos)
    if matches:
        tel = re.sub(r"[^\d]", "", matches[0])
        if len(tel) in (12, 13) and tel.startswith("0"):
            tel = tel[1:]
        return tel if tel.startswith("55") else "55" + tel
    return ""

def extrair_dados_lead(mensagens: list, page_id: str) -> dict:
    msgs_lead = [m for m in reversed(mensagens) if m.get("from", {}).get("id") != page_id]
    # Coleta texto das mensagens E dos campos description/title dos attachments.
    # Quando o lead envia contato pelo formulário FB, o telefone chega em
    # attachments[].description — não no campo message.
    partes = []
    for msg in msgs_lead:
        if msg.get("message"):
            partes.append(msg["message"])
        for att in msg.get("attachments", {}).get("data", []):
            if att.get("description"):
                partes.append(att["description"])
            if att.get("title") and "Phone" in att.get("title", ""):
                partes.append(att["title"])
    texto = "\n".join(partes)
    telefone = extrair_telefone(texto)
    m_email = re.search(r"Email[:\s]+([^\n]+)", texto, re.IGNORECASE)
    email = m_email.group(1).strip() if m_email else ""
    return {"telefone": telefone, "email": email}

# ── Facebook Graph API ─────────────────────────────────────────────────────────
def get_conversations(page_id: str, token: str, limit: int = 50) -> list:
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
            params={"fields": "message,from,created_time,attachments{title,description,url,type}", "limit": limit, "access_token": token},
            timeout=15,
        )
        r.raise_for_status()
        return r.json().get("data", [])
    except Exception:
        return []

def extrair_link_marketplace(mensagens: list) -> str:
    """Extrai URL real do item Marketplace dos attachments das mensagens."""
    for msg in mensagens:
        for att in msg.get("attachments", {}).get("data", []):
            url = att.get("url", "")
            if "/marketplace/item/" in url:
                return url
    return ""

def extrair_descricao_imovel(mensagens: list) -> str:
    """Extrai título do anúncio Marketplace dos attachments."""
    for msg in mensagens:
        for att in msg.get("attachments", {}).get("data", []):
            if "/marketplace/item/" in att.get("url", ""):
                title = att.get("title", "").strip()
                if title:
                    return title
    return "Marketplace FB"

# ── Formato de mensagem — formato validado 2026-08-10 ─────────────────────────
import urllib.parse as _urlparse

def _build_wa_link(tel_clean: str, nome: str, link_imovel: str) -> str:
    primeiro_nome = nome.split()[0] if nome else "você"
    if link_imovel:
        d0 = (
            f"Oi {primeiro_nome}, tudo bem? Aqui é a Impar Imóveis!\n"
            f"Vi que você entrou em contato pelo Marketplace sobre este imóvel:\n"
            f"{link_imovel}"
        )
    else:
        d0 = (
            f"Oi {primeiro_nome}, tudo bem? Aqui é a Impar Imóveis!\n"
            f"Vi que você demonstrou interesse em um dos nossos imóveis."
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

def _telegram_send(mensagem: str) -> bool:
    import json as _json, urllib.request as _req, os as _os
    cfg_path = Path.home() / ".impar-n8n-core/state/config.json"
    cfg      = _json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    token    = _os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("telegram_bot_token", "")
    chat_id  = _os.environ.get("TELEGRAM_CHAT_ID")   or cfg.get("telegram_chat_id", "")
    if not token or not chat_id:
        log("ERRO: telegram_bot_token ou telegram_chat_id não configurado")
        return False
    url     = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = _json.dumps({"chat_id": chat_id, "text": mensagem}).encode()
    req     = _req.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with _req.urlopen(req, timeout=15) as resp:
            return _json.loads(resp.read()).get("ok", False)
    except Exception as e:
        log(f"Telegram erro: {e}")
        return False


def send_to_group(message: str) -> bool:
    ok = _telegram_send(message)
    if ok:
        log("Notificação enviada via Telegram")
    else:
        log("ERRO ao enviar notificação via Telegram")
    return ok

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

        # ⛔ Guard nome bloqueado: bots do Facebook e variantes do Marketplace Assistant.
        if is_nome_bloqueado(nome):
            log(f"[IGNORADO] {nome} | {conv_id} — nome bloqueado (bot/assistant do Facebook)")
            processados.add(conv_id)
            continue

        # Extrai telefone, email, URL real do item e descrição do anúncio
        msgs      = get_messages(conv_id, token)

        # ⛔ Guard de conteúdo: mesmo com nome diferente, se o texto tem assinatura
        # do Facebook Marketplace Assistant → é o bot, nunca processar.
        if is_conteudo_bot_facebook(msgs):
            log(f"[IGNORADO] {nome} | {conv_id} — conteúdo de bot do Facebook (Marketplace Assistant)")
            processados.add(conv_id)
            continue
        dados     = extrair_dados_lead(msgs, page_id)
        telefone  = dados.get("telefone", "")
        email     = dados.get("email", "")
        link_item = extrair_link_marketplace(msgs)
        descricao = extrair_descricao_imovel(msgs)

        # ⛔ REGRA: processar SOMENTE leads do Marketplace.
        # Conversas pessoais/de páginas sem link /marketplace/item/ são ignoradas.
        if not link_item:
            log(f"[IGNORADO] {nome} | {conv_id} — sem link /marketplace/item/ (conversa pessoal ou não-marketplace)")
            processados.add(conv_id)
            continue

        num_conv   = conv_id.replace("t_", "")
        link_conv  = f"https://www.facebook.com/messages/t/{num_conv}"
        link_final = link_item
        data_hoje  = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        lead_row = {
            "telefone":             telefone,
            "nome":                 nome,
            "link_imovel":          link_final,
            "ref_imovel":           link_final,
            "descricao_imovel":     descricao,
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

        # ⛔ Sem telefone: aguarda o lead enviar → não marca como processado, retry no próximo ciclo.
        # Após SEM_TEL_ALERTA_CICLOS ciclos sem telefone, envia alerta para verificação manual.
        SEM_TEL_ALERTA_CICLOS = 6
        if not telefone:
            sem_tel_counts = checkpoint.setdefault("sem_tel_counts", {})
            sem_tel_counts[conv_id] = sem_tel_counts.get(conv_id, 0) + 1
            count = sem_tel_counts[conv_id]
            log(f"[SEM_TEL] {nome} | {conv_id} — sem telefone ainda (ciclo {count}), aguardando próxima varredura")
            if count == SEM_TEL_ALERTA_CICLOS:
                alerta = (
                    f"⚠️ LEAD SEM TELEFONE\n"
                    f"👤 Nome: {nome}\n"
                    f"🏠 Imóvel: {descricao}\n"
                    f"🔗 Conversa: https://www.facebook.com/messages/t/{conv_id.replace('t_','')}\n"
                    f"Verificar manualmente — {SEM_TEL_ALERTA_CICLOS} ciclos sem telefone."
                )
                _telegram_send(alerta)
                log(f"[ALERTA_SEM_TEL] {nome} | {conv_id} — alerta enviado após {count} ciclos")
            continue

        append_lead_to_csv(lead_row)
        log(f"[ADICIONADO] {nome} | tel: {telefone} | {conv_id}")

        msg = format_message(lead_row)
        ok  = send_to_group(msg)
        log(f"[TELEGRAM {'OK' if ok else 'FALHOU'}] {nome}")

        processados.add(conv_id)
        novos += 1

    checkpoint["processados"]      = list(processados)
    checkpoint["ultima_execucao"]  = datetime.now().isoformat(timespec="seconds")
    checkpoint["total_capturados"] = checkpoint.get("total_capturados", 0) + novos
    save_checkpoint(checkpoint)

    if novos == 0:
        sys.exit(0)

    log(f"[RESUMO] {novos} lead(s) processado(s)")

if __name__ == "__main__":
    main()
