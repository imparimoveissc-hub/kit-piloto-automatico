#!/usr/bin/env bash
# IMPAR OS — verificação de saúde dos componentes

set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_DIR="$(dirname "$SCRIPT_DIR")"
DB="$OS_DIR/database/impar.db"
JSON_OUT="${1:-}"

pass() { echo "  [PASS] $1"; }
fail() { echo "  [FAIL] $1"; FAILURES=$((FAILURES+1)); }
FAILURES=0

check_n8n() {
  local resp
  resp=$(curl -sf http://127.0.0.1:5678/healthz 2>/dev/null) && pass "n8n UP" || fail "n8n DOWN"
}

check_docker() {
  docker ps --filter name=impar-n8n --format "{{.Status}}" 2>/dev/null | grep -q "Up" && pass "impar-n8n container UP" || fail "impar-n8n container não encontrado"
}

check_db() {
  [[ -f "$DB" ]] || { fail "banco não existe: $DB"; return; }
  local tables
  tables=$(sqlite3 "$DB" ".tables" 2>/dev/null | tr ' ' '\n' | wc -l | tr -d ' ')
  [[ "$tables" -ge 10 ]] && pass "banco OK ($tables tabelas)" || fail "banco incompleto ($tables tabelas)"
}

check_registry() {
  local reg="$OS_DIR/registry/registry.json"
  [[ -f "$reg" ]] || { fail "registry.json não existe"; return; }
  local total
  total=$(python3 -c "import json; d=json.load(open('$reg')); print(d.get('total',0))" 2>/dev/null)
  [[ "$total" -gt 0 ]] && pass "registry OK ($total itens)" || fail "registry vazio"
}

check_cli() {
  [[ -x "$OS_DIR/bin/impar-os" ]] && pass "CLI executável" || fail "CLI não executável"
}

check_whitelist() {
  local wl="$OS_DIR/config/whitelist.json"
  [[ -f "$wl" ]] && pass "whitelist.json presente" || fail "whitelist.json ausente"
}

check_bridge_blocked() {
  local reg="$OS_DIR/registry/registry.json"
  [[ -f "$reg" ]] || return
  local status
  status=$(python3 -c "import json; d=json.load(open('$reg')); items=[i for i in d['items'] if 'start-bridge' in i['path']]; print(items[0]['classification'] if items else 'NOT_FOUND')" 2>/dev/null)
  [[ "$status" == "BLOCKED" ]] && pass "start-bridge.sh BLOQUEADO no registry" || fail "start-bridge.sh status: $status"
}

check_secrets_in_logs() {
  local found
  found=$(grep -rE '(password|token|secret|api_key)\s*[:=]\s*\S+' "$OS_DIR/logs/" 2>/dev/null | grep -v 'CREDENTIAL_PENDING' | wc -l | tr -d ' ')
  [[ "$found" -eq 0 ]] && pass "sem secrets nos logs" || fail "$found possíveis secrets nos logs"
}

echo "=== IMPAR OS Health Check ==="
check_n8n
check_docker
check_db
check_registry
check_cli
check_whitelist
check_bridge_blocked
check_secrets_in_logs

echo ""
if [[ "$FAILURES" -eq 0 ]]; then
  echo "RESULTADO: PASS (0 falhas)"
  exit 0
else
  echo "RESULTADO: FAIL ($FAILURES falha(s))"
  exit 1
fi
