#!/bin/bash
# Módulo: plan-execution — Gerar plano de execução com hash
# Uso: impar plan-execution <serviço>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/executor.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/executor.sh"

SERVICE="${1:-}"

if [ -z "$SERVICE" ]; then
    echo "Erro: Especifique um serviço"
    echo "Uso: impar plan-execution <serviço>"
    exit 1
fi

echo ""
format_header "PLANO DE EXECUÇÃO CONTROLADA (ETAPA 3A)"
echo "Serviço: $SERVICE"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Verificar whitelist
if ! is_whitelisted "$SERVICE"; then
    echo "❌ Serviço não autorizado para execução na ETAPA 3A"
    echo ""
    echo "Serviços autorizados:"
    echo "  • impar-update-current-state (apenas)"
    echo ""
    exit 1
fi

# Gerar plano completo
case "$SERVICE" in
    impar-update-current-state)
        ENTRYPOINT="/Users/usuario/.local/impar-automation/update-current-state.py"
        COMMAND="python3 $ENTRYPOINT"
        FILES_READ="
  • ~/.local/impar-automation/marketplace_boot_checkpoint.json
  • ~/.local/impar-automation/chaves-na-mao/checkpoint.json
  • 07_LOGS/task-ledger.md"
        FILES_MODIFIED="
  • 07_LOGS/CURRENT_STATE.md (backup de anterior em CURRENT_STATE.backup-HHMMSS)"
        DURATION="5-10 segundos"
        RISKS="
  • BAIXO: Leitura de JSON pode falhar se corrompido
  • BAIXO: Arquivo task-ledger pode estar em uso"
        PRECONDITIONS="
  • Python 3 disponível
  • Diretório ~/.local/impar-automation/ acessível
  • 07_LOGS/ acessível"
        POSTCONDITIONS="
  • CURRENT_STATE.md atualizado
  • Backup anterior preservado
  • Logs da execução em ~/.local/impar-automation/logs/"
        ;;
    *)
        echo "❌ Serviço desconhecido: $SERVICE"
        exit 1
        ;;
esac

# Criar conteúdo do plano
PLAN_CONTENT=$(cat <<PLAN
SERVICE: $SERVICE
ENTRYPOINT: $ENTRYPOINT
COMMAND: $COMMAND

ARQUIVOS QUE SERÃO LIDOS:$FILES_READ

ARQUIVOS QUE SERÃO MODIFICADOS:$FILES_MODIFIED

ESTIMATIVA DE DURAÇÃO: $DURATION

RISCOS CONHECIDOS:$RISKS

PRÉ-CONDIÇÕES:$PRECONDITIONS

PÓS-CONDIÇÕES:$POSTCONDITIONS

ROLLBACK POSSÍVEL:
  • Restaurar CURRENT_STATE.backup-HHMMSS → CURRENT_STATE.md
  • Comando: impar rollback-last impar-update-current-state

DATA DO PLANO: $(date -u +'%Y-%m-%dT%H:%M:%SZ')
PLAN
)

# Gerar hash do plano
PLAN_HASH=$(generate_plan_hash "$PLAN_CONTENT")

# Exibir plano
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ PLANO COMPLETO DE EXECUÇÃO                                      │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "$PLAN_CONTENT"
echo ""

# Exibir informações de autorização
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ INFORMAÇÕES DE APROVAÇÃO                                        │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  Hash do plano:         $PLAN_HASH"
echo "  Serviço:               $SERVICE"
echo "  Validade:              60 segundos"
echo "  Número de usos:        1 (consumida após uso)"
echo ""
echo "Para aprovar e executar:"
echo ""
echo "  1. Revise o plano acima (IMPORTANTE)"
echo "  2. Execute: impar approve $PLAN_HASH"
echo "  3. A aprovação expirará em 60 segundos"
echo "  4. Execute: impar execute $SERVICE --approval <TOKEN>"
echo ""

echo "⚠️  ATENÇÃO:"
echo "  • Se o plano mudar, o hash muda e a aprovação é inválida"
echo "  • A aprovação só pode ser usada UMA VEZ"
echo "  • Se expirar (60s), você precisa gerar novo plano"
echo ""

# Guardar plano em arquivo temporário para referência
PLAN_FILE="${PROJECT_ROOT}/.impar/plans/${PLAN_HASH}.plan"
mkdir -p "$(dirname "$PLAN_FILE")"
echo "$PLAN_CONTENT" > "$PLAN_FILE"
echo "Hash: $PLAN_HASH" >> "$PLAN_FILE"

echo "✅ Plano gerado e salvo"
echo "   Hash: $PLAN_HASH"
echo ""
