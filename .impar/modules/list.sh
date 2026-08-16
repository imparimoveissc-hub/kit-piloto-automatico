#!/bin/bash

# impar list module - List all registered automations

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
REGISTRY_FILE="$PROJECT_ROOT/.impar/registry.json"
HARDCODED_REGISTRY="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"

main() {
  print_section "LIST — Automações Registradas"

  # Tentar múltiplos locais
  local registry_path=""

  if [[ -f "$HARDCODED_REGISTRY" ]]; then
    registry_path="$HARDCODED_REGISTRY"
  elif [[ -f "$REGISTRY_FILE" ]]; then
    registry_path="$REGISTRY_FILE"
  else
    print_warning "Registry não encontrado"
    return 1
  fi

  echo "Automações Operacionais:"
  echo ""

  # Parse JSON manualmente com jq se disponível, senão com grep/awk
  if command -v jq &>/dev/null; then
    jq -r '.automations[] | "\(.id). \(.name_canonical) (\(.type)) — \(.status)"' "$registry_path" | while read -r line; do
      echo "  $line"
    done
  else
    # Fallback sem jq: listar apenas nomes
    grep -o '"name_canonical": "[^"]*"' "$registry_path" | cut -d'"' -f4 | nl | while read -r num name; do
      echo "  $num. $name"
    done
  fi

  echo ""
  echo "Dicas:"
  echo "  impar info <nome>      — Ver detalhes de uma automação"
  echo "  impar open <nome>      — Abrir pasta da automação"
  echo "  impar health <nome>    — Verificar saúde da automação"
  echo "  impar map              — Ver mapa de arquitetura"
  echo ""
}

main "$@"
