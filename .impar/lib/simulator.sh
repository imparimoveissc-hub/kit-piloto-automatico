#!/bin/bash
# Biblioteca de Simulação de Execução
# Fornece funções para simular passo a passo sem executar

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
REGISTRY_FILE="${PROJECT_ROOT}/.impar/registry.json"
GRAPH_FILE="${PROJECT_ROOT}/.impar/graph.json"

simulate_step() {
    local step_number="$1"
    local step_name="$2"
    local action="$3"
    local files_read="$4"
    local files_modified="$5"
    local risk_level="$6"
    local rollback="$7"

    cat <<EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PASSO $step_number: $step_name
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AÇÃO:
  $action

ARQUIVOS LIDOS:
  $files_read

ARQUIVOS QUE SERIAM MODIFICADOS:
  $files_modified

RISCO:
  $risk_level

ROLLBACK:
  $rollback

STATUS:
  ✓ SIMULADO (NÃO EXECUTADO)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
}

simulate_marketplace_steps() {
    simulate_step "1" "Inicializar Browser Pane" \
        "Conectar ao Browser Pane do Claude Code" \
        "Nenhum arquivo" \
        "Nenhum arquivo" \
        "MÉDIO" \
        "Fechar Browser Pane"

    simulate_step "2" "Conectar ao Playwright" \
        "Carregar biblioteca Playwright e inicializar browser" \
        "cache/playwright" \
        "Nenhum arquivo" \
        "MÉDIO" \
        "Desconectar Playwright"

    simulate_step "3" "Ler fila de postagens" \
        "Ler arquivo fila-postagens.csv e parsear imóveis" \
        "fila-postagens.csv" \
        "Nenhum arquivo" \
        "BAIXO" \
        "Nenhum (leitura apenas)"

    simulate_step "4" "Iterar sobre imóveis" \
        "Para cada imóvel na fila, preparar dados de publicação" \
        "fila-postagens.csv" \
        "Nenhum arquivo (simulação)" \
        "MÉDIO" \
        "Nenhum (simulação)"

    simulate_step "5" "Publicar no Marketplace" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Enviaria imóveis para Facebook Marketplace" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "CRÍTICO" \
        "Deletar publicações do Marketplace"

    simulate_step "6" "Atualizar checkpoint" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Marcaria imóveis como publicados" \
        "Nenhum (BLOQUEADO)" \
        "crosspost-grupos-log.csv (BLOQUEADO)" \
        "CRÍTICO" \
        "Restaurar checkpoint anterior"

    simulate_step "7" "Registrar sucesso" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Gravaria logs de execução" \
        "Nenhum (BLOQUEADO)" \
        "logs/marketplace.log (BLOQUEADO)" \
        "BAIXO" \
        "Limpar arquivo de log"
}

simulate_messenger_steps() {
    simulate_step "1" "Inicializar Messenger API" \
        "Conectar ao Facebook Messenger via AppleScript" \
        "~/.local/impar-automation/messenger/config" \
        "Nenhum arquivo" \
        "CRÍTICO" \
        "Desconectar API"

    simulate_step "2" "Verificar novas mensagens" \
        "Buscar mensagens não respondidas nos últimos 10 minutos" \
        "checkpoint.json, Messenger inbox" \
        "Nenhum arquivo" \
        "MÉDIO" \
        "Nenhum (leitura apenas)"

    simulate_step "3" "Gerar resposta automática" \
        "Usar IA para gerar resposta contextualizada" \
        "Nenhum arquivo" \
        "Nenhum arquivo (simulação)" \
        "ALTO" \
        "Nenhum (simulação)"

    simulate_step "4" "Enviar resposta" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Enviaria mensagem via Messenger" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "CRÍTICO" \
        "Deletar mensagem enviada"

    simulate_step "5" "Atualizar checkpoint" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Marcaria mensagem como respondida" \
        "Nenhum (BLOQUEADO)" \
        "checkpoint.json (BLOQUEADO)" \
        "CRÍTICO" \
        "Restaurar estado de resposta"
}

simulate_leads_steps() {
    simulate_step "1" "Consultar Outlook" \
        "Ler emails não lidos de Chaves na Mão" \
        "Outlook (via Composio)" \
        "Nenhum arquivo" \
        "ALTO" \
        "Nenhum (leitura apenas)"

    simulate_step "2" "Parsear dados de lead" \
        "Extrair: nome, telefone, referência do imóvel, descrição" \
        "Dados do email" \
        "Nenhum arquivo" \
        "BAIXO" \
        "Nenhum"

    simulate_step "3" "Verificar blocklist" \
        "Consultar CSV de bloqueados" \
        "leads-followup.csv" \
        "Nenhum arquivo" \
        "BAIXO" \
        "Nenhum (leitura apenas)"

    simulate_step "4" "Detectar duplicatas (24h)" \
        "Verificar se lead foi enviado nos últimos 24h" \
        "checkpoint.json" \
        "Nenhum arquivo" \
        "MÉDIO" \
        "Nenhum (leitura apenas)"

    simulate_step "5" "Enviar D0 via WhatsApp" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Enviaria mensagem de primeiro contato" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "CRÍTICO" \
        "Deletar mensagem do WhatsApp"

    simulate_step "6" "Notificar Jonata" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Enviaria notificação via WhatsApp Desktop" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "CRÍTICO" \
        "Nenhum (notificação interna)"

    simulate_step "7" "Atualizar checkpoint" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Marcaria lead como enviado" \
        "Nenhum (BLOQUEADO)" \
        "checkpoint.json (BLOQUEADO)" \
        "CRÍTICO" \
        "Restaurar checkpoint de leads"
}

simulate_nfse_steps() {
    simulate_step "1" "Autenticar no Portal Nacional" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Login com credenciais do Portal" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "CRÍTICO" \
        "Nenhum (simulação, sem login)"

    simulate_step "2" "Buscar pagamentos no Asaas" \
        "Consultar API Asaas para pagamentos pendentes" \
        "Asaas API" \
        "Nenhum arquivo" \
        "MÉDIO" \
        "Nenhum (leitura apenas)"

    simulate_step "3" "Validar dados de NFS-e" \
        "Verificar completude de dados para emissão" \
        "Dados do Asaas" \
        "Nenhum arquivo" \
        "BAIXO" \
        "Nenhum"

    simulate_step "4" "Emitir NFS-e" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Emitiria nota fiscal de serviço" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "CRÍTICO" \
        "Cancelar NFS-e no Portal Nacional"

    simulate_step "5" "Enviar PDF por email" \
        "🚫 BLOQUEADO EM SIMULAÇÃO - Enviaria NFS-e via email" \
        "Nenhum (BLOQUEADO)" \
        "Nenhum (BLOQUEADO)" \
        "MÉDIO" \
        "Retornar NFS-e"
}

export -f simulate_step
export -f simulate_marketplace_steps
export -f simulate_messenger_steps
export -f simulate_leads_steps
export -f simulate_nfse_steps
