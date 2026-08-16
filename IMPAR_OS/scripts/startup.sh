#!/usr/bin/env bash
# IMPAR OS — Startup/Wake script
# Executa em: boot, wake do sleep, reconexão de rede
# Princípio: ZERO tokens de IA — só operações determinísticas

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_DIR="$(dirname "$SCRIPT_DIR")"
DB="$OS_DIR/database/impar.db"
LOG="$OS_DIR/logs/startup.log"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EVENT="${IMPAR_EVENT:-boot}"

log() { echo "[$TS] [startup] $*" >> "$LOG"; }

log "--- evento=$EVENT pid=$$ ---"

# ── 1. Aguardar Docker (máx 30s) ────────────────────────────────────────────
docker_wait=0
until docker info >/dev/null 2>&1 || [[ $docker_wait -ge 30 ]]; do
  sleep 2; docker_wait=$((docker_wait+2))
done

if ! docker info >/dev/null 2>&1; then
  log "AVISO: Docker não disponível após ${docker_wait}s — abortando"
  exit 0
fi

# ── 2. Garantir n8n UP ───────────────────────────────────────────────────────
n8n_wait=0
until curl -sf http://127.0.0.1:5678/healthz >/dev/null 2>&1 || [[ $n8n_wait -ge 60 ]]; do
  # Se container existe mas está parado, iniciar
  status=$(docker ps -a --filter name=impar-n8n --format "{{.Status}}" 2>/dev/null | head -1)
  if echo "$status" | grep -qi "exited\|stopped\|created"; then
    log "n8n parado — iniciando..."
    cd "$HOME/.impar-n8n-core" && docker compose up -d >/dev/null 2>&1 || \
      docker start impar-n8n >/dev/null 2>&1 || true
  fi
  sleep 3; n8n_wait=$((n8n_wait+3))
done

if curl -sf http://127.0.0.1:5678/healthz >/dev/null 2>&1; then
  log "n8n UP (aguardou ${n8n_wait}s)"
else
  log "AVISO: n8n indisponível após ${n8n_wait}s"
fi

# ── 3. Sync de estado (sem IA) ───────────────────────────────────────────────
if [[ -f "$DB" ]]; then
  sqlite3 "$DB" "INSERT OR REPLACE INTO system_state VALUES
    ('last_startup','$TS','$TS'),
    ('last_event','$EVENT','$TS'),
    ('n8n_status','$(curl -sf http://127.0.0.1:5678/healthz >/dev/null 2>&1 && echo ok || echo down)','$TS');" 2>/dev/null || true
  log "estado sincronizado no banco"
fi

# ── 4. Gravar execução (sem IA) ──────────────────────────────────────────────
if [[ -f "$DB" ]]; then
  sqlite3 "$DB" "INSERT INTO executions
    (run_id,timestamp,origin,action,duration_ms,status,ai_used,cache_used,exit_code)
    VALUES ('startup-$$','$TS','launchagent','startup.${EVENT}',0,'ok',0,0,0);" 2>/dev/null || true
fi

log "startup concluído — ai_used=false"

# ── 5. Rotacionar log (manter ≤500 linhas) ──────────────────────────────────
if [[ -f "$LOG" ]]; then
  tail -500 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG" 2>/dev/null || true
fi
