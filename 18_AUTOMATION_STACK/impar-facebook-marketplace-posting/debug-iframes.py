#!/usr/bin/env python3
"""Debug de iframes"""

import json
import re
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

def load_listing(queue_path, index):
    listings = json.loads(queue_path.read_text(encoding="utf-8"))
    return listings[index - 1]

def main():
    listing = load_listing(DEFAULT_QUEUE, 1)
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(DEFAULT_PROFILE),
            headless=False,
            viewport={"width": 1280, "height": 900},
        )
        
        page = browser.new_page()
        page.goto(CREATE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        
        print("\n" + "="*80)
        print("DEBUG: Estrutura de iframes")
        print("="*80)
        
        # Contar iframes
        iframes = page.query_selector_all('iframe')
        print(f"\nTotal de iframes na página: {len(iframes)}")
        
        # Procurar por "Avançar" de diferentes formas
        print("\n🔍 Procurando 'Avançar' de diferentes formas:")
        
        # Forma 1: page.get_by_text
        try:
            locator = page.get_by_text("Avançar", exact=True)
            print(f"  page.get_by_text('Avançar', exact=True): {locator.count()} encontrado(s)")
            if locator.count() > 0:
                print(f"    Bounding box: {locator.first.bounding_box()}")
                print(f"    Visível: {locator.first.is_visible()}")
                print(f"    Habilitado: {locator.first.is_enabled()}")
        except Exception as e:
            print(f"    Erro: {e}")
        
        # Forma 2: evaluate JavaScript
        try:
            result = page.evaluate("""
            () => {
                const buttons = document.querySelectorAll('button');
                const found = Array.from(buttons).filter(b => 
                    b.textContent.includes('Avançar') || 
                    b.textContent.includes('Publicar')
                );
                return {
                    total_buttons: buttons.length,
                    found_buttons: found.length,
                    buttons: found.map(b => ({
                        text: b.textContent.substring(0, 50),
                        visible: b.offsetParent !== null,
                        disabled: b.disabled,
                        classes: b.className
                    }))
                };
            }
            """)
            print(f"\n  Via JavaScript:")
            print(f"    Total de buttons: {result['total_buttons']}")
            print(f"    Botões com 'Avançar'/'Publicar': {result['found_buttons']}")
            for btn in result['buttons']:
                print(f"      - {btn}")
        except Exception as e:
            print(f"    Erro: {e}")
        
        print("\n[Navegador aberto - feche quando terminar]")
        input("ENTER...")
        browser.close()

if __name__ == "__main__":
    main()
