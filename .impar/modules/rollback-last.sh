#!/bin/bash
# Módulo: rollback-last — Desfazer última execução de um serviço
# Uso: impar rollback-last <serviço>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"

SERVICE="${1:-}"

if [ -z "$SERVICE" ]; then
    echo "Erro: Especifique um serviço"
    echo "Uso: impar rollback-last <serviço>"
    exit 1
fi

echo ""
format_header "ROLLBACK DA ÚLTIMA EXECUÇÃO"
echo "Serviço: $SERVICE"
echo ""

# Encontrar backup mais recente
BACKUPS_DIR="${PROJECT_ROOT}/.impar/backups"
if [ ! -d "$BACKUPS_DIR" ]; then
    echo "❌ Nenhum backup encontrado"
    exit 1
fi

LATEST_BACKUP=$(ls -t "$BACKUPS_DIR" | head -1)
if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ Nenhum backup disponível"
    exit 1
fi

BACKUP_PATH="${BACKUPS_DIR}/${LATEST_BACKUP}"

echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ PREVIEW DO ROLLBACK                                             │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "Serviço:        $SERVICE"
echo "Backup:         $LATEST_BACKUP"
echo "Localização:    $BACKUP_PATH"
echo ""
echo "Arquivos que serão restaurados:"
ls -lh "$BACKUP_PATH"/ 2>/dev/null || echo "  Nenhum arquivo"
echo ""

# Pedir confirmação
read -p "Deseja continuar com o rollback? (sim/não): " -r confirm

if [ "$confirm" != "sim" ]; then
    echo "❌ Rollback cancelado"
    exit 0
fi

# Executar rollback
echo ""
echo "▶ Restaurando arquivos..."
for file in "$BACKUP_PATH"/*; do
    filename=$(basename "$file")
    # Restaurar para localização original
    if [ "$filename" = "CURRENT_STATE.md" ]; then
        target="${PROJECT_ROOT}/07_LOGS/CURRENT_STATE.md"
    else
        target="${PROJECT_ROOT}/$filename"
    fi

    cp "$file" "$target"
    echo "  ✅ Restaurado: $filename"
done

echo ""
echo "✅ ROLLBACK CONCLUÍDO COM SUCESSO"
echo ""
echo "Arquivos restaurados de: $LATEST_BACKUP"
echo "Data do backup: $(stat -f '%Sm' "$BACKUP_PATH" 2>/dev/null || echo 'N/A')"
echo ""
