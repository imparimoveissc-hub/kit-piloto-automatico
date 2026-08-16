#!/usr/bin/env bash
# post-task-hook.sh — KOS Fase 3: Autoaprendizado pós-task
# Chamado pelo Claude ao final de qualquer task que altere uma automação, skill ou configuração.
# Atualiza lastModified no Brain module, regenera index.json e registra em kos-updates.log
#
# Uso: bash 00_OS/kos/post-task-hook.sh <modulo> [descricao_da_mudanca]
# Ex:  bash 00_OS/kos/post-task-hook.sh marketplace "adicionado novo grupo ao CSV"
# Ex:  bash 00_OS/kos/post-task-hook.sh leads "checkpoint.json resetado por duplicata"
#
# Módulos válidos: marketplace | leads | sistema | nfse | contratos | followup | geral

set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BRAIN_DIR="$KIT_DIR/00_OS/kos/brain"
REGISTRY="$KIT_DIR/00_OS/kos/registry.yaml"
BUILD_INDEX="$KIT_DIR/00_OS/kos/build-index.py"
LOG="$KIT_DIR/07_LOGS/kos-updates.log"
DESKTOP_KOS="$HOME/Desktop/KOS-V30"

MODULE="${1:-geral}"
CHANGE_DESC="${2:-atualização sem descrição}"
TODAY=$(date +%Y-%m-%d)
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# ── 1. Atualizar lastModified no Brain module ─────────────────────────────────
# Capitaliza primeira letra do módulo para corresponder ao nome do arquivo
MODULE_CAP="$(echo "${MODULE:0:1}" | tr '[:lower:]' '[:upper:]')${MODULE:1}"

BRAIN_FILE="$BRAIN_DIR/${MODULE_CAP}.md"

if [ -f "$BRAIN_FILE" ]; then
    # Substitui a linha "atualizado:" no frontmatter
    sed -i '' "s/^atualizado: .*/atualizado: ${TODAY}/" "$BRAIN_FILE"
    echo "[post-task] ✅ Brain/${MODULE_CAP}.md — lastModified → ${TODAY}"
else
    echo "[post-task] ⚠️  Brain module não encontrado: $BRAIN_FILE (módulo: ${MODULE_CAP})"
    echo "[post-task]    Use kos-register-skill.sh para criar um módulo novo."
fi

# ── 1b. Atualizar current-state.md do módulo ─────────────────────────────────
STATE_FILE="$BRAIN_DIR/${MODULE_CAP}.current-state.md"
if [ -f "$STATE_FILE" ]; then
    sed -i '' "s/^atualizado: .*/atualizado: ${TODAY}/" "$STATE_FILE"
    sed -i '' "s|^ultima_mudanca:.*|ultima_mudanca: \"${CHANGE_DESC}\"|" "$STATE_FILE"
    echo "[post-task] ✅ ${MODULE_CAP}.current-state.md → atualizado"
fi

# ── 2. Atualizar registry.yaml — campo ultima_alteracao do módulo ─────────────
if grep -q "^  ${MODULE}:" "$REGISTRY" 2>/dev/null; then
    # Substitui a linha ultima_alteracao dentro do bloco do módulo
    python3 - "$REGISTRY" "$MODULE" "$TODAY" << 'PYEOF'
import sys, re

registry_path = sys.argv[1]
module = sys.argv[2]
today = sys.argv[3]

with open(registry_path, encoding='utf-8') as f:
    content = f.read()

# Encontrar o bloco do módulo e atualizar apenas a sua ultima_alteracao
# Substitui a primeira ocorrência de ultima_alteracao após o marcador do módulo
pattern = rf'(  {re.escape(module)}:.*?ultima_alteracao: )\d{{4}}-\d{{2}}-\d{{2}}'
updated = re.sub(pattern, rf'\g<1>{today}', content, count=1, flags=re.DOTALL)

with open(registry_path, 'w', encoding='utf-8') as f:
    f.write(updated)

print(f"[post-task] ✅ registry.yaml — módulo '{module}' ultima_alteracao → {today}")
PYEOF
else
    echo "[post-task] ℹ️  Módulo '${MODULE}' não encontrado no registry.yaml — pulando update do registry"
fi

# ── 3. Regenerar index.json ────────────────────────────────────────────────────
echo "[post-task] 🔄 Regenerando index.json ..."
python3 "$BUILD_INDEX" 2>&1 | grep -E "(✅|⚠️|funções|tasks|Agentes)" || true

# ── 4. Sincronizar Desktop KOS-V30 (se existir) ───────────────────────────────
if [ -d "$DESKTOP_KOS" ]; then
    cp "$REGISTRY" "$DESKTOP_KOS/registry.yaml" 2>/dev/null || true
    cp "$BRAIN_DIR/_INDEX.md" "$DESKTOP_KOS/brain/_INDEX.md" 2>/dev/null || true
    [ -f "$BRAIN_FILE" ] && cp "$BRAIN_FILE" "$DESKTOP_KOS/brain/${MODULE_CAP}.md" 2>/dev/null || true
    echo "[post-task] 📂 Desktop/KOS-V30 sincronizado"
fi

# ── 5. Registrar em kos-updates.log ───────────────────────────────────────────
mkdir -p "$(dirname "$LOG")"
echo "[${NOW}] módulo=${MODULE} | mudança=${CHANGE_DESC}" >> "$LOG"
echo "[post-task] 📋 Registrado em 07_LOGS/kos-updates.log"

echo ""
echo "[post-task] Concluído. Módulo: ${MODULE} | ${CHANGE_DESC}"
