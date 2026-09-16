#!/usr/bin/env python3
"""
notificar_lead_whatsapp.py — envia notificação de lead via Telegram.
(Interface mantida idêntica para compatibilidade com todos os chamadores.)
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG = Path.home() / ".impar-n8n-core/state/config.json"
ACCOUNTS_CONFIG = Path.home() / ".local/impar-automation/accounts.json"
LOG    = Path.home() / ".local/impar-automation/logs/notificar-lead.log"


def _cfg() -> dict:
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
    except Exception:
        return {}


def _accounts_cfg() -> dict:
    try:
        return json.loads(ACCOUNTS_CONFIG.read_text(encoding="utf-8")) if ACCOUNTS_CONFIG.exists() else {}
    except Exception:
        return {}


def _log(msg: str):
    from datetime import datetime
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")


def _account(account_id: str) -> dict:
    if not account_id:
        return {}
    for account in _accounts_cfg().get("accounts", []):
        if account.get("id") == account_id:
            return account
    return {}


def _read_token_file(path_value: str) -> str:
    if not path_value:
        return ""
    path = Path(path_value.replace("~", str(Path.home())))
    try:
        return path.read_text(encoding="utf-8").strip() if path.exists() else ""
    except Exception:
        return ""


def telegram_credentials(account_id: str = "") -> tuple[str, str]:
    cfg = _cfg()
    accounts_cfg = _accounts_cfg()
    account = _account(account_id)

    token = (
        os.environ.get("TELEGRAM_BOT_TOKEN")
        or _read_token_file(account.get("telegram_token_file", ""))
        or _read_token_file(accounts_cfg.get("shared", {}).get("telegram_token_file", ""))
        or cfg.get("telegram_bot_token", "")
    )
    if account_id:
        # Com multiconta, o perfil precisa mandar no Telegram configurado dele.
        # TELEGRAM_CHAT_ID do ambiente fica apenas como fallback legado.
        chat_id = (
            str(account.get("telegram_chat_id", "") or "")
            or str(cfg.get("telegram_chat_id", "") or "")
            or os.environ.get("TELEGRAM_CHAT_ID", "")
        )
    else:
        chat_id = (
            os.environ.get("TELEGRAM_CHAT_ID")
            or str(cfg.get("telegram_chat_id", "") or "")
        )
    return token, chat_id


def enviar_telegram(mensagem: str, account_id: str = "") -> bool:
    token, chat_id = telegram_credentials(account_id)
    if not token or not chat_id:
        _log(f"ERRO: telegram_bot_token ou telegram_chat_id não configurado (account_id={account_id or 'default'})")
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


def _extract_url(text: str) -> str:
    """Retorna text se for URL, extrai a primeira URL encontrada, ou string vazia."""
    if not text:
        return ""
    text = text.strip()
    if text.startswith("https://") or text.startswith("http://"):
        return text
    m = re.search(r'https?://\S+', text)
    return m.group(0) if m else ""


def build_wa_link(digits: str, nome: str, link_imovel: str, origem: str) -> str:
    nome_first = nome.split()[0] if nome else "você"
    if link_imovel:
        texto = (
            f"Oi {nome_first}, tudo bem? Aqui é a Impar Imóveis!\n"
            f"Vi que você entrou em contato pelo Marketplace sobre este imóvel:\n"
            f"{link_imovel}\n\n"
            f"Gostaria de retirar dúvidas?"
        )
    else:
        texto = (
            f"Oi {nome_first}, tudo bem? Aqui é a Impar Imóveis!\n"
            f"Vi que você demonstrou interesse em um dos nossos imóveis."
        )
    return f"https://wa.me/{digits}?text={urllib.parse.quote(texto)}" if digits else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nome",          default="Lead")
    parser.add_argument("--telefone",      default="")
    parser.add_argument("--resumo",        default="")
    parser.add_argument("--link-imovel",   default="")
    parser.add_argument("--origem",        default="marketplace")
    parser.add_argument("--account-id",    "--perfil", dest="account_id", default="")
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

    link_imovel_url = _extract_url(args.link_imovel)
    wa_link = build_wa_link(tel, args.nome, link_imovel_url, args.origem)
    link_display = link_imovel_url or "Link indisponível"
    resumo_display = args.resumo or "N/A"

    msg = (
        f"{header}\n"
        f"👤 Nome: {args.nome}\n"
        f"📞 Telefone: {tel_display}\n"
        f"🏠 Imóvel: {resumo_display}\n"
        f"🔗 Anúncio: {link_display}"
        + (f"\n\n👉 Toque para chamar:\n{wa_link}" if wa_link else "")
    )

    ok = enviar_telegram(msg, args.account_id)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
