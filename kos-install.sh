#!/usr/bin/env bash
# kos-install.sh — instala componentes máquina-específicos do KOS V30
# Roda em qualquer Mac que tenha o kit sincronizado via iCloud.
# Idempotente: seguro executar múltiplas vezes.
#
# Uso: bash /caminho/para/kit/kos-install.sh
# Guia Obsidian nova máquina: 00_OS/kos/OBSIDIAN-NOVA-MAQUINA.md

set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo ""
echo "=== KOS Install — Kit Piloto Automático V30 ==="
echo "Kit:  $KIT_DIR"
echo "Home: $HOME"
echo ""

# ── [1/5] Diretórios locais ────────────────────────────────────────────────────
echo "[1/5] Criando diretórios locais em ~/.local/impar-automation/ ..."
mkdir -p \
    "$HOME/.local/impar-automation/marketplace" \
    "$HOME/.local/impar-automation/chaves-na-mao" \
    "$HOME/.local/impar-automation/leads-planilha" \
    "$HOME/.local/impar-automation/messenger" \
    "$HOME/.local/impar-automation/atende-leads" \
    "$HOME/.local/impar-automation/nfem"
echo "   ✅ Diretórios criados"

# ── [2/5] Leads watcher ───────────────────────────────────────────────────────
echo ""
echo "[2/5] Instalando leads_watcher.py ..."
WATCHER_SRC="$KIT_DIR/18_AUTOMATION_STACK/impar-leads-planilha-watcher/leads_watcher.py"
WATCHER_DST="$HOME/.local/impar-automation/leads-planilha/leads_watcher.py"

if [ -f "$WATCHER_SRC" ]; then
    cp "$WATCHER_SRC" "$WATCHER_DST"
    chmod +x "$WATCHER_DST"
    echo "   ✅ leads_watcher.py → $WATCHER_DST"
else
    echo "   ⚠️  AVISO: $WATCHER_SRC não encontrado — pulando"
fi

# ── [3/5] LaunchAgent: leads-planilha-watcher ─────────────────────────────────
echo ""
echo "[3/5] Configurando LaunchAgent com.impar.leads-planilha-watcher ..."
PLIST_TEMPLATE="$KIT_DIR/18_AUTOMATION_STACK/impar-leads-planilha-watcher/com.impar.leads-planilha-watcher.plist.template"
PLIST_DST="$HOME/Library/LaunchAgents/com.impar.leads-planilha-watcher.plist"

if [ -f "$PLIST_TEMPLATE" ]; then
    sed "s|HOME_PLACEHOLDER|$HOME|g" "$PLIST_TEMPLATE" > "$PLIST_DST"
    launchctl unload "$PLIST_DST" 2>/dev/null || true
    launchctl load "$PLIST_DST"
    echo "   ✅ LaunchAgent carregado: $PLIST_DST"
else
    echo "   ⚠️  AVISO: template plist não encontrado — pulando"
fi

# ── [4/5] Obsidian vault ──────────────────────────────────────────────────────
echo ""
echo "[4/5] Configurando vault do Obsidian ..."
VAULT="$KIT_DIR/Cofre-Obsidian"
OBSIDIAN_APP="/Applications/Obsidian.app"
OBSIDIAN_CFG="$HOME/Library/Application Support/obsidian"

if [ ! -d "$OBSIDIAN_APP" ]; then
    echo "   ⚠️  Obsidian não encontrado em /Applications/Obsidian.app"
    echo "   → Baixe em https://obsidian.md e instale antes de continuar."
    echo "   → Depois rode este script novamente para concluir o passo 4."
