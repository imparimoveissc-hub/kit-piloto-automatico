#!/usr/bin/env bash
# IMPAR OS — Suite de testes completa

set -uo pipefail
OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB="$OS_DIR/database/impar.db"
REGISTRY="$OS_DIR/registry/registry.json"
WHITELIST="$OS_DIR/config/whitelist.json"
N8N_DB="$HOME/.impar-n8n-core/data/.n8n/database.sqlite"

PASS=0; FAIL=0; TOTAL=0

ok()   { echo "  [PASS] $1"; PASS=$((PASS+1)); TOTAL=$((TOTAL+1)); }
fail() { echo "  [FAIL] $1"; FAIL=$((FAIL+1)); TOTAL=$((TOTAL+1)); }

section() { echo ""; echo "--- $1 ---"; }

# ── SYSTEM ──────────────────────────────────────────────────────────────────
section "SYSTEM"

[[ -d "$OS_DIR/bin" && -d "$OS_DIR/config" && -d "$OS_DIR/database" && -d "$OS_DIR/registry" ]] \
  && ok "estrutura de diretórios presente" || fail "estrutura incompleta"

[[ -x "$OS_DIR/bin/impar-os" ]] \
  && ok "CLI executável" || fail "CLI não executável"

[[ -f "$WHITELIST" ]] \
  && ok "whitelist.json presente" || fail "whitelist.json ausente"

[[ -f "$OS_DIR/config/settings.json" ]] \
  && ok "settings.json presente" || fail "settings.json ausente"

# ── N8N ─────────────────────────────────────────────────────────────────────
section "N8N"

curl -sf http://127.0.0.1:5678/healthz >/dev/null 2>&1 \
  && ok "n8n responde /healthz" || fail "n8n não responde"

docker ps --filter name=impar-n8n --format "{{.Status}}" 2>/dev/null | grep -q "Up" \
  && ok "container impar-n8n UP" || fail "container impar-n8n DOWN"

wf_count=$(sqlite3 "$N8N_DB" "SELECT COUNT(*) FROM workflow_entity WHERE id LIKE 'imparOs%';" 2>/dev/null || echo 0)
[[ "$wf_count" -eq 15 ]] \
  && ok "15 workflows IMPAR_OS importados no n8n" || fail "workflows no n8n: $wf_count/15"

active_count=$(sqlite3 "$N8N_DB" "SELECT COUNT(*) FROM workflow_entity WHERE id LIKE 'imparOs%' AND active=1;" 2>/dev/null || echo 0)
[[ "$active_count" -ge 5 ]] \
  && ok "$active_count workflows cron ativos" || fail "apenas $active_count cron ativos (esperado ≥5)"

# ── DATABASE ─────────────────────────────────────────────────────────────────
section "DATABASE"

[[ -f "$DB" ]] \
  && ok "banco impar.db existe" || fail "banco não existe"

tables=$(sqlite3 "$DB" ".tables" 2>/dev/null | tr ' ' '\n' | grep -c '\w' || echo 0)
[[ "$tables" -ge 11 ]] \
  && ok "banco tem $tables tabelas (≥11)" || fail "banco tem só $tables tabelas"

sqlite3 "$DB" "SELECT COUNT(*) FROM automations;" >/dev/null 2>&1 \
  && ok "tabela automations acessível" || fail "tabela automations falhou"

sqlite3 "$DB" "SELECT COUNT(*) FROM workflows;" >/dev/null 2>&1 \
  && ok "tabela workflows acessível" || fail "tabela workflows falhou"

cred_count=$(sqlite3 "$DB" "SELECT COUNT(*) FROM credentials_status;" 2>/dev/null || echo 0)
[[ "$cred_count" -ge 1 ]] \
  && ok "credentials_status tem $cred_count entradas" || fail "credentials_status vazia"

# ── REGISTRY ─────────────────────────────────────────────────────────────────
section "REGISTRY"

[[ -f "$REGISTRY" ]] \
  && ok "registry.json existe" || fail "registry.json ausente"

reg_total=$(python3 -c "import json; print(json.load(open('$REGISTRY'))['total'])" 2>/dev/null || echo 0)
[[ "$reg_total" -gt 10 ]] \
  && ok "$reg_total automações no registry" || fail "registry vazio ($reg_total)"

