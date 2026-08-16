#!/bin/bash

# Library for formatting kernel responses with source attribution

set -euo pipefail

# Find common.sh
if [[ -f "$(dirname "$0")/common.sh" ]]; then
  source "$(dirname "$0")/common.sh"
elif [[ -f "$(dirname "$0")/../lib/common.sh" ]]; then
  source "$(dirname "$0")/../lib/common.sh"
else
  echo "ERROR: Cannot find common.sh" >&2
  exit 1
fi

# Format response header
format_header() {
  local title="${1:-}"
  echo ""
  print_section "$title"
}

# Format automation info
format_automation_info() {
  local name="${1:-}"
  local status="${2:-unknown}"
  local risk="${3:-MEDIUM}"

  case "$status" in
    active|ativo)
      echo "  ${GREEN}✅ ATIVO${NC}"
      ;;
    offline)
      echo "  ${RED}🔴 OFFLINE${NC}"
      ;;
    paused)
      echo "  ${YELLOW}⏸️ PAUSADO${NC}"
      ;;
    *)
      echo "  ${YELLOW}?${NC} $status"
      ;;
  esac

  echo "  Risco: $risk"
}

# Format source citation
format_sources() {
  local -a sources=("$@")

  if [[ ${#sources[@]} -eq 0 ]]; then
    return
  fi

  echo ""
  echo "${GRAY}Fontes consultadas:${NC}"
  for source in "${sources[@]}"; do
    echo "  • $source"
  done
}

# Format execution blocker
format_execution_blocker() {
  echo ""
  print_warning "EXECUÇÃO BLOQUEADA"
  echo "  Este kernel só suporta leitura. Use 'impar run <automação>' para saber como executar."
  echo ""
}

# Format warning
format_warning() {
  local msg="${1:-}"
  echo ""
  print_warning "$msg"
  echo ""
}

# Format success
format_success() {
  local msg="${1:-}"
  echo ""
  print_success "$msg"
  echo ""
}

export -f format_header format_automation_info format_sources format_execution_blocker format_warning format_success
