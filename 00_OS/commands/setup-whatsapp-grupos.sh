#!/bin/bash
# ============================================================
# setup-whatsapp-grupos.sh
# Aplica configurações de WhatsApp (grupos + números) no kit
# Uso: bash setup-whatsapp-grupos.sh
# Data: 2026-08-03
# ============================================================

set -e

KIT_ROOT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
TASKS_DIR="$HOME/.claude/scheduled-tasks"

echo "🔧 Iniciando setup WhatsApp grupos — Impar Imóveis"
echo "Kit: $KIT_ROOT"
echo ""

# ── NÚMEROS ──────────────────────────────────────────────────
# Impar Imóveis (WhatsApp Desktop agora é esta conta)
IMPAR_WA="5547920026017"
# Jonata pessoal (recebe notificações do gerente digital)
JONATA_WA="5547996876631"

# ── GRUPOS ───────────────────────────────────────────────────
GRUPO_LEADS="NOVOS LEADS"
GRUPO_FOLLOWUP="FOLLOW UP IMPAR"

# ── COORDENADA CAMPO DE MENSAGEM (WhatsApp Desktop 1440x791)──
CLICK_X=900
CLICK_Y=795

echo "📱 Números configurados:"
echo "   Impar Imóveis : $IMPAR_WA"
echo "   Jonata pessoal: $JONATA_WA"
echo "   Grupo leads   : $GRUPO_LEADS"
echo "   Grupo followup: $GRUPO_FOLLOWUP"
echo "   Click campo   : ($CLICK_X, $CLICK_Y)"
echo ""

# ── 1. leads_watcher.py (gerente digital → Jonata pessoal) ───
WATCHER="$KIT_ROOT/18_AUTOMATION_STACK/impar-leads-planilha-watcher/leads_watcher.py"
if [ -f "$WATCHER" ]; then
    sed -i '' "s/IMPAR_IMOVEIS = \"[0-9]*\"/IMPAR_IMOVEIS = \"$JONATA_WA\"/" "$WATCHER"
    echo "✅ leads_watcher.py → Jonata $JONATA_WA"
else
    echo "⚠️  leads_watcher.py não encontrado em $WATCHER"
fi

# ── 2. varredura_inbox.py (marketplace → grupo NOVOS LEADS) ──
VARREDURA="$KIT_ROOT/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/varredura_inbox.py"
if [ -f "$VARREDURA" ]; then
    sed -i '' "s/GRUPO_LEADS = \"[^\"]*\"/GRUPO_LEADS = \"$GRUPO_LEADS\"/" "$VARREDURA"
    echo "✅ varredura_inbox.py → grupo '$GRUPO_LEADS'"
else
    echo "⚠️  varredura_inbox.py não encontrado"
fi

# ── 3. notificar_lead_whatsapp.py (chaves na mão → NOVOS LEADS)
NOTIFICAR="$KIT_ROOT/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/notificar_lead_whatsapp.py"
if [ -f "$NOTIFICAR" ]; then
    sed -i '' "s/GRUPO = \"[^\"]*\"/GRUPO = \"$GRUPO_LEADS\"/" "$NOTIFICAR"
    sed -i '' "s/CLICK_X = [0-9]*/CLICK_X = $CLICK_X/" "$NOTIFICAR"
    sed -i '' "s/CLICK_Y = [0-9]*/CLICK_Y = $CLICK_Y/" "$NOTIFICAR"
    echo "✅ notificar_lead_whatsapp.py → grupo '$GRUPO_LEADS' | click ($CLICK_X,$CLICK_Y)"
else
    echo "⚠️  notificar_lead_whatsapp.py não encontrado"
fi

# ── 4. SKILL.md follow-up manhã ───────────────────────────────
SKILL="$TASKS_DIR/impar-followup-manha/SKILL.md"
if [ -f "$SKILL" ]; then
    sed -i '' "s/keystroke \"FOLLOW UP IMPAR\"/keystroke \"$GRUPO_FOLLOWUP\"/" "$SKILL"
    echo "✅ impar-followup-manha/SKILL.md → grupo '$GRUPO_FOLLOWUP'"
else
    echo "⚠️  impar-followup-manha/SKILL.md não encontrado em $SKILL"
fi

# ── 5. Verifica LaunchAgents ativos ──────────────────────────
echo ""
echo "🔍 LaunchAgents de leads ativos:"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
for plist in "$LAUNCHD_DIR"/impar-*.plist "$LAUNCHD_DIR"/leads-*.plist; do
    [ -f "$plist" ] || continue
    label=$(basename "$plist" .plist)
    state=$(launchctl list "$label" 2>/dev/null | grep '"PID"' | awk '{print $3}' | tr -d ';')
    if [ -n "$state" ] && [ "$state" != "0" ]; then
        echo "   ✅ $label (PID $state)"
    else
        echo "   ⏸️  $label (não rodando)"
    fi
done

echo ""
echo "✅ Setup concluído. Reinicie os LaunchAgents se necessário:"
echo "   launchctl kickstart -k gui/\$(id -u)/<label>"
echo ""
echo "📋 Resumo das rotas de notificação:"
echo "   Gerente Digital (leads CSV)  → Jonata pessoal ($JONATA_WA)"
echo "   Marketplace / varredura inbox → Grupo: $GRUPO_LEADS"
echo "   Chaves na Mão                → Grupo: $GRUPO_LEADS"
echo "   Follow-up manhã              → Grupo: $GRUPO_FOLLOWUP"
