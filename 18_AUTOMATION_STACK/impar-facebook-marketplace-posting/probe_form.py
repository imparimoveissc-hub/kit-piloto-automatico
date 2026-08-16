#!/usr/bin/env python3
"""Sonda o formulario de novo classificado e lista campos de texto reais."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-profile"
CREATE_URL = "https://www.facebook.com/marketplace/create/rental"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        str(PROFILE), headless=True, viewport={"width": 1280, "height": 900}
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(CREATE_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(6000)
    fields = page.evaluate(
        """() => Array.from(document.querySelectorAll('input, textarea, [role="textbox"], [role="combobox"]'))
            .filter(e => e.offsetParent !== null)
            .map(e => ({
                tag: e.tagName,
                type: e.type || '',
                aria: e.getAttribute('aria-label') || '',
                placeholder: e.getAttribute('placeholder') || '',
                labelledby: (e.getAttribute('aria-labelledby') || '')
                    .split(' ').map(id => (document.getElementById(id)||{}).innerText || '').join('|'),
                value: (e.value || e.innerText || '').slice(0, 40),
            }))"""
    )
    print(json.dumps(fields, ensure_ascii=False, indent=1))
    page.screenshot(path="/tmp/probe_form.png")
    ctx.close()
