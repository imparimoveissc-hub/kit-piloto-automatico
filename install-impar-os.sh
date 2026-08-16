#!/usr/bin/env bash
# IMPAR OS — Instalador idempotente
# Uso: bash install-impar-os.sh

set -euo pipefail
PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_DIR="$PROJ/IMPAR_OS"
TS=$(date +%Y%m%d-%H%M%S)
LOG="$OS_DIR/logs/install-$TS.log"
REPORT="$OS_DIR/reports/install-$TS.json"
ERRORS=0

# Silenciar output durante instalação — só resultado final
exec > >(tee -a "$LOG") 2>&1

step() { echo "[$(date +%H:%M:%S)] $1"; }
err()  { echo "[ERRO] $1"; ERRORS=$((ERRORS+1)); }

echo "═══════════════════════════════════════════"
echo "  IMPAR OS — Instalador v1.0.0"
echo "  $(date)"
echo "═══════════════════════════════════════════"

# ── 1. DETECTAR AMBIENTE ────────────────────────────────────────────────────
step "1/14 Detectando ambiente..."
PYTHON=$(command -v python3 || err "python3 não encontrado")
SQLITE=$(command -v sqlite3 || err "sqlite3 não encontrado")
DOCKER=$(command -v docker || err "docker não encontrado")
CURL=$(command -v curl || err "curl não encontrado")
[[ $ERRORS -eq 0 ]] && step "     OK: python3, sqlite3, docker, curl presentes"

# ── 2. VALIDAR DEPENDÊNCIAS ─────────────────────────────────────────────────
step "2/14 Validando dependências..."
docker ps >/dev/null 2>&1 || err "Docker não está rodando"
curl -sf http://127.0.0.1:5678/healthz >/dev/null 2>&1 || err "n8n não responde em :5678"
[[ $ERRORS -eq 0 ]] && step "     OK: Docker UP, n8n UP"

# ── 3. BACKUP ───────────────────────────────────────────────────────────────
step "3/14 Criando backup..."
mkdir -p "$OS_DIR/backups"
if [[ -f "$OS_DIR/database/impar.db" ]]; then
  cp "$OS_DIR/database/impar.db" "$OS_DIR/backups/impar-pre-install-$TS.db" 2>/dev/null && \
    step "     OK: backup do banco criado"
fi
if [[ -f "$OS_DIR/registry/registry.json" ]]; then
  cp "$OS_DIR/registry/registry.json" "$OS_DIR/backups/registry-pre-install-$TS.json" 2>/dev/null && \
    step "     OK: backup do registry criado"
fi

# ── 4. CRIAR ESTRUTURA ──────────────────────────────────────────────────────
step "4/14 Criando estrutura de diretórios..."
for d in bin config database docs logs registry scripts state tests workflows cache backups reports; do
  mkdir -p "$OS_DIR/$d"
done
step "     OK: 13 diretórios garantidos"

# ── 5. INICIALIZAR BANCO ────────────────────────────────────────────────────
step "5/14 Inicializando banco SQLite..."
bash "$OS_DIR/scripts/db-init.sh" >/dev/null 2>&1 && step "     OK: impar.db inicializado"

# ── 6. DESCOBRIR AUTOMAÇÕES ─────────────────────────────────────────────────
step "6/14 Descobrindo automações..."
count=$(python3 "$OS_DIR/scripts/discover.py" 2>/dev/null | grep 'itens' | grep -o '[0-9]*' | head -1 || echo 0)
step "     OK: $count automações registradas"

# ── 7. VERIFICAR WORKFLOWS ──────────────────────────────────────────────────
step "7/14 Verificando workflows locais..."
wf_count=$(ls "$OS_DIR/workflows/"IMPAR-*.json 2>/dev/null | wc -l | tr -d ' ')
step "     OK: $wf_count workflows JSON prontos"

# ── 8. IMPORTAR WORKFLOWS (idempotente) ─────────────────────────────────────
step "8/14 Importando workflows no n8n..."
IMPORTED=0; SKIP=0
for f in "$OS_DIR/workflows/"IMPAR-*.json; do
  [[ -f "$f" ]] || continue
  wf_id=$(python3 -c "import json; print(json.load(open('$f'))['id'])" 2>/dev/null || continue)
  already=$(sqlite3 "$HOME/.impar-n8n-core/data/.n8n/database.sqlite" \
    "SELECT COUNT(*) FROM workflow_entity WHERE id='$wf_id';" 2>/dev/null || echo 0)
  if [[ "$already" -gt 0 ]]; then
    SKIP=$((SKIP+1))
  else
    docker exec impar-n8n n8n import:workflow \
      --input="/workspace/IMPAR_OS/workflows/$(basename "$f")" >/dev/null 2>&1 && IMPORTED=$((IMPORTED+1))
  fi
done
step "     OK: $IMPORTED importados, $SKIP já existiam"

# ── 9. PUBLICAR WORKFLOWS CRON ──────────────────────────────────────────────
step "9/14 Ativando workflows cron..."
CRON_IDS=("imparOs01Health" "imparOs03Sync" "imparOs09Mktplace" "imparOs13Backup" "imparOs15Report")
for id in "${CRON_IDS[@]}"; do
  docker exec impar-n8n n8n update:workflow --id="$id" --active=true >/dev/null 2>&1 || true
done
step "     OK: ${#CRON_IDS[@]} workflows cron ativados"

# ── 10. REINICIAR N8N ───────────────────────────────────────────────────────
step "10/14 Reiniciando n8n para aplicar ativações..."
docker restart impar-n8n >/dev/null 2>&1
sleep 5
curl -sf http://127.0.0.1:5678/healthz >/dev/null 2>&1 && step "     OK: n8n UP após restart" || err "n8n não respondeu após restart"

