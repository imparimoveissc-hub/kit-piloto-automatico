#!/bin/bash

# impar status module - Display current automation state

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
LOGS_PATH="$PROJECT_ROOT/$(get_config logs_path)"
MEMORY_PATH="$(expand_path $(get_config memory_path))"
WORKSPACE_PATH="$PROJECT_ROOT/$(get_config workspace_path)"
AUTOMATION_PATH="$PROJECT_ROOT/$(get_config automation_stack_path)"

main() {
  print_section "STATUS — Estado Atual da Automação Impar"

  # LaunchAgents
  show_launchagents_status

  # Automações conhecidas
  show_automacoes_conhecidas

  # Memória persistente
  show_memory_status

  # Task ledger
  show_ledger_status

  # Checkpoints
  show_checkpoints_status

  # Serviços desligados
  show_disabled_services

  # Alertas atuais
  show_alerts_status

  print_section "FIM — STATUS"
}

show_launchagents_status() {
  print_section "LaunchAgents"

  local agents_dir="$(expand_path ~/Library/LaunchAgents)"
  local impar_agents=0
  local active_count=0
  local inactive_count=0

  if [[ -d "$agents_dir" ]]; then
    while IFS= read -r plist; do
      if [[ "$plist" == *"impar"* ]] || [[ "$plist" == *"com.impar"* ]]; then
        impar_agents=$((impar_agents + 1))
        local agent_name=$(basename "$plist" .plist)

        if launchctl list 2>/dev/null | grep -q "$agent_name"; then
          print_success "$agent_name"
          active_count=$((active_count + 1))
        else
          print_warning "$agent_name (inactive)"
          inactive_count=$((inactive_count + 1))
        fi
      fi
    done < <(find "$agents_dir" -name "*.plist" -type f | sort)
  fi

  echo ""
  print_info "Total: $impar_agents agentes (${GREEN}$active_count ativo${NC}s, ${YELLOW}$inactive_count inativo${NC}s)"
  echo ""
}

show_automacoes_conhecidas() {
  print_section "Automações Conhecidas"

  local automacoes=(
    "marketplace:Marketplace + Grupos (Impar Imóveis)"
    "leads:Leads Chaves na Mão (WhatsApp)"
    "messenger:Messenger Inbox (Facebook)"
    "whatsapp:WhatsApp (Status: OFFLINE)"
    "nfse:Emissão de NFS-e (Portal Nacional)"
  )

  for auto in "${automacoes[@]}"; do
    local name="${auto%:*}"
    local desc="${auto#*:}"
    print_info "$name: $desc"
  done

  echo ""
}

show_memory_status() {
  print_section "Memória Persistente"

  if [[ ! -d "$MEMORY_PATH" ]]; then
    print_error "Diretório de memória não encontrado"
    return 1
  fi

  local file_count=$(find "$MEMORY_PATH" -name "*.md" -type f 2>/dev/null | wc -l)
  local total_size=$(du -sh "$MEMORY_PATH" 2>/dev/null | awk '{print $1}')
  local latest_file=$(ls -t "$MEMORY_PATH"/*.md 2>/dev/null | head -1)
  local latest_mtime=$(get_file_mtime "$latest_file" 2>/dev/null || echo "unknown")

  print_info "Arquivos: $file_count"
  print_info "Tamanho total: $total_size"
  print_info "Última atualização: $latest_mtime"
  echo ""
}

show_ledger_status() {
  print_section "Task Ledger"

  local ledger_file="$LOGS_PATH/task-ledger.md"

  if [[ ! -f "$ledger_file" ]]; then
    print_warning "Task ledger não encontrado"
    return 0
  fi

  local lines=$(count_lines "$ledger_file")
  local size=$(get_file_size "$ledger_file")
  local mtime=$(get_file_mtime "$ledger_file")

  print_info "Arquivo: task-ledger.md"
  print_info "Linhas: $lines"
  print_info "Tamanho: $size"
  print_info "Última atualização: $mtime"
  echo ""
}

show_checkpoints_status() {
  print_section "Checkpoints"

  local checkpoint_count=0

  if [[ -d "$WORKSPACE_PATH" ]]; then
    while IFS= read -r checkpoint; do
      if [[ -f "$checkpoint" ]]; then
        checkpoint_count=$((checkpoint_count + 1))
        local filename=$(basename "$checkpoint")
        local mtime=$(get_file_mtime "$checkpoint")

        if is_valid_json "$checkpoint"; then
          print_success "$filename — $mtime"
        else
          print_warning "$filename — JSON inválido"
        fi
      fi
    done < <(find "$WORKSPACE_PATH" -name "checkpoint.json" -o -name "*checkpoint*.json" 2>/dev/null)
  fi

  if [[ $checkpoint_count -eq 0 ]]; then
    print_info "Nenhum checkpoint encontrado"
  else
    print_info "Total: $checkpoint_count checkpoints"
  fi
  echo ""
}

show_disabled_services() {
  print_section "Serviços Intencionalmente Desligados"

  print_info "WhatsApp: ${YELLOW}OFFLINE${NC} (por requisição, não reautenticar)"
  print_info "VPS Oracle: Sessão ainda ativa na VM (chave SSH não disponível neste Mac)"
  print_info "QNAX Chatwoot: ${YELLOW}PARADO${NC} (docker compose down, dados preservados)"
  echo ""
}

show_alerts_status() {
  print_section "Alertas Atuais"

  local alert_count=0

  # Verificar se há alertas recentes nos logs
  if [[ -f "$LOGS_PATH/RELATORIO_FINAL_ETAPA_A_B_C.md" ]]; then
    print_info "Último relatório de validação: $(get_file_mtime "$LOGS_PATH/RELATORIO_FINAL_ETAPA_A_B_C.md")"
    alert_count=$((alert_count + 1))
  fi

  # Verificar se há incidentes não resolvidos
  if [[ -f "$MEMORY_PATH/impar-loop-whatsapp-2026-07-21.md" ]]; then
    print_warning "⚠ WhatsApp loop em 2026-07-21 — LaunchAgents desabilitados"
    alert_count=$((alert_count + 1))
  fi

  if [[ $alert_count -eq 0 ]]; then
    print_success "Sem alertas críticos"
  fi
  echo ""
}

main "$@"
