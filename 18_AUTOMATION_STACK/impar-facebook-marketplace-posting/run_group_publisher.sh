#!/bin/bash
# Launcher unico para a publicacao em grupos do Facebook Impar.
# Fluxo:
# 1) prepara a fila do Marketplace para a data alvo;
# 2) gera a fila de grupos correspondente;
# 3) abre o publicador de grupos já ajustado.
#
# Uso:
#   ./run_group_publisher.sh
#   ./run_group_publisher.sh 2026-07-20
#   ./run_group_publisher.sh --publish --headed
#   TARGET_DAY=2026-07-20 ./run_group_publisher.sh --publish

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DAY="${TARGET_DAY:-}"
PUBLISH=0
HEADED=0
SYSTEM_CHROME=0
BATCH_SIZE=19
BATCH_INTERVAL=180
START_INDEX=1
SKIP_GENERATE=0

show_help() {
    cat <<'EOF'
Launcher unico do publicador de grupos da Impar.

Uso:
  ./run_group_publisher.sh [YYYY-MM-DD] [opcoes]

Opcoes:
  --publish         Publica de verdade.
  --headed          Abre o navegador visivel.
  --system-chrome   Usa o Google Chrome do sistema.
  --start-index N   Comeca a publicar a partir do item N da fila.
  --batch-size N    Quantidade de grupos por lote.
  --batch-interval N Intervalo em segundos entre lotes.
  --skip-generate   Nao regenera as filas antes de publicar.
  --help            Mostra esta ajuda.

Variavel de ambiente:
  TARGET_DAY        Data alvo no formato YYYY-MM-DD.
EOF
}

is_date() {
    [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --publish)
            PUBLISH=1
            shift
            ;;
        --headed)
            HEADED=1
            shift
            ;;
        --system-chrome)
            SYSTEM_CHROME=1
            shift
            ;;
        --start-index)
            START_INDEX="${2:-}"
            shift 2
            ;;
        --batch-size)
            BATCH_SIZE="${2:-}"
            shift 2
            ;;
        --batch-interval)
            BATCH_INTERVAL="${2:-}"
            shift 2
            ;;
        --skip-generate)
            SKIP_GENERATE=1
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            if [[ -z "$TARGET_DAY" ]] && is_date "$1"; then
                TARGET_DAY="$1"
                shift
            else
                echo "[ERRO] Argumento desconhecido: $1" >&2
                echo
                show_help
                exit 1
            fi
            ;;
    esac
done

if [[ -z "$TARGET_DAY" ]]; then
    TARGET_DAY="$(python3 -c 'from datetime import date, timedelta; print((date.today() + timedelta(days=1)).isoformat())')"
fi

cd "$SCRIPT_DIR"

echo "[INFO] Launcher grupos Impar"
echo "[INFO] Data alvo: $TARGET_DAY"
echo "[INFO] Modo: $([[ "$PUBLISH" -eq 1 ]] && echo PUBLICAR || echo REVISAO)"

if [[ "$SKIP_GENERATE" -eq 0 ]]; then
    echo "[ETAPA 1/3] Gerando fila do Marketplace..."
    MARKETPLACE_START_DATE="$TARGET_DAY" python3 generate_queue.py

    echo "[ETAPA 2/3] Gerando fila de grupos..."
    python3 generate_group_queue.py "$TARGET_DAY"
else
    echo "[ETAPA 1/3] Geração de filas ignorada por --skip-generate."
fi

echo "[ETAPA 3/3] Abrindo publicador de grupos..."
cmd=(
    python3 publish_groups_playwright.py
    --queue "$SCRIPT_DIR/fila-grupos-postagens.csv"
    --start-index "$START_INDEX"
    --batch-size "$BATCH_SIZE"
    --batch-interval "$BATCH_INTERVAL"
)

if [[ "$HEADED" -eq 1 ]]; then
    cmd+=(--headed)
fi

if [[ "$PUBLISH" -eq 1 ]]; then
    cmd+=(--publish)
fi

if [[ "$SYSTEM_CHROME" -eq 1 ]]; then
    cmd+=(--system-chrome)
fi

"${cmd[@]}"
