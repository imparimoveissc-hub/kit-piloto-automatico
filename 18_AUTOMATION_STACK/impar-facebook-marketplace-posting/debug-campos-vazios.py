#!/usr/bin/env python3
"""Encontra campos vazios que estão impedindo a publicação"""

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

def only_digits(value):
    return re.sub(r"\D+", "", str(value or ""))

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
        
        # Fazer o mesmo que fill_listing faz
        inputs = page.locator('input[type="file"]')
        if inputs.count() > 0:
            for i in range(inputs.count()):
                current = inputs.nth(i)
                try:
                    multiple = current.evaluate("el => el.multiple")
                    if multiple:
                        current.set_input_files(listing["fotos"])
                        break
                except:
                    if i == 0:
                        inputs.nth(0).set_input_files(listing["fotos"])
                        break
        
        page.wait_for_timeout(2000)
        
        print("\n" + "="*80)
        print("DEBUG: Campos do formulário")
        print("="*80)
        
        # Listar todos os inputs e seus valores
        result = page.evaluate("""
        () => {
            const inputs = document.querySelectorAll('input[type="text"], textarea, input[type="number"]');
            return Array.from(inputs).map(inp => ({
                type: inp.type,
                name: inp.name,
                placeholder: inp.placeholder,
                aria_label: inp.getAttribute('aria-label'),
                value: inp.value,
                required: inp.required
            }));
        }
        """)
        
        print(f"\nTotal de inputs/textareas: {len(result)}")
        for i, inp in enumerate(result):
            status = "❌ VAZIO" if not inp['value'] else "✓ PREENCHIDO"
            print(f"  [{i}] {status} - {inp['aria_label'] or inp['placeholder'] or inp['name']}")
            if inp['value']:
                print(f"       Valor: {inp['value'][:60]}")
            if inp['required']:
                print(f"       ⚠️  OBRIGATÓRIO")
        
        # Tentar habilitar debug do Facebook
        print("\n" + "="*80)
        print("TENTANDO PREENCHER CAMPOS OBRIGATÓRIOS...")
        print("="*80)
        
        # Tentar preencher campos
        test_fills = [
            ("Numero de quartos", "0"),
            ("Numero de banheiros", "1"),
            ("Preco", only_digits(listing["preco"])),
            ("Preço", only_digits(listing["preco"])),
            ("Localizacao", listing["cidade"]),
            ("Localização", listing["cidade"]),
        ]
        
        for label, value in test_fills:
            try:
                locator = page.get_by_label(label, exact=False)
                if locator.count() == 1:
                    locator.fill(value, timeout=2000)
                    print(f"✓ Preenchido '{label}' com '{value}'")
            except:
                pass
        
        # Verificar se botão ficou habilitado
        page.wait_for_timeout(2000)
        try:
            btn = page.get_by_text("Avançar", exact=True).first
            enabled = btn.is_enabled()
            print(f"\n🔘 Botão 'Avançar' habilitado: {enabled}")
        except:
            print("\n🔘 Não consegui verificar o botão")
        
        print("\n[Navegador aberto - feche quando terminar]")
        input("ENTER...")
        browser.close()

if __name__ == "__main__":
    main()
