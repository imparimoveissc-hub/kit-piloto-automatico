#!/usr/bin/env bash
# kos-register-skill.sh — registra nova skill/automação no KOS
# Executa após criar qualquer nova skill, rotina ou automação.
# Atualiza: registry.yaml → index.json → brain/_INDEX.md
#
# Uso interativo: bash kos-register-skill.sh
# Uso direto:     bash kos-register-skill.sh --id minha-skill --modulo leads --desc "descrição"

set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGISTRY="$KIT_DIR/00_OS/kos/registry.yaml"
BRAIN_INDEX="$KIT_DIR/00_OS/kos/brain/_INDEX.md"
BUILD_INDEX="$KIT_DIR/00_OS/kos/build-index.py"
BRAIN_DIR="$KIT_DIR/00_OS/kos/brain"

echo ""
echo "=== KOS Register Skill/Automação ==="
echo "Kit: $KIT_DIR"
echo ""

# ── Modo direto (flags) ────────────────────────────────────────────────────────
ID=""
MODULO=""
DESC=""
STATUS="ativo"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --id)    ID="$2";     shift 2 ;;
        --modulo) MODULO="$2"; shift 2 ;;
        --desc)  DESC="$2";   shift 2 ;;
        --status) STATUS="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# ── Modo interativo ────────────────────────────────────────────────────────────
if [ -z "$ID" ]; then
    echo "Qual é o ID da skill/automação? (ex: impar-nova-skill, leads-followup-d7)"
    read -r ID
fi

if [ -z "$MODULO" ]; then
    echo ""
    echo "Qual módulo KOS? marketplace | leads | sistema | nfse | contratos | followup | novo"
    read -r MODULO
fi

if [ -z "$DESC" ]; then
    echo ""
    echo "Descrição em uma linha:"
    read -r DESC
fi

echo ""
echo "Arquivo principal (caminho relativo ao kit, ou deixe em branco):"
read -r ARQUIVO_PRINCIPAL

echo ""
echo "Tipo: skill | rotina | automacao | launchagent | task"
read -r TIPO

echo ""
echo "Triggers (palavras que o usuário diz para acionar, separadas por vírgula):"
read -r TRIGGERS

echo ""
echo "Status: ativo | pausado | desenvolvimento | desativado [Enter = ativo]"
read -r STATUS_INPUT
[ -n "$STATUS_INPUT" ] && STATUS="$STATUS_INPUT"

# ── Criar entrada no registry.yaml ────────────────────────────────────────────
echo ""
echo "📝 Adicionando ao registry.yaml ..."

# Montar bloco YAML da nova entrada
HOJE=$(date +%Y-%m-%d)
ARQUIVO_LINHA=""
[ -n "$ARQUIVO_PRINCIPAL" ] && ARQUIVO_LINHA="      - $ARQUIVO_PRINCIPAL"
TRIGGERS_YAML=""
IFS=',' read -ra TRIG_ARR <<< "$TRIGGERS"
for t in "${TRIG_ARR[@]}"; do
    t_trimmed="$(echo "$t" | xargs)"
    TRIGGERS_YAML="${TRIGGERS_YAML}      - \"$t_trimmed\"\n"
done

YAML_BLOCK="
  ${ID}:
    name: ${ID}
    description: ${DESC}
    status: ${STATUS}
    tipo: ${TIPO}
    criticidade: media
    brain: ${BRAIN_DIR}/${MODULO^}.md
    arquivos_principais:
${ARQUIVO_LINHA}
    triggers_usuario:
$(printf '%b' "$TRIGGERS_YAML")    ultima_alteracao: ${HOJE}
"

# Adicionar ao final do registry.yaml
printf '%b' "$YAML_BLOCK" >> "$REGISTRY"
echo "   ✅ Entrada '${ID}' adicionada ao registry.yaml"

# ── Atualizar _INDEX.md do Brain ───────────────────────────────────────────────
echo ""
echo "📖 Atualizando Brain _INDEX.md ..."
echo "" >> "$BRAIN_INDEX"
echo "| ${ID} | ${MODULO} | ${DESC} | ${STATUS} | ${HOJE} |" >> "$BRAIN_INDEX"
echo "   ✅ Linha adicionada ao _INDEX.md"

# ── Criar template de Brain note (se módulo novo) ─────────────────────────────
BRAIN_FILE="$BRAIN_DIR/${MODULO^}.md"
if [ ! -f "$BRAIN_FILE" ] && [ "$MODULO" != "marketplace" ] && [ "$MODULO" != "leads" ] && \
   [ "$MODULO" != "sistema" ] && [ "$MODULO" != "nfse" ] && [ "$MODULO" != "contratos" ] && \
   [ "$MODULO" != "followup" ]; then
    echo ""
    echo "🆕 Módulo novo detectado — criando Brain note template em brain/${MODULO^}.md ..."
    cat > "$BRAIN_FILE" << MDEOF
---
tipo: brain
modulo: ${MODULO^}
status: ${STATUS}
criticidade: media
atualizado: ${HOJE}
---

# ${MODULO^} — ${DESC}

> [!info] Status: ${STATUS}
> Módulo criado em ${HOJE}.

## O que o sistema faz

[A PREENCHER]

## Arquivos principais

- \`${ARQUIVO_PRINCIPAL}\`

## Como acionar

| O que você quer | O que dizer |
|-----------------|-------------|
$(for t in "${TRIG_ARR[@]}"; do echo "| [A PREENCHER] | \"$(echo "$t" | xargs)\" |"; done)

## Logs

[A PREENCHER]

## Problemas conhecidos

[Nenhum registrado ainda]

## Ver também

- [[00 - Índice Brain]] — voltar ao índice
MDEOF
    echo "   ✅ Brain note criada: $BRAIN_FILE"
    echo "   → Complete os campos [A PREENCHER] para ativar a nota"
fi

# ── Regenerar index.json ───────────────────────────────────────────────────────
echo ""
echo "🔄 Regenerando index.json ..."
python3 "$BUILD_INDEX"

# ── Sincronizar Desktop KOS-V30 (se existir) ──────────────────────────────────
DESKTOP_KOS="$HOME/Desktop/KOS-V30"
if [ -d "$DESKTOP_KOS" ]; then
    echo ""
    echo "📂 Sincronizando ~/Desktop/KOS-V30/ ..."
    cp "$REGISTRY" "$DESKTOP_KOS/registry.yaml"
    cp "$BUILD_INDEX" "$DESKTOP_KOS/build-index.py"
    cp "$BRAIN_INDEX" "$DESKTOP_KOS/brain/_INDEX.md"
    [ -f "$BRAIN_FILE" ] && cp "$BRAIN_FILE" "$DESKTOP_KOS/brain/$(basename "$BRAIN_FILE")"
    echo "   ✅ KOS-V30 atualizado"
fi

echo ""
echo "=== Registro concluído ==="
echo "Skill '${ID}' adicionada ao módulo '${MODULO}'."
echo ""
echo "Próximos passos:"
echo "  1. Revise a entrada em: $REGISTRY"
[ ! -f "$BRAIN_FILE" ] || echo "  2. Complete os campos [A PREENCHER] em: $BRAIN_FILE"
echo "  3. Atualize o Brain module se houver mudanças estruturais"
