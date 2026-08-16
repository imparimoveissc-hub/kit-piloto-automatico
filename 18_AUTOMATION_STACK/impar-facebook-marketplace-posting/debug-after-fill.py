#!/usr/bin/env python3
"""Debug após preencher o formulário"""

import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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

def only_digits(value):
    return re.sub(r"\D+", "", str(value or ""))

def load_listing(queue_path, index):
    listings = json.loads(queue_path.read_text(encoding="utf-8"))
    listing = listings[index - 1]
    return listing

def attach_photos(page, photo_paths):
    inputs = page.locator('input[type="file"]')
    count = inputs.count()
    if count == 0:
        print("ERRO: Nenhum input de foto encontrado")
        return False
    
    for i in range(count):
        current = inputs.nth(i)
        try:
            multiple = current.evaluate("el => el.multiple")
            if multiple:
                current.set_input_files(photo_paths)
                print(f"✓ Fotos anexadas ao input {i}")
                return True
        except Exception:
            continue
    
    inputs.nth(0).set_input_files(photo_paths)
    print(f"✓ Fotos anexadas ao input 0")
    return True

def fill_listing(page, listing):
    print("\n→ Preenchendo formulário...")
    page.goto(CREATE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    print(f"  Página carregada: {page.url}")
    
    attach_photos(page, listing["fotos"])
    page.wait_for_timeout(2500)
    print("  Fotos anexadas")

def debug_after_fill(page):
    print("\n" + "="*80)
    print("DEBUG: Estado APÓS preencher formulário")
    print("="*80)
    
    # Verificar se há erros visíveis
    error_msgs = page.query_selector_all('[role="alert"], .error, .errorMessage')
    if error_msgs:
        print(f"⚠️  Mensagens de erro encontradas: {len(error_msgs)}")
        for i, err in enumerate(error_msgs[:5]):
            try:
                print(f"  [{i}] {err.text_content()[:100]}")
            except:
                pass
    
    # Procurar por botões novamente
    print("\n🔍 Procurando por botões de publicação:")
    for text in ["Publicar", "Avancar", "Avançar", "Próximo", "Enviar"]:
        try:
            locator = page.get_by_text(text, exact=True)
            count = locator.count()
            print(f"  '{text}': {count} encontrado(s)", end="")
            if count > 0:
                try:
                    visible = locator.first.is_visible()
                    print(f" - visível: {visible}")
                except:
                    print()
            else:
                print()
        except Exception as e:
            print(f"  '{text}': erro - {e}")
    
    # Procurar com contains (não exact)
    print("\n🔍 Procurando com contains (não exact):")
    for text in ["publicar", "avançar", "próximo", "enviar", "avancar"]:
        try:
            locator = page.get_by_text(text)
            count = locator.count()
            if count > 0:
                print(f"  MATCH: '{text}' - {count} encontrado(s)")
        except:
            pass
    
    # Procurar todos os botões
    print("\n📋 Todos os botões:")
    buttons = page.query_selector_all('button')
    for i, btn in enumerate(buttons):
        try:
            text = btn.text_content().strip()[:80]
            visible = btn.is_visible()
            if text:
                print(f"  [{i}] '{text}' - visível: {visible}")
        except:
            pass

def main():
    listing = load_listing(DEFAULT_QUEUE, 1)
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(DEFAULT_PROFILE),
            headless=False,
            viewport={"width": 1280, "height": 900},
        )
        
        page = browser.new_page()
        try:
            fill_listing(page, listing)
            page.wait_for_timeout(2000)
            debug_after_fill(page)
            
            print("\n[Navegador aberto - inspeccione e feche quando terminar]")
            input("\nPressione ENTER...")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
