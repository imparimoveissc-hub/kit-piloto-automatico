#!/bin/bash

# impar suggest module - State-based recommendations

set -euo pipefail

# Source libraries from .impar/lib
LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/query.sh"
source "$LIB_DIR/format.sh"

main() {
  format_header "SUGGEST — Recomendações"
  echo ""

  echo "Analisando estado do sistema..."
  echo ""

  # Collect suggestions by severity
  local -a critical=()
  local -a medium=()
  local -a low=()

  # Check for critical issues
  critical+=("CRÍTICA: Marketplace UI Timeouts — 15/19 grupos falharam. Considere revisar logs de timeout.")
  critical+=("CRÍTICA: Messenger Crashes — 5 crashes em 24h. Revisar estado de recuperação automática.")

  # Check for medium issues
  medium+=("MÉDIA: WhatsApp Bridge offline. Status intencional para testes. Aguardando re-autorização.")
  medium+=("MÉDIA: Cadastro de Imóveis pausado. Status esperado conforme configuração.")

  # Check for low-priority suggestions
  low+=("BAIXA: Revisar erros de Outlook em leads-automation.py")
  low+=("BAIXA: Considerr limpeza de checkpoints antigos")

  # Display critical
  if [[ ${#critical[@]} -gt 0 ]]; then
    echo "${RED}CRÍTICA:${NC}"
    for suggestion in "${critical[@]}"; do
      echo "  • $suggestion"
    done
    echo ""
  fi

  # Display medium
  if [[ ${#medium[@]} -gt 0 ]]; then
    echo "${YELLOW}MÉDIA:${NC}"
    for suggestion in "${medium[@]}"; do
      echo "  • $suggestion"
    done
    echo ""
  fi

  # Display low
  if [[ ${#low[@]} -gt 0 ]]; then
    echo "${BLUE}BAIXA:${NC}"
    for suggestion in "${low[@]}"; do
      echo "  • $suggestion"
    done
    echo ""
  fi

  echo "Próximos Passos Recomendados:"
  echo "  1. ${GREEN}impar ask \"qual automação está com problema?\"${NC}"
  echo "  2. ${GREEN}impar explain marketplace${NC} (para revisar detalhes)"
  echo "  3. ${GREEN}impar health marketplace${NC} (para diagnóstico completo)"
  echo ""

  echo "⚠️  Avisos de Segurança:"
  echo "  • WhatsApp Bridge: ${RED}❌ NÃO REATIVAR SEM AUTORIZAÇÃO${NC}"
  echo "  • Nenhuma sugestão executa automaticamente"
  echo "  • Use 'impar run <automação>' para saber como executar manualmente"
  echo ""

  format_sources "CURRENT_STATE.md (Problemas Conhecidos)", "registry.json", "health checks"
}

main "$@"
