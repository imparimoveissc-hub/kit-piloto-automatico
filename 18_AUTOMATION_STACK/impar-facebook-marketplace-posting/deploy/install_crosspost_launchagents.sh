#!/bin/bash
# install_crosspost_launchagents.sh
# Instala os 3 LaunchAgents de crosspost de grupos do Facebook.
# Substitui PLACEHOLDER_SCRIPT_PATH pelo caminho real do script e registra no launchd.
#
# Uso:
#   cd 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/deploy
#   bash install_crosspost_launchagents.sh

set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_DIR="$(dirname "$DEPLOY_DIR")"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"
LOGS_DIR="$HOME/Library/Logs"

PLISTS=(
    "com.impar.marketplace-crosspost-manha"
    "com.impar.marketplace-crosspost-tarde"
    "com.impar.marketplace-crosspost-noite"
)

mkdir -p "$LAUNCHAGENTS_DIR"
mkdir -p "$LOGS_DIR"
chmod +x "$SCRIPT_DIR/run_crosspost.sh"

echo "Diretorio do script: $SCRIPT_DIR"
echo "Usuario: $(whoami) | HOME: $HOME"
echo ""

for LABEL in "${PLISTS[@]}"; do
    SRC="$DEPLOY_DIR/${LABEL}.plist"
    DST="$LAUNCHAGENTS_DIR/${LABEL}.plist"

    if [ ! -f "$SRC" ]; then
        echo "ERRO: Nao encontrado: $SRC"
        continue
    fi

    # Substitui placeholder pelo caminho real e pelo usuario real
    sed \
        -e "s|PLACEHOLDER_SCRIPT_PATH|${SCRIPT_DIR}|g" \
        -e "s|/Users/usuario|${HOME}|g" \
        "$SRC" > "$DST"

    # Descarrega versao anterior se existir
    if launchctl list | grep -q "$LABEL" 2>/dev/null; then
        launchctl unload "$DST" 2>/dev/null || true
        echo "[$LABEL] Versao anterior descarregada."
    fi

    # Carrega
    launchctl load -w "$DST"
    echo "[$LABEL] Instalado e carregado. OK"
done

echo ""
echo "Verificacao:"
for LABEL in "${PLISTS[@]}"; do
    STATUS=$(launchctl list | grep "$LABEL" || echo "(nao encontrado)")
    echo "  $STATUS"
done

echo ""
echo "Logs disponiveis em:"
echo "  tail -f $LOGS_DIR/impar-crosspost-manha.log"
echo "  tail -f $LOGS_DIR/impar-crosspost-tarde.log"
echo "  tail -f $LOGS_DIR/impar-crosspost-noite.log"
echo ""
echo "Para forcar execucao agora (teste):"
echo "  launchctl start com.impar.marketplace-crosspost-manha"
echo ""
echo "Para remover os LaunchAgents:"
echo "  launchctl unload ~/Library/LaunchAgents/com.impar.marketplace-crosspost-*.plist"
echo "  rm ~/Library/LaunchAgents/com.impar.marketplace-crosspost-*.plist"
