#!/bin/bash
# Módulo: dry-run — Simular execução passo a passo (sem executar)
# Uso: impar dry-run <automacao>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/simulator.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/simulator.sh"

AUTOMATION="${1:-}"

if [ -z "$AUTOMATION" ]; then
    echo "Erro: Especifique uma automação"
    echo "Uso: impar dry-run <automacao>"
    exit 1
fi

echo ""
format_header "SIMULAÇÃO DRY-RUN DE EXECUÇÃO"
echo "Automação: $AUTOMATION"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "⚠️  ESTA É UMA SIMULAÇÃO — NENHUMA AÇÃO SERÁ EXECUTADA"
echo ""

# Mapear automação para função de simulação
case "$AUTOMATION" in
    impar-facebook-marketplace-posting)
        simulate_marketplace_steps
        ;;
    impar-messenger-bridge)
        simulate_messenger_steps
        ;;
    chaves-na-mao-lead-checker)
        simulate_leads_steps
        ;;
    nfem-joinville)
        simulate_nfse_steps
        ;;
    *)
        echo "⚠️  Simulação não configurada para: $AUTOMATION"
        echo ""
        echo "Simulações disponíveis:"
        echo "  • impar-facebook-marketplace-posting"
        echo "  • impar-messenger-bridge"
        echo "  • chaves-na-mao-lead-checker"
        echo "  • nfem-joinville"
        echo ""
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CONCLUSÃO DA SIMULAÇÃO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Simulação concluída com sucesso"
echo "   Nenhuma ação foi realmente executada"
echo "   Todos os passos foram marcados como SIMULADO"
echo ""
echo "PRÓXIMOS PASSOS:"
echo "  1. Revisar cada passo da simulação acima"
echo "  2. Confirmar que as ações estão corretas"
echo "  3. Se tudo está OK, aguardar autorização explícita para ETAPA 3"
echo ""
echo "PARA EXECUÇÃO REAL:"
echo "  A execução real ainda não está habilitada."
echo "  Utilize 'impar plan', 'impar validate' e 'impar dry-run'"
echo "  para preparar e simular antes de executor."
echo ""
