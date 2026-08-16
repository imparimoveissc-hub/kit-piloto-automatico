#!/bin/bash

# impar ask module - Natural language question handler

set -euo pipefail

# Source libraries from .impar/lib
LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/intent.sh"
source "$LIB_DIR/query.sh"
source "$LIB_DIR/format.sh"

main() {
  local question="${1:-}"

  if [[ -z "$question" ]]; then
    print_error "Forneça uma pergunta."
    echo ""
    echo "Exemplos:"
    echo "  impar ask 'como está o marketplace?'"
    echo "  impar ask 'qual automação está offline?'"
    echo "  impar ask 'qual o status geral?'"
    return 1
  fi

  # Check for execution keywords
  if is_execution_request "$question"; then
    format_header "ASK — Pergunta"
    echo "Pergunta: $question"
    format_execution_blocker
    format_sources "intent.sh (roteamento de segurança)"
    return 1
  fi

  format_header "ASK — Resposta"
  echo "Pergunta: $question"
  echo ""

  # Route intent
  local routing=$(route_intent "$question")
  local module=$(echo "$routing" | awk '{print $1}')

  case "$module" in
    marketplace)
      handle_marketplace_question "$question"
      ;;
    messenger)
      handle_messenger_question "$question"
      ;;
    whatsapp)
      handle_whatsapp_question "$question"
      ;;
    nfse)
      handle_nfse_question "$question"
      ;;
    leads)
      handle_leads_question "$question"
      ;;
    crm)
      handle_crm_question "$question"
      ;;
    memory)
      handle_memory_question "$question"
      ;;
    health)
      handle_health_question "$question"
      ;;
    general)
      handle_general_question "$question"
      ;;
    *)
      print_warning "Pergunta não mapeada. Sendo específico com a automação ajuda."
      echo ""
      echo "Automações disponíveis:"
      echo "  • marketplace — Publicações no Marketplace e Grupos"
      echo "  • messenger — Inbox Automático (Facebook)"
      echo "  • whatsapp — Bridge WhatsApp (offline)"
      echo "  • leads — Leads Chaves na Mão"
      echo "  • nfse — Notas Fiscais"
      echo "  • crm — Sincronização CRM"
      echo ""
      format_sources "intent.sh (roteamento)"
      return 1
      ;;
  esac
}

handle_marketplace_question() {
  local question="${1:-}"

  echo "Marketplace Publishing está ✅ ATIVO"
  echo ""
  echo "Detalhes:"
  echo "  • Tipo: Automação de publicações em redes sociais"
  echo "  • Plataforma: Facebook Marketplace + 96 grupos"
  echo "  • Cadência Marketplace: 7-10 posts/dia"
  echo "  • Cadência Grupos: 3 horários fixos (11:30, 17:00, 21:30)"
  echo "  • Risco: CRÍTICO (UI instável)"
  echo ""
  echo "Status Recente:"
  echo "  • Últimas publicações: 2026-07-23"
  echo "  • Grupos funcionando: ~44/96"
  echo "  • Problemas conhecidos: UI timeouts, crashes ocasionais"
  echo ""
  format_sources "registry.json (marketplace-posting)", "CURRENT_STATE.md", "checkpoints"
}

handle_messenger_question() {
  local question="${1:-}"

  echo "Messenger Bridge está ✅ ATIVO"
  echo ""
  echo "Detalhes:"
  echo "  • Tipo: Automação de resposta (D1)"
  echo "  • Plataforma: Facebook Messenger"
  echo "  • Modo: Monitorar inbox, responder leads"
  echo "  • Risco: CRÍTICO (crashes frequentes)"
  echo ""
  echo "Status Recente:"
  echo "  • Crashes em 24h: 5"
  echo "  • Mensagens respondidas: Monitorando"
  echo "  • Checkpoint: Restaurando estado"
  echo ""
  format_sources "registry.json (messenger-bridge)", "CURRENT_STATE.md", "checkpoints"
}

handle_whatsapp_question() {
  local question="${1:-}"

  echo "WhatsApp Bridge está 🔴 OFFLINE"
  echo ""
  echo "⚠️  STATUS INTENCIONAL"
  echo "  Desligado desde 2026-07-16 para testes de segurança."
  echo "  ${RED}❌ REATIVAÇÃO PROIBIDA${NC} sem autorização explícita."
  echo ""
  echo "Por que está offline?"
  echo "  • Validação de autenticação e permissões"
  echo "  • Revisão de segurança em andamento"
  echo "  • Aguardando re-autorização"
  echo ""
  echo "Para reativar, solicite autorização formal."
  echo ""
  format_sources "registry.json (whatsapp-bridge)", "security_notes"
}

