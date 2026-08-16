#!/bin/bash

# impar search module - Term-based search across registry and documentation

set -euo pipefail

# Source libraries from .impar/lib
LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

main() {
  local query="${1:-}"

  if [[ -z "$query" ]]; then
    print_error "Forneça um termo para buscar."
    echo ""
    echo "Exemplos:"
    echo "  impar search marketplace"
    echo "  impar search facebook"
    echo "  impar search offline"
    return 1
  fi

  format_header "SEARCH — Busca por Termo"
  echo "Termo: $query"
  echo ""

  local registry="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"
  local found=0

  if [[ ! -f "$registry" ]]; then
    print_error "Registry não encontrado"
    return 1
  fi

  # Search in registry
  python3 << PYSCRIPT
import json
import sys

query = "$query".lower()
registry = "$registry"
found = False

try:
  with open(registry) as f:
    data = json.load(f)

    for auto in data.get('automations', []):
      name = auto.get('name_canonical', '').lower()
      aliases = [a.lower() for a in auto.get('aliases', [])]
      description = auto.get('description', '').lower()
      category = auto.get('category', '').lower()

      if query in name or query in description or query in category or any(query in a for a in aliases):
        print(f"  {auto['name_canonical']}")
        print(f"    Tipo: {auto['type']}")
        print(f"    Status: {auto['status']}")
        print(f"    Descrição: {auto['description'][:80]}...")
        print(f"    Categoria: {auto['category']}")
        print(f"    Risco: {auto['risk_level']}")
        print()
        found = True

except Exception as e:
  print(f"Erro ao buscar: {e}", file=sys.stderr)
  sys.exit(1)

if not found:
  print(f"  Nenhuma automação encontrada com '{query}'")

PYSCRIPT

  echo ""
  echo "Dica: use 'impar explain <automação>' para mais detalhes"
  echo ""
  format_sources "registry.json"
}

main "$@"
