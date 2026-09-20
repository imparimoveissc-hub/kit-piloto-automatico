#!/bin/bash
# Wrapper: sincroniza browser-profile iCloud ↔ local antes/depois da varredura.
# Python 3.9 (CommandLineTools) não acessa iCloud em LaunchAgents; bash/cp tem acesso.

ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
LOCAL_DIR="$HOME/.local/impar-automation/messenger"
ICLOUD_PROFILE="$ICLOUD/05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-profile"
LOCAL_PROFILE="$LOCAL_DIR/browser-profile"
LOG="$LOCAL_DIR/varredura-wrapper.log"
ACCOUNT_ID="${IMPAR_ACCOUNT_ID:-jonata}"
LOCK_MAX_AGE_SECONDS="${IMPAR_LOCK_MAX_AGE_SECONDS:-900}"
VARREDURA_TIMEOUT_SECONDS="${IMPAR_VARREDURA_TIMEOUT_SECONDS:-240}"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

# Lock: evita execuções paralelas
LOCK="$LOCAL_DIR/.varredura.lock"
if [ -f "$LOCK" ]; then
    PID=$(awk 'NR==1 {print $1}' "$LOCK" 2>/dev/null)
    START_TS=$(awk 'NR==2 {print $1}' "$LOCK" 2>/dev/null)
    NOW_TS=$(date +%s)
    AGE=$(( NOW_TS - ${START_TS:-0} ))
    if kill -0 "$PID" 2>/dev/null; then
        if [ "$AGE" -gt "$LOCK_MAX_AGE_SECONDS" ]; then
            echo "[$(ts)] Lock antigo (${AGE}s, PID=$PID) — removendo e seguindo" >> "$LOG"
            rm -f "$LOCK"
        else
            echo "[$(ts)] Já rodando (PID=$PID, ${AGE}s) — saindo" >> "$LOG"
            exit 0
        fi
    else
        echo "[$(ts)] Lock órfão removido (PID=$PID)" >> "$LOG"
        rm -f "$LOCK"
    fi
fi
printf "%s\n%s\n%s\n" "$$" "$(date +%s)" "$ACCOUNT_ID" > "$LOCK"
trap "rm -f '$LOCK'" EXIT

# Lock cruzado: varredura e capturar_lead_messenger.py compartilham o mesmo browser-profile
# (Chromium SingletonLock trava se os dois abrirem o perfil ao mesmo tempo).
CAPTADOR_LOCK="$HOME/.local/impar-automation/marketplace-leads/.lock"
WAITED_X=0
while [ -f "$CAPTADOR_LOCK" ] && [ "$WAITED_X" -lt 60 ]; do
    CPID=$(cat "$CAPTADOR_LOCK" 2>/dev/null)
    if ! kill -0 "$CPID" 2>/dev/null; then
        break
    fi
    sleep 3
    WAITED_X=$((WAITED_X + 3))
done

echo "[$(ts)] run_varredura.sh iniciado (account=$ACCOUNT_ID)" >> "$LOG"

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

# Sync iCloud→local SOMENTE se local não tiver sessão válida (Cookies ausente ou vazio)
LOCAL_COOKIES="$LOCAL_PROFILE/Default/Cookies"
LOCAL_COOKIES_SIZE=0
[ -f "$LOCAL_COOKIES" ] && LOCAL_COOKIES_SIZE=$(stat -f%z "$LOCAL_COOKIES" 2>/dev/null || echo 0)

if [ "$LOCAL_COOKIES_SIZE" -lt 4096 ] && [ -d "$ICLOUD_PROFILE" ]; then
    sync_profile "$ICLOUD_PROFILE" "$LOCAL_PROFILE" && \
        echo "[$(ts)] Profile sessão iCloud→local OK (local ausente/vazio)" >> "$LOG" || \
        echo "[$(ts)] AVISO: sync iCloud→local falhou — usando cópia anterior" >> "$LOG"
else
    echo "[$(ts)] Profile local OK (${LOCAL_COOKIES_SIZE}B) — skip iCloud→local" >> "$LOG"
fi

# Executa varredura com limite de tempo. Se o Facebook travar, o proximo ciclo roda.
/usr/bin/python3 -u "$LOCAL_DIR/varredura_inbox.py" &
CHILD_PID=$!
WAITED=0
EXIT=0
while kill -0 "$CHILD_PID" 2>/dev/null; do
    if [ "$WAITED" -ge "$VARREDURA_TIMEOUT_SECONDS" ]; then
        echo "[$(ts)] Timeout da varredura (${VARREDURA_TIMEOUT_SECONDS}s) — encerrando PID=$CHILD_PID" >> "$LOG"
        kill "$CHILD_PID" 2>/dev/null || true
        sleep 2
        kill -9 "$CHILD_PID" 2>/dev/null || true
        wait "$CHILD_PID" 2>/dev/null || true
        EXIT=124
        break
    fi
    sleep 5
    WAITED=$((WAITED + 5))
done
if [ "$EXIT" = "0" ]; then
    wait "$CHILD_PID"
    EXIT=$?
fi

# Sync cookies/sessão local → iCloud (preserva sessão renovada, exclui Cache)
if [ -d "$LOCAL_PROFILE" ]; then
    sync_profile "$LOCAL_PROFILE" "$ICLOUD_PROFILE" && \
        echo "[$(ts)] Profile sessão local→iCloud OK (exit=$EXIT)" >> "$LOG" || \
        echo "[$(ts)] AVISO: sync local→iCloud falhou" >> "$LOG"
fi

exit $EXIT