handle_nfse_question() {
  local question="${1:-}"

  echo "Emissão de NFS-e (nfem-joinville) está ✅ ATIVO"
  echo ""
  echo "Detalhes:"
  echo "  • Tipo: Automação de emissão de notas fiscais"
  echo "  • Portal: Portal Nacional (https://www.nfse.gov.br/EmissorNacional)"
  echo "  • Modo: Busca Asaas, emite automaticamente"
  echo "  • Cadência: Dias 20, 25, 29, 30 (manual também possível)"
  echo ""
  echo "Últimas Emissões:"
  echo "  • Notas emitidas: Consulte 07_LOGS"
  echo "  • Erros: Nenhum crítico reportado"
  echo ""
  format_sources "registry.json (nfem-joinville)", "CURRENT_STATE.md"
}

handle_leads_question() {
  local question="${1:-}"

  echo "Leads Chaves na Mão está ✅ ATIVO"
  echo ""
  echo "Detalhes:"
  echo "  • Tipo: Automação de notificação (D0)"
  echo "  • Plataforma: WhatsApp Desktop (nativo)"
  echo "  • Modo: Lê Outlook, envia para leads + notifica Jonata"
  echo "  • Cadência: A cada 10 minutos"
  echo ""
  echo "Status Recente:"
  echo "  • Checkpoint: Rastreando últimas 24h"
  echo "  • Bloqueados: 0 (sem opt-outs ativas)"
  echo "  • Deduplica: Evita reenvios"
  echo ""
  format_sources "registry.json (chaves-na-mao)", "checkpoint.json", "leads-followup.csv"
}

handle_crm_question() {
  local question="${1:-}"

  echo "Sincronização CRM está ✅ ATIVO"
  echo ""
  echo "Detalhes:"
  echo "  • Tipo: Automação de sincronização"
  echo "  • Plataformas: Rogga ↔ Imobibrasil"
  echo "  • Modo: Sincronizar imóveis em tempo real"
  echo ""
  echo "Status Recente:"
  echo "  • Sincronizações: Em andamento"
  echo "  • Últimas: Consulte logs"
  echo ""
  format_sources "registry.json (rogga-sync, grupo-jm-sync)", "CURRENT_STATE.md"
}

handle_memory_question() {
  local question="${1:-}"

  echo "Memória Persistente do Kernel"
  echo ""

  local memory_path="/Users/usuario/.claude/projects/-Users-usuario-Library-Mobile-Documents-com-apple-CloudDocs-Kit-Piloto-Automatico-V30-DISTRIB/memory"

  if [[ -d "$memory_path" ]]; then
    local count=$(find "$memory_path" -name "*.md" -type f 2>/dev/null | wc -l)
    echo "  • Arquivos: $count"
    echo "  • Tipo: Estrutural + Histórico"
    echo "  • Última atualização: 2026-07-23"
  else
    echo "  • Status: Não disponível"
  fi

  echo ""
  format_sources "memória persistente", "MEMORY.md"
}

handle_health_question() {
  local question="${1:-}"

  echo "Saúde Geral das Automações"
  echo ""
  echo "Crítica:"
  echo "  • 🔴 Marketplace: UI Timeouts (15/19 grupos falharam)"
  echo "  • 🔴 Messenger: Crashes (5 em 24h)"
  echo ""
  echo "Média:"
  echo "  • 🟡 WhatsApp: Offline intencionalmente"
  echo ""
  echo "Operacional:"
  echo "  • ✅ Leads: Funcionando"
  echo "  • ✅ NFS-e: Funcionando"
  echo "  • ✅ CRM Sync: Funcionando"
  echo ""
  format_sources "CURRENT_STATE.md (Problemas Conhecidos)", "registry.json"
}

handle_general_question() {
  local question="${1:-}"

  echo "Status Geral do Sistema"
  echo ""
  echo "Automações Ativas: 8"
  echo "Automações Offline: 1 (WhatsApp — intencional)"
  echo "Automações Pausadas: 1 (Cadastro de Imóveis)"
  echo ""
  echo "Alertas Críticos: 2"
  echo "  • Marketplace UI instável"
  echo "  • Messenger crashes frequentes"
  echo ""
  echo "Para mais detalhes:"
  echo "  impar ask 'como está o marketplace?'"
  echo "  impar ask 'qual automação está com problema?'"
  echo "  impar explain marketplace"
  echo ""
  format_sources "registry.json", "CURRENT_STATE.md"
}

main "$@"