else
    # Criar .obsidian/ com config mínima
    mkdir -p "$VAULT/.obsidian"

    if [ ! -f "$VAULT/.obsidian/app.json" ]; then
        cat > "$VAULT/.obsidian/app.json" << 'JSON'
{
  "alwaysUpdateLinks": true,
  "newFileLocation": "current",
  "attachmentFolderPath": "Assets",
  "useMarkdownLinks": false,
  "newLinkFormat": "shortest",
  "readableLineLength": true,
  "strictLineBreaks": false,
  "foldHeading": true,
  "foldIndent": true
}
JSON
    fi

    if [ ! -f "$VAULT/.obsidian/appearance.json" ]; then
        cat > "$VAULT/.obsidian/appearance.json" << 'JSON'
{
  "theme": "obsidian",
  "translucency": false
}
JSON
    fi

    if [ ! -f "$VAULT/.obsidian/workspace.json" ]; then
        cat > "$VAULT/.obsidian/workspace.json" << 'JSON'
{
  "main": {
    "id": "brain-main",
    "type": "split",
    "children": [
      {
        "id": "brain-leaf",
        "type": "leaf",
        "state": {
          "type": "markdown",
          "state": {
            "file": "KPA30/Brain/00 - Índice Brain.md",
            "mode": "preview",
            "source": false
          }
        }
      }
    ],
    "direction": "vertical"
  },
  "left": {
    "id": "left-sidebar",
    "type": "split",
    "children": [
      {
        "id": "file-explorer",
        "type": "tabs",
        "children": [
          {
            "id": "file-explorer-leaf",
            "type": "leaf",
            "state": { "type": "file-explorer", "state": {} }
          }
        ]
      }
    ],
    "direction": "horizontal",
    "width": 260
  },
  "right": {
    "id": "right-sidebar",
    "type": "split",
    "children": [],
    "direction": "horizontal",
    "width": 0
  },
  "active": "brain-leaf",
  "lastOpenFiles": [
    "KPA30/Brain/00 - Índice Brain.md",
    "KPA30/Brain/Marketplace.md",
    "KPA30/Brain/Leads.md",
    "KPA30/Brain/Sistema.md",
    "KPA30/Brain/NFS-e.md",
    "KPA30/Brain/Contratos.md",
    "KPA30/00 - Índice KPA30.md"
  ]
}
JSON
    fi

    # Registrar vault no Obsidian (só se ainda não registrado)
    mkdir -p "$OBSIDIAN_CFG"
    if [ ! -f "$OBSIDIAN_CFG/obsidian.json" ]; then
        VAULT_ID=$(openssl rand -hex 8)
        TS=$(python3 -c "import time; print(int(time.time() * 1000))")
        cat > "$OBSIDIAN_CFG/obsidian.json" << JSON
{
  "vaults": {
    "${VAULT_ID}": {
      "path": "${VAULT}",
      "ts": ${TS},
      "open": true
    }
  },
  "updateDisabled": false,
  "hasOtherAppsRunning": false
}
JSON
        echo "   ✅ Vault registrado (ID: ${VAULT_ID})"
    else
        echo "   ℹ️  obsidian.json já existe — vault provavelmente já registrado"
    fi

    # Teste: verificar que .obsidian/ foi criado
    if [ -d "$VAULT/.obsidian" ]; then
        echo "   ✅ Vault configurado: $VAULT"
        echo "   → Abra o Obsidian para ativar o vault"
        echo "   → Guia completo: $KIT_DIR/00_OS/kos/OBSIDIAN-NOVA-MAQUINA.md"
    else
        echo "   ❌ Falha ao criar .obsidian/ — verificar permissões"
    fi
fi

# ── [5/5] Gerar KOS Index + Injetar cabeçalho nas tasks/skills ───────────────
echo ""
echo "[5/5] Gerando KOS index e injetando cabeçalho KOS nas tasks/skills ..."
BUILD_INDEX="$KIT_DIR/00_OS/kos/build-index.py"
INJECT="$KIT_DIR/00_OS/kos/inject-kos-header.py"

if [ -f "$BUILD_INDEX" ]; then
    python3 "$BUILD_INDEX"
else
    echo "   ⚠️  build-index.py não encontrado — pulando"
fi

if [ -f "$INJECT" ]; then
    echo ""
    python3 "$INJECT"
else
    echo "   ⚠️  inject-kos-header.py não encontrado — pulando"
fi

# ── Verificação final ─────────────────────────────────────────────────────────
echo ""
echo "=== KOS instalado com sucesso ==="
echo ""
echo "Brain (Claude):        $KIT_DIR/00_OS/kos/brain/"
echo "Brain (Obsidian):      $KIT_DIR/Cofre-Obsidian/KPA30/Brain/"
echo "Token Policy:          $KIT_DIR/00_OS/kos/token-policy.md"
echo "Registry:              $KIT_DIR/00_OS/kos/registry.yaml"
echo "Index:                 $KIT_DIR/00_OS/kos/index.json"
echo "Watcher de leads:      $WATCHER_DST"
echo "Guia Obsidian:         $KIT_DIR/00_OS/kos/OBSIDIAN-NOVA-MAQUINA.md"
echo ""
echo "Confirme que o CLAUDE.md referencia 00_OS/kos/token-policy.md"
echo "na seção de Inicialização (passo 8)."
