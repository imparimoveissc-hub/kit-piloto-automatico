#!/usr/bin/env python3
"""
notificar_lead_whatsapp.py — envia notificação de lead via Telegram.
(Interface mantida idêntica para compatibilidade com todos os chamadores.)
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG = Path.home() / ".impar-n8n-core/state/config.json"
LOG    = Path.home() / ".local/impar-automation/logs/notificar-lead.log"


def _cfg() -> dict:
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    except Exception:
        return {}


def _log(msg: str):
    from datetime import datetime
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")


def enviar_telegram(mensagem: str) -> bool:
    cfg     = _cfg()
    token   = os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("telegram_bot_token", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")   or cfg.get("telegram_chat_id", "")
    if not token or not chat_id:
        _log("ERRO: telegram_bot_token ou telegram_chat_id não configurado")
        print("ERRO: telegram_bot_token ou telegram_chat_id não configurado.", file=sys.stderr)
        return False
    url     = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": mensagem}).encode()
    req     = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            ok = result.get("ok", False)
            if ok:
                _log(f"Telegram OK: {mensagem[:80]}")
            else:
                _log(f"Telegram ERRO: {result}")
            return ok
    except Exception as e:
        _log(f"Telegram exceção: {e}")
        print(f"ERRO Telegram: {e}", file=sys.stderr)
        return False


def build_wa_link(digits: str, nome: str, link_imovel: str, origem: str) -> str:
    nome_first = nome.split()[0] if nome else "você"
    if link_imovel:
        texto = (
            f"Oi {nome_first}, tudo bem? Aqui é a Impar Imóveis!\n"
            f"Vi que você entrou em contato pelo Marketplace sobre este imóvel:\n"
            f"{link_imovel}\n\n"
            f"Gostaria de retirar mais duvidas?"
        )
    else:
        texto = (
            f"Oi {nome_first}, tudo bem? Aqui é a Impar Imóveis!\n"
            f"Vi que você demonstrou interesse em um dos nossos imóveis.\n\n"
            f"Gostaria de retirar mais duvidas?"
        )
    return f"https://wa.me/{digits}?text={urllib.parse.quote(texto)}" if digits else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nome",          default="Lead")
    parser.add_argument("--telefone",      default="")
    parser.add_argument("--resumo",        default="")
    parser.add_argument("--link-imovel",   default="")
    parser.add_argument("--origem",        default="marketplace")
    # Compatibilidade com chamadores antigos que usam --from-planilha
    parser.add_argument("--from-planilha", action="store_true")
    args = parser.parse_args()

    if args.from_planilha:
        _log("--from-planilha: modo legado, nenhum lead novo a notificar via planilha neste ciclo")
        sys.exit(0)

    tel = "".join(c for c in args.telefone if c.isdigit()) if args.telefone else ""
    if tel and not tel.startswith("55"):
        tel = "55" + tel

    if len(tel) == 13:
        tel_display = f"+{tel[:2]} {tel[2:4]} {tel[4:9]}-{tel[9:]}"
    elif len(tel) == 12:
        tel_display = f"+{tel[:2]} {tel[2:4]} {tel[4:8]}-{tel[8:]}"
    else:
        tel_display = f"+{tel}" if tel else "Não informado"

    origem = args.origem.lower()
    if "chaves" in origem:
        header = "🔔 NOVO LEAD CHAVES NA MÃO"
    elif "facebook" in origem or "marketplace" in origem:
        header = "🔔 NOVO LEAD FACEBOOK MARKETPLACE"
    else:
        header = "🔔 NOVO LEAD"

    wa_link = build_wa_link(tel, args.nome, args.link_imovel, args.origem)
    link_display = args.link_imovel or "N/A"
    resumo_display = args.resumo or "N/A"

    msg = (
        f"{header}\n"
        f"👤 Nome: {args.nome}\n"
        f"📞 Telefone: {tel_display}\n"
        f"🏠 Imóvel: {resumo_display}\n"
        f"🔗 Anúncio: {link_display}"
        + (f"\n\n👉 Toque para chamar:\n{wa_link}" if wa_link else "")
    )

    ok = enviar_telegram(msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
