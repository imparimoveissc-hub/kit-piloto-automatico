#!/usr/bin/env python3
"""
Script para autenticar no Facebook e preparar sessão para automação Marketplace

Uso:
  python3 login-facebook.py

O navegador abrirá e você poderá fazer login normalmente.
A sessão será salva no perfil do navegador para reuso em automações.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-profile"

def main():
    print("="*80)
    print("LOGIN FACEBOOK - AUTOMAÇÃO MARKETPLACE IMPAR")
    print("="*80)
    
    PROFILE.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Perfil: {PROFILE}")
    print("\nAbrindo Facebook...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            headless=False,
            viewport={"width": 1280, "height": 900},
        )
        
        page = browser.new_page()
        page.goto("https://facebook.com", wait_until="load")
        
        print("\n" + "="*80)
        print("✅ NAVEGADOR ABERTO")
        print("="*80)
        print("\n📋 INSTRUÇÕES:")
        print("  1. Faça login na sua conta Facebook (Impar/Jonata)")
        print("  2. Verifique se está logado (deve aparecer seu nome no menu)")
        print("  3. Navegue para: https://facebook.com/marketplace/create/rental")
        print("  4. Verifique se o formulário aparecer corretamente")
        print("  5. Feche o navegador quando terminar")
        print("\n💾 Sua sessão será salva automaticamente no perfil!")
        print("="*80)
        
        input("\nPressione ENTER para continuar (o navegador já está aberto)...")
        
        # Aguardar enquanto o navegador está aberto
        while len(browser.contexts[0].pages) > 0:
            time.sleep(1)
        
        browser.close()
    
    print("\n✅ Sessão salva! Você pode agora executar:")
    print("\n  python3 publish_marketplace_playwright.py \\")
    print("    --queue <fila.json> \\")
    print("    --index 1 \\")
    print("    --headed \\")
    print("    --publish")
    print("\n")

if __name__ == "__main__":
    main()
