#!/bin/bash

# impar open module - Open automation folder in Finder

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
AUTOMATION_PATH="$PROJECT_ROOT/18_AUTOMATION_STACK"

main() {
  local automation_name="${1:-}"

  if [[ -z "$automation_name" ]]; then
    print_error "Uso: impar open <nome>"
    echo ""
    echo "Exemplos:"
    echo "  impar open impar-facebook-marketplace-posting"
    echo "  impar open chaves-na-mao-lead-checker"
    echo ""
    return 1
  fi

  open_automation "$automation_name"
}

open_automation() {
  local automation_name="$1"
  local automation_dir="$AUTOMATION_PATH/$automation_name"

  if [[ ! -d "$automation_dir" ]]; then
    print_error "Automação não encontrada: $automation_name"
    echo ""
    echo "Procure por 'impar list' para listar automações disponíveis"
    return 1
  fi

  print_info "Abrindo: $automation_name"

  # Abrir no Finder
  open "$automation_dir"

  print_success "Pasta aberta em: $automation_dir"
}

main "$@"
