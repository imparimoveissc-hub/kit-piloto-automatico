#!/bin/bash
# Módulo: execute — Executar serviço com aprovação (ETAPA 3A)
# Uso: impar execute <serviço> --approval <token>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/executor.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/executor.sh"

SERVICE="${1:-}"
APPROVAL_TOKEN=""

# Parse argumentos
while [[ $# -gt 1 ]]; do
    case "$2" in
        --approval)
            APPROVAL_TOKEN="$3"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$SERVICE" ]; then
    echo "Erro: Especifique um serviço"
    echo "Uso: impar execute <serviço> --approval <token>"
    exit 1
fi

if [ -z "$APPROVAL_TOKEN" ]; then
    echo "Erro: Aprovação requerida"
    echo "Uso: impar execute <serviço> --approval <token>"
    exit 1
fi

echo ""
format_header "EXECUÇÃO CONTROLADA (ETAPA 3A)"
echo "Serviço: $SERVICE"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# VALIDAÇÕES PRÉ-EXECUÇÃO

echo "▶ Validação 1: Verificar whitelist..."
if ! is_whitelisted "$SERVICE"; then
    echo "❌ Serviço não está na whitelist"
    audit_log "$SERVICE" "BLOCKED" '{"reason":"not_whitelisted"}'
    exit 1
fi
echo "✅ Serviço autorizado"

echo "▶ Validação 2: Verificar aprovação..."
if ! validate_approval "$APPROVAL_TOKEN" "$SERVICE"; then
    audit_log "$SERVICE" "BLOCKED" '{"reason":"invalid_approval"}'
    exit 1
fi
echo "✅ Aprovação válida"

# Carregar metadados do serviço
case "$SERVICE" in
    impar-update-current-state)
        ENTRYPOINT="/Users/usuario/.local/impar-automation/update-current-state.py"
        COMMAND="python3 $ENTRYPOINT"
        BACKUP_FILES="07_LOGS/CURRENT_STATE.md"
        ;;
    *)
        echo "❌ Serviço desconhecido"
        audit_log "$SERVICE" "BLOCKED" '{"reason":"unknown_service"}'
        exit 1
        ;;
esac

echo "▶ Validação 3: Verificar entrypoint..."
if [ ! -f "$ENTRYPOINT" ]; then
    echo "❌ Entrypoint não encontrado: $ENTRYPOINT"
    audit_log "$SERVICE" "BLOCKED" '{"reason":"entrypoint_not_found"}'
    exit 1
fi
echo "✅ Entrypoint existe"

# CRIAR BACKUP
echo "▶ Backup de arquivos..."
BACKUP_DIR="${PROJECT_ROOT}/.impar/backups/$(date +%s)"
mkdir -p "$BACKUP_DIR"
for file in $BACKUP_FILES; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        cp "$PROJECT_ROOT/$file" "$BACKUP_DIR/"
        echo "  ✅ Backup: $file"
    fi
done

# EXECUTAR
echo ""
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ EXECUTANDO: $SERVICE                                       │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""

START_TIME=$(date +%s)
EXIT_CODE=0

# Executar comando e capturar saída
if output=$($COMMAND 2>&1); then
    EXIT_CODE=0
    echo "✅ Execução bem-sucedida"
else
    EXIT_CODE=$?
    echo "⚠️ Execução finalizou com código: $EXIT_CODE"
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "Saída:"
echo "$output" | head -20
if [ $(echo "$output" | wc -l) -gt 20 ]; then
    echo "... ($(echo "$output" | wc -l) linhas totais)"
fi
echo ""

# AUDITORIA
echo "▶ Registrando auditoria..."
audit_log "$SERVICE" "EXECUTED" "{\"exit_code\":$EXIT_CODE,\"duration\":$DURATION}"
mark_approval_used "$APPROVAL_TOKEN"
echo "✅ Auditoria registrada"

# VERIFICAR RESULTADO
echo ""
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ RESULTADO DA EXECUÇÃO                                           │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  Serviço:            $SERVICE"
echo "  Exit Code:          $EXIT_CODE"
echo "  Duração:            ${DURATION}s"
echo "  Aprovação:          Consumida (não reutilizável)"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ EXECUÇÃO CONCLUÍDA COM SUCESSO"
    echo ""
    echo "Arquivos modificados:"
    ls -lh "$PROJECT_ROOT/07_LOGS/CURRENT_STATE.md" 2>/dev/null || echo "  Nenhum"
    echo ""
else
    echo "❌ EXECUÇÃO FINALIZOU COM ERRO"
    echo ""
    echo "Rollback disponível:"
    echo "  impar rollback-last impar-update-current-state"
    echo ""
fi

echo "Para auditoria completa:"
echo "  tail -f 07_LOGS/EXECUTION_AUDIT.jsonl"
echo ""
