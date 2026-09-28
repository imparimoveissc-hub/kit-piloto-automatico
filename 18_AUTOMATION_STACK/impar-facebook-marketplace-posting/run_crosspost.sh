#!/bin/bash
# run_crosspost.sh — Wrapper para crosspost_groups_v2.py com lock e timeout.
# Chamado pelos LaunchAgents: com.impar.marketplace-crosspost-{manha,tarde,noite}.plist
#
# Uso: ./run_crosspost.sh [--cadence N] [--max-dia N] [--limit N] [--mensagem "texto"]
# Ex:  ./run_crosspost.sh --cadence 180 --max-dia 32

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$HOME/.local/impar-automation/marketplace"
LOG="$LOG_DIR/crosspost-wrapper.log"
LOCK="$LOG_DIR/.crosspost.lock"
LOCK_MAX_AGE=7200   # 2 horas
TIMEOUT=14400       # 4 horas (96 grupos × 3 min = ~4.8h no pior caso)

mkdir -p "$LOG_DIR"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

# --- Lock: evita execucoes paralelas ---
if [ -f "$LOCK" ]; then
    PID=$(awk 'NR==1 {print $1}' "$LOCK" 2>/dev/null || echo 0)
    START_TS=$(awk 'NR==2 {print $1}' "$LOCK" 2>/dev/null || echo 0)
    NOW_TS=$(date +%s)
    AGE=$(( NOW_TS - ${START_TS:-0} ))
    if kill -0 "$PID" 2>/dev/null; then
        if [ "$AGE" -gt "$LOCK_MAX_AGE" ]; then
            echo "[$(ts)] Lock antigo (${AGE}s, PID=$PID) — removendo e seguindo" >> "$LOG"
            rm -f "$LOCK"
        else
            echo "[$(ts)] Crosspost ja rodando (PID=$PID, ${AGE}s) — saindo" >> "$LOG"
            exit 0
        fi
    else
        echo "[$(ts)] Lock orfao removido (PID=$PID)" >> "$LOG"
        rm -f "$LOCK"
    fi
fi
printf "%s\n%s\n" "$$" "$(date +%s)" > "$LOCK"
trap "rm -f '$LOCK'" EXIT

echo "[$(ts)] run_crosspost.sh iniciado (args: $*)" >> "$LOG"

# --- Executa com timeout ---
/usr/bin/python3 -u "$SCRIPT_DIR/crosspost_groups_v2.py" "$@" &
CHILD_PID=$!
WAITED=0
EXIT_CODE=0

while kill -0 "$CHILD_PID" 2>/dev/null; do
    if [ "$WAITED" -ge "$TIMEOUT" ]; then
        echo "[$(ts)] Timeout do crosspost (${TIMEOUT}s) — encerrando PID=$CHILD_PID" >> "$LOG"
        kill "$CHILD_PID" 2>/dev/null || true
        sleep 2
        kill -9 "$CHILD_PID" 2>/dev/null || true
        wait "$CHILD_PID" 2>/dev/null || true
        EXIT_CODE=124
        break
    fi
    sleep 10
    WAITED=$((WAITED + 10))
done

if [ "$EXIT_CODE" = "0" ]; then
    wait "$CHILD_PID"
    EXIT_CODE=$?
fi

echo "[$(ts)] run_crosspost.sh encerrado (exit=$EXIT_CODE)" >> "$LOG"
exit $EXIT_CODE
