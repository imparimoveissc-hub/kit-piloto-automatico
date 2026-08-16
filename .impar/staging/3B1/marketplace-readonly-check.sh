#!/bin/bash
set -euo pipefail

READONLY_MODE=true
ALLOW_MUTATIONS=false
ALLOW_PUBLISH=false
ALLOW_MESSAGES=false

STAGING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${STAGING_DIR}/../../.."
EVIDENCE_DIR="$PROJECT_ROOT/07_LOGS/EVIDENCIAS_MARKETPLACE_3B1"
CONFIG_FILE="$STAGING_DIR/config.json"
RESULT_FILE="$PROJECT_ROOT/07_LOGS/RESULTADO_MARKETPLACE_READONLY_3B1.json"

mkdir -p "$EVIDENCE_DIR"

# Função para registrar ação bloqueada
block_action() {
  local action="$1"
  echo "[BLOCKED] $action" >> "$EVIDENCE_DIR/blocked-actions.log"
}

# Função para registrar seletor encontrado
log_selector() {
  local name="$1"
  local selector="$2"
  local found="$3"
  echo "{\"name\":\"$name\",\"selector\":\"$selector\",\"found\":$found}" >> "$EVIDENCE_DIR/selectors.jsonl"
}

# Criar resultado JSON
cat > "$RESULT_FILE" << 'RESULT_EOF'
{
  "stage": "3B.1",
  "mode": "READ_ONLY",
  "browser_started": false,
  "existing_session_found": false,
  "marketplace_accessible": false,
  "creation_page_safely_accessible": false,
  "selectors_checked": 0,
  "selectors_found": 0,
  "blocked_requests": 0,
  "mutating_requests_completed": 0,
  "dangerous_clicks_completed": 0,
  "messages_sent": 0,
  "ads_created": 0,
  "ads_modified": 0,
  "credentials_used": false,
  "captcha_detected": false,
  "checkpoint_detected": false,
  "rc1_integrity": "CHECKING",
  "audit_integrity": "CHECKING",
  "result": "PENDING",
  "limitations": []
}
RESULT_EOF

echo "✅ Script básico criado"
