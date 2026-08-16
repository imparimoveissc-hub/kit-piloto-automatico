#!/usr/bin/env python3
"""Driver generico do Facebook com o perfil persistente da automacao.

Acoes:
  --scan-inbox            lista threads do Marketplace inbox (JSON)
  --open-thread URL       abre uma conversa e extrai as ultimas mensagens
  --reply URL --message M abre a conversa e envia M no composer (acao real)
  --goto URL              apenas navega e tira screenshot
Sempre grava screenshot em --shot (default scratchpad).
Falha segura: se detectar tela de login/checkpoint, imprime SESSAO_INVALIDA e sai 2.
"""
import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

WORKSPACE = Path(
    "/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/"
    "Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/"
    "automacoes/facebook-marketplace"
)
PROFILE = WORKSPACE / "browser-profile"


def check_session(page):
    try:
        if page.locator("input[type='password']").count() > 0:
            return False
        url = page.url
        if "login" in url or "checkpoint" in url:
            return False
    except Exception:
        pass
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan-inbox", action="store_true")
    ap.add_argument("--open-thread")
    ap.add_argument("--reply")
    ap.add_argument("--message")
    ap.add_argument("--goto")
    ap.add_argument("--shot", default="/tmp/fb_driver.png")
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--wait", type=int, default=9000)
    args = ap.parse_args()

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=not args.headed,
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        out = {"ok": True}
        try:
            url = (
                "https://www.facebook.com/marketplace/inbox/"
                if args.scan_inbox
                else (args.open_thread or args.reply or args.goto)
            )
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(args.wait)

            if not check_session(page):
                print("SESSAO_INVALIDA")
                page.screenshot(path=args.shot)
                ctx.close()
                sys.exit(2)

            if args.scan_inbox:
                threads = page.eval_on_selector_all(
                    "a[href*='/marketplace/t/']",
                    """els => els.map(e => {
                        const row = e.closest('[role=\"row\"]') || e;
                        return {
                          href: e.href,
                          label: e.getAttribute('aria-label') || '',
                          text: (row.innerText || '').slice(0, 300),
                        };
                    })""",
                )
                out["threads"] = threads

            if args.open_thread:
                out["page_text"] = page.evaluate(
                    "() => (document.body.innerText || '').slice(0, 6000)"
                )

            if args.reply:
                if not args.message:
                    raise SystemExit("--reply exige --message")
                box = page.locator(
                    "div[role='textbox'][contenteditable='true']"
                ).last
                box.wait_for(state="visible", timeout=15000)
                box.click()
                box.type(args.message, delay=40)
                page.wait_for_timeout(700)
                page.keyboard.press("Enter")
                page.wait_for_timeout(2500)
                out["replied"] = True

            page.screenshot(path=args.shot)
        except SystemExit:
            raise
        except Exception as e:
            out = {"ok": False, "error": str(e)}
            try:
                page.screenshot(path=args.shot)
            except Exception:
                pass
        finally:
            ctx.close()
        print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
