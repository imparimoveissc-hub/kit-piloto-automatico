#!/bin/bash
set -euo pipefail

# Modo Sandbox Global
export SANDBOX_MODE="true"
export SANDBOX_TEMP=$(mktemp -d)
export SANDBOX_LOG="$SANDBOX_TEMP/sandbox.log"

trap "rm -rf $SANDBOX_TEMP" EXIT

# Função para interceptar chamadas externas
would_execute() {
  local action="$1"
  local details="${2:-}"
  echo "[WOULD_EXECUTE] $action $([ -n "$details" ] && echo "→ $details" || echo "")" | tee -a "$SANDBOX_LOG"
}

# Substituir executáveis perigosos
browser() { would_execute "WOULD_OPEN_BROWSER" "$@"; }
playwright() { would_execute "WOULD_START_PLAYWRIGHT" "$@"; }
whatsapp_send() { would_execute "WOULD_SEND_WHATSAPP" "$@"; }
facebook_post() { would_execute "WOULD_POST_MARKETPLACE" "$@"; }
api_call() { would_execute "WOULD_CALL_API" "$@"; }
start_launchagent() { would_execute "WOULD_START_LAUNCHAGENT" "$@"; }

export -f would_execute browser playwright whatsapp_send facebook_post api_call start_launchagent

# Log de início
echo "════════════════════════════════════════════" >> "$SANDBOX_LOG"
echo "SANDBOX MODE ATIVADO" >> "$SANDBOX_LOG"
echo "Timestamp: $(date -u +'%Y-%m-%dT%H:%M:%SZ')" >> "$SANDBOX_LOG"
echo "Temp Dir: $SANDBOX_TEMP" >> "$SANDBOX_LOG"
echo "════════════════════════════════════════════" >> "$SANDBOX_LOG"

# Retornar caminho do log
echo "$SANDBOX_LOG"