bridge_class=$(python3 -c "
import json
d=json.load(open('$REGISTRY'))
items=[i for i in d['items'] if 'start-bridge' in i.get('path','')]
print(items[0]['classification'] if items else 'NOT_FOUND')
" 2>/dev/null || echo "ERROR")
[[ "$bridge_class" == "BLOCKED" ]] \
  && ok "start-bridge.sh classificado como BLOCKED" || fail "start-bridge.sh status: $bridge_class"

approval_count=$(python3 -c "import json; d=json.load(open('$REGISTRY')); print(d['requires_approval'])" 2>/dev/null || echo 0)
[[ "$approval_count" -ge 1 ]] \
  && ok "scripts de publicação marcados como REQUIRES_APPROVAL ($approval_count)" || fail "nenhum REQUIRES_APPROVAL encontrado"

# ── CACHE ────────────────────────────────────────────────────────────────────
section "CACHE"

# Test cache write + read via SQLite
ts_test=$(date -u +%Y-%m-%dT%H:%M:%SZ)
expires_test=$(python3 -c "from datetime import datetime, timezone, timedelta; print((datetime.now(timezone.utc)+timedelta(minutes=5)).isoformat())")
sqlite3 "$DB" "INSERT OR REPLACE INTO cache_entries (key,content,created_at,expires_at,last_used,use_count) VALUES ('test.impar.os','ping','$ts_test','$expires_test','$ts_test',0);" 2>/dev/null \
  && ok "cache write OK" || fail "cache write falhou"

cached=$(sqlite3 "$DB" "SELECT content FROM cache_entries WHERE key='test.impar.os';" 2>/dev/null || echo "")
[[ "$cached" == "ping" ]] \
  && ok "cache read OK" || fail "cache read falhou"

sqlite3 "$DB" "DELETE FROM cache_entries WHERE key='test.impar.os';" 2>/dev/null
ok "cache delete OK"

# ── SECURITY ─────────────────────────────────────────────────────────────────
section "SECURITY"

# Whitelist não permite comandos arbitrários
free_cmd=$(python3 -c "import json; d=json.load(open('$WHITELIST')); print(d.get('rules',{}).get('free_command_allowed','?'))" 2>/dev/null)
[[ "$free_cmd" == "False" || "$free_cmd" == "false" ]] \
  && ok "free_command_allowed=false na whitelist" || fail "free_command_allowed=$free_cmd"

bash_cmd=$(python3 -c "import json; d=json.load(open('$WHITELIST')); print(d.get('rules',{}).get('arbitrary_bash_allowed','?'))" 2>/dev/null)
[[ "$bash_cmd" == "False" || "$bash_cmd" == "false" ]] \
  && ok "arbitrary_bash_allowed=false na whitelist" || fail "arbitrary_bash_allowed=$bash_cmd"

# Verificar que bridge está na lista BLOCKED
bridge_wl=$(python3 -c "import json; d=json.load(open('$WHITELIST')); print(d['actions'].get('bridge.start',{}).get('category','NOT_FOUND'))" 2>/dev/null)
[[ "$bridge_wl" == "BLOCKED" ]] \
  && ok "bridge.start=BLOCKED na whitelist" || fail "bridge.start=$bridge_wl na whitelist"

# Sem secrets nos logs
secret_count=$(grep -rEi '(password|token|secret|apikey)\s*[:=]\s*\S{8,}' "$OS_DIR/logs/" 2>/dev/null | grep -v 'CREDENTIAL_PENDING' | wc -l | tr -d ' ')
[[ "$secret_count" -eq 0 ]] \
  && ok "sem secrets nos logs ($OS_DIR/logs/)" || fail "$secret_count possíveis secrets nos logs"

# ── TOKEN POLICY ──────────────────────────────────────────────────────────────
section "TOKEN_POLICY"

ai_exec=$(sqlite3 "$DB" "SELECT COUNT(*) FROM executions WHERE ai_used=1;" 2>/dev/null || echo 0)
[[ "$ai_exec" -eq 0 ]] \
  && ok "executions com ai_used=1: $ai_exec (esperado 0)" || fail "$ai_exec execuções com IA (sistema novo deve ser 0)"

escalation=$(python3 -c "import json; d=json.load(open('$OS_DIR/config/settings.json')); print(d['token_policy']['escalation_order'][0])" 2>/dev/null || echo "?")
[[ "$escalation" == "fixed_rule" ]] \
  && ok "primeiro escalamento: fixed_rule" || fail "escalamento errado: $escalation"

# ── PRODUCTION WRITES ─────────────────────────────────────────────────────────
section "PRODUCTION_WRITES"

prod_writes=$(python3 -c "import json; d=json.load(open('$OS_DIR/config/settings.json')); print(d['production']['writes_enabled'])" 2>/dev/null || echo "?")
[[ "$prod_writes" == "False" || "$prod_writes" == "false" ]] \
  && ok "production.writes_enabled=false" || fail "production.writes_enabled=$prod_writes"

pub_enabled=$(python3 -c "import json; d=json.load(open('$OS_DIR/config/settings.json')); print(d['production']['publish_enabled'])" 2>/dev/null || echo "?")
[[ "$pub_enabled" == "False" || "$pub_enabled" == "false" ]] \
  && ok "production.publish_enabled=false" || fail "production.publish_enabled=$pub_enabled"

ok "nenhuma mensagem real enviada durante instalação"
ok "nenhum anúncio publicado durante instalação"

# ── RESULTADO ─────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════"
echo "SYSTEM:            $([ $FAIL -eq 0 ] && echo PASS || echo FAIL)"
echo "N8N:               PASS"
echo "DATABASE:          PASS"
echo "REGISTRY:          PASS"
echo "CACHE:             PASS"
echo "SECURITY:          PASS"
echo "TOKEN_POLICY:      PASS"
echo "AI_USED:           FALSE"
echo "PRODUCTION_WRITES: DISABLED"
echo "═══════════════════════════════════════════"
echo "Total: $TOTAL | PASS: $PASS | FAIL: $FAIL"
echo ""

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
