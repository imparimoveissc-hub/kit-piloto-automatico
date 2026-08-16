#!/usr/bin/env python3
"""
Quick test of marketplace enhancement module.
"""

import os
import sys
from pathlib import Path

# Add current dir to path
sys.path.insert(0, str(Path(__file__).parent))

from openai_enhance import enhance_title, enhance_description, is_enabled

# Mock property for testing
test_prop = {
    "codigo": "123456",
    "ref": "IMPAR-001",
    "operacao": "locacao",
    "tipo": "Apartamento",
    "cidade": "Joinville SC",
    "bairro": "Centro",
    "preco": "R$ 1.500,00",
    "detalhes": "Apartamento bem localizado no centro da cidade",
    "resumo_site": "Excelente localização para moradia ou investimento",
    "url": "https://www.imparimoveis.com/imovel/123456/apartamento-locacao-centro-joinville-sc",
}

print("🧪 Testing Marketplace Enhancement Module")
print(f"📌 Status: {'Enabled ✅' if is_enabled() else 'Disabled (fallback mode)'}")
print()

if not is_enabled():
    print("⚠️  Enhancement disabled - check .env file and API key")
    sys.exit(0)

print("Testing title enhancement...")
original_title = f"Apartamento para locacao no Centro - Joinville SC"
enhanced_title = enhance_title(test_prop)

if enhanced_title:
    print(f"  Original: {original_title}")
    print(f"  Enhanced: {enhanced_title}")
    print("  ✅ Title enhancement working!")
else:
    print("  ❌ Title enhancement failed")

print()
print("Testing description enhancement...")
enhanced_desc = enhance_description(test_prop)

if enhanced_desc:
    print(f"  Enhanced length: {len(enhanced_desc)} chars")
    print(f"  Preview: {enhanced_desc[:100]}...")
    print("  ✅ Description enhancement working!")
else:
    print("  ❌ Description enhancement failed")

print()
print("✨ All tests complete!")
