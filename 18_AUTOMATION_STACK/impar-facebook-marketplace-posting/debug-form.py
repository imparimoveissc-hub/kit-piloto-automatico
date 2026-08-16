#!/usr/bin/env python3
"""Debug script para diagnosticar o estado do formulário do Facebook Marketplace"""

import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUEUE = (
    ROOT
    / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/uploads-2026-07-08/anuncios-2026-07-08.json"
)
DEFAULT_PROFILE = (
    ROOT
    / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-profile"
)
CREATE_URL = "https://www.facebook.com/marketplace/create/rental"

def debug_page(page):
    """Imprime informações de debug sobre o estado da página"""
    print("\n" + "="*80)
    print("DEBUG: Estado da Página")
    print("="*80)
    
    # URL atual
    print(f"URL: {page.url}")
    
    # Verificar se está logado (procura por elemento que indica login)
    try:
        logged_in = page.query_selector('[aria-label*="Seu perfil"]')
        print(f"Logado: {logged_in is not None}")
    except:
        print("Logado: [não consegui verificar]")
    
    # Procura por botões com qualquer texto
    print("\nBotões encontrados na página:")
    buttons = page.query_selector_all('button')
    for i, btn in enumerate(buttons[:20]):  # Primeiros 20 botões
        try:
            text = btn.text_content().strip()[:100]
            visible = btn.is_visible()
            print(f"  [{i}] '{text}' - visível: {visible}")
        except:
            pass
    
    # Procura especificamente pelos textos de publicação
    print("\nProcurando por botões de publicação:")
    for text in ["Publicar", "Avancar", "Avançar", "publicar", "avançar"]:
        try:
            locator = page.get_by_text(text, exact=True)
            count = locator.count()
            print(f"  '{text}': {count} encontrado(s)")
            if count > 0:
                try:
                    visible = locator.first.is_visible()
                    print(f"    - visível: {visible}")
                except:
                    pass
        except Exception as e:
            print(f"  '{text}': erro - {e}")
    
    # Procura por elementos input (formulário)
    print("\nCampos de formulário encontrados:")
    inputs = page.query_selector_all('input, textarea, select')
    for i, inp in enumerate(inputs[:15]):  # Primeiros 15 campos
        try:
            inp_type = inp.get_attribute('type') or 'unknown'
            label = inp.get_attribute('aria-label') or inp.get_attribute('placeholder') or ''
            value = inp.input_value() if inp_type == 'text' else '[não-text]'
            print(f"  [{i}] {inp_type}: {label[:50]}")
        except:
            pass
    
    # Capturar o HTML para análise
    print("\n" + "="*80)
    print("HTML da página (últimos 2000 caracteres):")
    print("="*80)
    html = page.content()
    print(html[-2000:])

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(DEFAULT_PROFILE),
            headless=False,
            viewport={"width": 1280, "height": 900},
        )
        
        page = browser.new_page()
        page.goto(CREATE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        debug_page(page)
        
        print("\n[Navegador aberto - feche manualmente para continuar]")
        input("\nPressione ENTER depois de revisar o navegador...")
        
        browser.close()

if __name__ == "__main__":
    main()
