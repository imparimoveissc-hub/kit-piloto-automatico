#!/usr/bin/env python3
"""Sessao interativa persistente do Facebook (perfil da automacao).

Le comandos JSON de CMD_FILE quando o campo "seq" muda, executa e grava
RESULT_FILE + screenshot. Comandos:
  {"seq":1,"op":"goto","url":"..."}
  {"seq":2,"op":"click","x":100,"y":200}
  {"seq":3,"op":"type","text":"ola"}
  {"seq":4,"op":"key","key":"Enter"}
  {"seq":5,"op":"eval","js":"() => document.title"}
  {"seq":6,"op":"shot"}
  {"seq":7,"op":"scroll","dy":600}
  {"seq":8,"op":"exit"}
"""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
SCRATCH = Path(
    "/private/tmp/claude-501/-Users-usuario-Library-Mobile-Documents-"
    "com-apple-CloudDocs-Kit-Piloto-Automatico-V30-DISTRIB/"
    "3a039641-cbed-49bd-8dae-6bd1254db231/scratchpad"
)
CMD_FILE = SCRATCH / "fb_cmd.json"
RESULT_FILE = SCRATCH / "fb_result.json"
SHOT = SCRATCH / "fb_shot.png"
PROFILE = Path(
    "/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/"
    "Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/"
    "automacoes/facebook-marketplace/browser-profile"
)


def write_result(seq, data):
    RESULT_FILE.write_text(
        json.dumps({"seq": seq, **data}, ensure_ascii=False), encoding="utf-8"
    )


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    last_seq = 0
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE), headless=True, viewport={"width": 1280, "height": 900}
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        write_result(0, {"ok": True, "status": "ready"})
        while True:
            time.sleep(0.5)
            try:
                cmd = json.loads(CMD_FILE.read_text(encoding="utf-8"))
            except Exception:
                continue
            seq = cmd.get("seq", 0)
            if seq <= last_seq:
                continue
            last_seq = seq
            op = cmd.get("op")
            out = {"ok": True, "op": op}
            try:
                if op == "goto":
                    page.goto(cmd["url"], wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(cmd.get("wait", 6000))
                elif op == "click":
                    page.mouse.click(cmd["x"], cmd["y"])
                    page.wait_for_timeout(cmd.get("wait", 2500))
                elif op == "type":
                    page.keyboard.type(cmd["text"], delay=35)
                    page.wait_for_timeout(500)
                elif op == "key":
                    page.keyboard.press(cmd["key"])
                    page.wait_for_timeout(cmd.get("wait", 1500))
                elif op == "eval":
                    out["value"] = page.evaluate(cmd["js"])
                elif op == "scroll":
                    page.mouse.wheel(0, cmd.get("dy", 600))
                    page.wait_for_timeout(1200)
                elif op == "shot":
                    pass
                elif op == "exit":
                    page.screenshot(path=str(SHOT))
                    write_result(seq, {"ok": True, "op": "exit"})
                    break
                else:
                    out = {"ok": False, "error": f"op desconhecida: {op}"}
                page.screenshot(path=str(SHOT))
            except Exception as e:
                out = {"ok": False, "op": op, "error": str(e)}
                try:
                    page.screenshot(path=str(SHOT))
                except Exception:
                    pass
            write_result(seq, out)
        ctx.close()


if __name__ == "__main__":
    main()