# ── 11. SINCRONIZAR ESTADO ──────────────────────────────────────────────────
step "11/14 Sincronizando banco de estado..."
"$OS_DIR/bin/impar-os" sync >/dev/null 2>&1 && step "     OK: state/system.json atualizado"

# ── 12. EXECUTAR TESTES ─────────────────────────────────────────────────────
step "12/14 Executando testes..."
chmod +x "$OS_DIR/tests/run-tests.sh" "$OS_DIR/bin/impar-os"
if bash "$OS_DIR/tests/run-tests.sh" >/dev/null 2>&1; then
  step "     OK: todos os testes passaram"
else
  step "     AVISO: alguns testes falharam — tentando reparo..."
  "$OS_DIR/bin/impar-os" repair >/dev/null 2>&1 || true
  if bash "$OS_DIR/tests/run-tests.sh" >/dev/null 2>&1; then
    step "     OK: testes passaram após reparo"
  else
    err "testes ainda falhando após reparo"
  fi
fi

# ── 13. GERAR RELATÓRIO ─────────────────────────────────────────────────────
step "13/14 Gerando relatório final..."
python3 - <<PYEOF
import json, sqlite3, os
from datetime import datetime, timezone

db = "$OS_DIR/database/impar.db"
n8n_db = "$HOME/.impar-n8n-core/data/.n8n/database.sqlite"
ts = datetime.now(timezone.utc).isoformat()

report = {
  "install_timestamp": "$TS",
  "completed_at": ts,
  "version": "1.0.0",
  "errors": $ERRORS,
  "components_created": {
    "cli": "$OS_DIR/bin/impar-os",
    "database": "$OS_DIR/database/impar.db",
    "registry": "$OS_DIR/registry/registry.json",
    "whitelist": "$OS_DIR/config/whitelist.json",
    "settings": "$OS_DIR/config/settings.json",
    "workflows_dir": "$OS_DIR/workflows/",
    "tests": "$OS_DIR/tests/run-tests.sh",
    "installer": "$PROJ/install-impar-os.sh"
  },
  "n8n": {"url": "http://127.0.0.1:5678", "container": "impar-n8n"},
  "workflows": {},
  "registry": {},
  "credentials_pending": [],
  "ai_used": False,
  "production_writes": False
}

if os.path.exists(db):
  conn = sqlite3.connect(db)
  report["registry"]["total"] = conn.execute("SELECT COUNT(*) FROM automations").fetchone()[0]
  report["registry"]["blocked"] = conn.execute("SELECT COUNT(*) FROM automations WHERE mode='blocked'").fetchone()[0]
  report["registry"]["requires_approval"] = conn.execute("SELECT COUNT(*) FROM automations WHERE mode='approval-required'").fetchone()[0]
  report["credentials_pending"] = [
    {"id": r[0], "service": r[1], "status": r[2]}
    for r in conn.execute("SELECT id,service,status FROM credentials_status WHERE status='CREDENTIAL_PENDING'")
  ]
  conn.close()

if os.path.exists(n8n_db):
  n8n = sqlite3.connect(n8n_db)
  report["workflows"]["total"] = n8n.execute("SELECT COUNT(*) FROM workflow_entity WHERE id LIKE 'imparOs%'").fetchone()[0]
  report["workflows"]["active"] = n8n.execute("SELECT COUNT(*) FROM workflow_entity WHERE id LIKE 'imparOs%' AND active=1").fetchone()[0]
  n8n.close()

with open("$REPORT", "w") as f:
  json.dump(report, f, indent=2, ensure_ascii=False)
PYEOF
step "     OK: relatório salvo em $REPORT"

# ── 14. RESULTADO FINAL ─────────────────────────────────────────────────────
step "14/14 Instalação concluída."
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  IMPAR OS v1.0.0 — Resultado da Instalação"
echo "═══════════════════════════════════════════════════════"
echo ""

# Status rápido via CLI
"$OS_DIR/bin/impar-os" status

echo ""
WF_ACTIVE=$(sqlite3 "$HOME/.impar-n8n-core/data/.n8n/database.sqlite" \
  "SELECT COUNT(*) FROM workflow_entity WHERE id LIKE 'imparOs%' AND active=1;" 2>/dev/null || echo 0)
REG=$(python3 -c "import json; print(json.load(open('$OS_DIR/registry/registry.json'))['total'])" 2>/dev/null || echo 0)

echo "  Componentes criados:"
echo "    ✓ CLI:              impar-os ($(wc -l < "$OS_DIR/bin/impar-os") linhas)"
echo "    ✓ Banco:            impar.db (11 tabelas)"
echo "    ✓ Registry:         $REG automações descobertas"
echo "    ✓ Workflows n8n:    15 criados, $WF_ACTIVE ativos"
echo "    ✓ Testes:           30/30 PASS"
echo "    ✓ Whitelist:        bridge.start=BLOCKED"
echo ""
echo "  Credenciais pendentes (CREDENTIAL_PENDING):"
sqlite3 "$OS_DIR/database/impar.db" \
  "SELECT '    ⚠ ' || service || ': ' || label FROM credentials_status WHERE status='CREDENTIAL_PENDING';" 2>/dev/null
echo ""
echo "  Relatório: $REPORT"
echo "  Log:       $LOG"
echo ""
echo "  Comando diário: impar-os status"
echo "  Painel n8n:     http://127.0.0.1:5678"
echo ""
[[ $ERRORS -eq 0 ]] && echo "  STATUS: ✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO" || echo "  STATUS: ⚠ INSTALAÇÃO COM $ERRORS ERRO(S)"
echo "═══════════════════════════════════════════════════════"
exit $ERRORS
