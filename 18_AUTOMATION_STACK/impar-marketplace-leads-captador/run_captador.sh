#!/bin/bash
# Wrapper: roda capturar_lead_messenger.py via Playwright (sessão autenticada do browser).
# Fluxo: Marketplace Inbox (browser) → CSV local → Telegram.
# Nota: marketplace_leads_captador.py (Graph API) fica como fallback quando o token FB for renovado.

LOCAL_DIR="$HOME/.local/impar-automation/marketplace-leads"
LOG="$LOCAL_DIR/wrapper.log"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

# Lock: evita execuções paralelas
LOCK="$LOCAL_DIR/.lock"
if [ -f "$LOCK" ]; then
    PID=$(cat "$LOCK" 2>/dev/null)
    if kill -0 "$PID" 2>/dev/null; then
        echo "[$(ts)] Outra instância rodando (PID=$PID) — saindo" >> "$LOG"
        exit 0
    fi
fi
echo $$ > "$LOCK"
trap "rm -f '$LOCK'" EXIT

# Lock cruzado: captador e varredura_inbox.py compartilham o mesmo browser-profile
# (Chromium SingletonLock trava se os dois abrirem o perfil ao mesmo tempo).
VARREDURA_LOCK="$HOME/.local/impar-automation/messenger/.varredura.lock"
WAITED=0
while [ -f "$VARREDURA_LOCK" ] && [ "$WAITED" -lt 60 ]; do
    VPID=$(awk 'NR==1 {print $1}' "$VARREDURA_LOCK" 2>/dev/null)
    if ! kill -0 "$VPID" 2>/dev/null; then
        break
    fi
    sleep 3
    WAITED=$((WAITED + 3))
done

echo "[$(ts)] run_captador.sh iniciado" >> "$LOG"

# Sincroniza .env do iCloud (evita PermissionError em LaunchAgents)
ICLOUD_ENV="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/18_AUTOMATION_STACK/facebook-mcp/.env"
if [ -f "$ICLOUD_ENV" ]; then
    cp "$ICLOUD_ENV" "$LOCAL_DIR/.env" 2>/dev/null && echo "[$(ts)] .env sincronizado do iCloud" >> "$LOG"
fi

# Executa captador via Playwright (detecção por div — sem depender de <a href>)
/usr/bin/python3 "$LOCAL_DIR/capturar_lead_messenger.py" >> "$LOG" 2>&1
EXIT_CODE=$?

echo "[$(ts)] Captador finalizado (exit=$EXIT_CODE)" >> "$LOG"
exit $EXIT_CODE
