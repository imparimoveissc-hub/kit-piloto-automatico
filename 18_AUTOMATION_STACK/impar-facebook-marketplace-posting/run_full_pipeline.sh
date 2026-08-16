#!/bin/bash
# Pipeline completo: Marketplace → Fila → Grupos
# Uso: ./run_full_pipeline.sh [TARGET_DATE]
# Ex: ./run_full_pipeline.sh 2026-07-18

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DATE="${1:-}"

echo "[$(date +'%Y-%m-%d %H:%M:%S')] ========== PIPELINE MARKETPLACE + GRUPOS =========="

if [ -n "$TARGET_DATE" ]; then
    echo "[INFO] Data alvo: $TARGET_DATE"
    export TARGET_DAY="$TARGET_DATE"
else
    echo "[INFO] Data alvo: hoje"
fi

# 1. Gerar fila diária do Marketplace
echo ""
echo "[ETAPA 1/2] Gerando fila diária do Marketplace..."
cd "$SCRIPT_DIR"
python3 generate_queue.py || {
    echo "[ERRO] Falha ao gerar fila de Marketplace"
    exit 1
}

# 2. Expandir em grupos
echo ""
echo "[ETAPA 2/2] Expandindo em fila de grupos (19 grupos × cadência 3min)..."
if [ -n "$TARGET_DATE" ]; then
    python3 generate_group_queue.py "$TARGET_DATE" || {
        echo "[ERRO] Falha ao gerar fila de grupos"
        exit 1
    }
else
    python3 generate_group_queue.py || {
        echo "[ERRO] Falha ao gerar fila de grupos"
        exit 1
    }
fi

echo ""
echo "[SUCESSO] Pipeline completo!"
echo ""
echo "Arquivos gerados:"
echo "  - fila-postagens.csv (Marketplace)"
echo "  - fila-grupos-postagens.csv (Grupos, 19 por imóvel)"
echo ""
echo "Próximas etapas:"
echo "  1. Revisar fila-postagens.csv no Marketplace"
echo "  2. Confirmar publicação (ou usar publish_marketplace_playwright.py)"
echo "  3. Aguardar conclusão das postagens"
echo "  4. Expandir fila de grupos (ou roda automático em 3h se configurado)"
echo ""
