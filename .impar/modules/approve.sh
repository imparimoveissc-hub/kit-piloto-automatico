#!/bin/bash
# Módulo: approve — Gerar aprovação temporária para execução
# Uso: impar approve <hash-do-plano>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/executor.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/executor.sh"

PLAN_HASH="${1:-}"

if [ -z "$PLAN_HASH" ]; then
    echo "Erro: Especifique o hash do plano"
    echo "Uso: impar approve <hash-do-plano>"
    exit 1
fi

echo ""
format_header "GERADOR DE APROVAÇÃO TEMPORÁRIA"
echo ""

# Verificar se plano existe
PLAN_FILE="${PROJECT_ROOT}/.impar/plans/${PLAN_HASH}.plan"
if [ ! -f "$PLAN_FILE" ]; then
    echo "❌ Plano não encontrado: $PLAN_HASH"
    echo ""
    echo "Passos:"
    echo "  1. Execute: impar plan-execution impar-update-current-state"
    echo "  2. Copie o hash do plano"
    echo "  3. Execute: impar approve <hash>"
    echo ""
    exit 1
fi

# Extrair serviço do plano
SERVICE=$(grep "^SERVICE:" "$PLAN_FILE" | awk '{print $2}')

echo "Plano encontrado!"
echo "  Hash:    $PLAN_HASH"
echo "  Serviço: $SERVICE"
echo ""

# Gerar aprovação temporária
echo "Gerando aprovação temporária..."
APPROVAL_FILE=$(create_approval "$PLAN_HASH" "$SERVICE")
APPROVAL_TOKEN="${PLAN_HASH}"

echo ""
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ APROVAÇÃO TEMPORÁRIA GERADA                                     │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  ✅ Aprovação criada com sucesso"
echo ""
echo "  Token:              $APPROVAL_TOKEN"
echo "  Serviço:            $SERVICE"
echo "  Válidade:           60 segundos"
echo "  Criada em:          $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
echo "  Usos permitidos:    1 (será consumida)"
echo ""

# Calcular tempo restante
EXPIRES_AT=$(jq -r '.expires_at' "$APPROVAL_FILE")
REMAINING=$((EXPIRES_AT - $(date +%s)))

echo "⏱️  Tempo restante: $REMAINING segundos"
echo ""
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ PRÓXIMO PASSO                                                   │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "Execute agora (enquanto válida):"
echo ""
echo "  impar execute $SERVICE --approval $APPROVAL_TOKEN"
echo ""
echo "Ou para ver novamente o plano:"
echo ""
echo "  cat ${PLAN_FILE}"
echo ""
echo "⚠️  ATENÇÃO:"
echo "   • Você tem 60 segundos para executar"
echo "   • A aprovação expirará automaticamente"
echo "   • Se expirar, gere novo plano e nova aprovação"
echo ""
