#!/bin/bash
# Wrapper: sincroniza browser-profile iCloud ↔ local antes/depois da varredura.
# Python 3.9 (CommandLineTools) não acessa iCloud em LaunchAgents; bash/cp tem acesso.

ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
LOCAL_DIR="$HOME/.local/impar-automation/messenger"
ICLOUD_PROFILE="$ICLOUD/05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-profile"
LOCAL_PROFILE="$LOCAL_DIR/browser-profile"
LOG="$LOCAL_DIR/varredura-wrapper.log"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

# Lock: evita execuções paralelas
LOCK="$LOCAL_DIR/.varredura.lock"
if [ -f "$LOCK" ]; then
    PID=$(cat "$LOCK" 2>/dev/null)
    if kill -0 "$PID" 2>/dev/null; then
        echo "[$(ts)] Já rodando (PID=$PID) — saindo" >> "$LOG"
        exit 0
    fi
    rm -f "$LOCK"
fi
echo $$ > "$LOCK"
trap "rm -f '$LOCK'" EXIT

echo "[$(ts)] run_varredura.sh iniciado" >> "$LOG"

# Sync cookies/sessão iCloud → local (exclui Cache — não é necessário para sessão)
sync_profile() {
    local SRC="$1" DST="$2"
    if [ ! -d "$SRC" ]; then return 0; fi
    mkdir -p "$DST"
    # Copia apenas arquivos de sessão: Cookies, Local Storage, Session Storage, IndexedDB
    for subdir in Default/Cookies "Default/Local Storage" "Default/Session Storage" \
                  Default/IndexedDB Default/Login\ Data Default/Network Default/Preferences \
                  Default/Secure\ Preferences Default/Extension\ State; do
        local s="$SRC/$subdir"
        local d="$DST/$subdir"
        [ -e "$s" ] || continue
        mkdir -p "$(dirname "$d")"
        /bin/cp -Rp "$s" "$(dirname "$d")/" 2>/dev/null
    done
}

if [ -d "$ICLOUD_PROFILE" ]; then
    sync_profile "$ICLOUD_PROFILE" "$LOCAL_PROFILE" && \
        echo "[$(ts)] Profile sessão iCloud→local OK" >> "$LOG" || \
        echo "[$(ts)] AVISO: sync iCloud→local falhou — usando cópia anterior" >> "$LOG"
else
    echo "[$(ts)] AVISO: perfil iCloud não encontrado — usando local" >> "$LOG"
fi

# Executa varredura
/usr/bin/python3 "$LOCAL_DIR/varredura_inbox.py"
EXIT=$?

# Sync cookies/sessão local → iCloud (preserva sessão renovada, exclui Cache)
if [ -d "$LOCAL_PROFILE" ]; then
    sync_profile "$LOCAL_PROFILE" "$ICLOUD_PROFILE" && \
        echo "[$(ts)] Profile sessão local→iCloud OK (exit=$EXIT)" >> "$LOG" || \
        echo "[$(ts)] AVISO: sync local→iCloud falhou" >> "$LOG"
fi

exit $EXIT
