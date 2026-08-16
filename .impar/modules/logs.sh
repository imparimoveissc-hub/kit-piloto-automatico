#!/bin/bash

# impar logs module - List and filter logs by module

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
LOGS_PATH="$PROJECT_ROOT/$(get_config logs_path)"
AUTOMATION_PATH="$PROJECT_ROOT/$(get_config automation_stack_path)"
MAX_LINES=$(get_config max_log_lines)

main() {
  local module="${1:-}"

  if [[ -z "$module" ]]; then
    show_available_modules
  else
    show_module_logs "$module"
  fi
}

show_available_modules() {
  print_section "Logs Disponíveis por Módulo"

  local modules=(
    "marketplace:Marketplace + Grupos"
    "grupos:Publicação em Grupos"
    "messenger:Messenger Inbox"
    "whatsapp:WhatsApp"
    "leads:Leads Chaves na Mão"
    "nfse:Emissão de NFS-e"
    "memory:Memória Persistente"
    "launchagents:LaunchAgents"
  )

  echo "Módulos disponíveis:"
  echo ""
  for mod in "${modules[@]}"; do
    local name="${mod%:*}"
    local desc="${mod#*:}"
    echo -e "  ${BLUE}$name${NC}  — $desc"
  done

  echo ""
  echo "Uso: impar logs <módulo>"
  echo ""
  echo "Exemplos:"
  echo "  impar logs marketplace  — Últimas $MAX_LINES linhas de logs do Marketplace"
  echo "  impar logs messenger    — Últimas $MAX_LINES linhas de logs do Messenger"
  echo ""

  # Show available log files
  print_section "Arquivos de Log Encontrados"

  if [[ -d "$LOGS_PATH" ]]; then
    list_files_formatted "$LOGS_PATH" "*.md"
    list_files_formatted "$LOGS_PATH" "*.csv"
    list_files_formatted "$LOGS_PATH" "*.log"
  fi

  echo ""
}

show_module_logs() {
  local module="$1"

  case "$module" in
    marketplace)
      show_marketplace_logs
      ;;
    grupos)
      show_grupos_logs
      ;;
    messenger)
      show_messenger_logs
      ;;
    whatsapp)
      show_whatsapp_logs
      ;;
    leads)
      show_leads_logs
      ;;
    nfse)
      show_nfse_logs
      ;;
    memory)
      show_memory_logs
      ;;
    launchagents)
      show_launchagents_logs
      ;;
    *)
      print_error "Módulo desconhecido: $module"
      echo ""
      show_available_modules
      return 1
      ;;
  esac
}

show_marketplace_logs() {
  print_section "LOGS — Marketplace + Grupos"

  local log_file="$AUTOMATION_PATH/impar-facebook-marketplace-posting/crosspost-grupos-log.csv"

  if [[ ! -f "$log_file" ]]; then
    print_warning "Arquivo de log não encontrado: $log_file"
    return 1
  fi

  echo "Arquivo: $(basename "$log_file")"
  echo "Linhas: $(count_lines "$log_file")"
  echo "Tamanho: $(get_file_size "$log_file")"
  echo ""

  print_section "Últimas $MAX_LINES linhas"
  show_tail "$log_file" "$MAX_LINES"

  echo ""
}

show_grupos_logs() {
  print_section "LOGS — Publicação em Grupos"

  local log_dir="$AUTOMATION_PATH/impar-facebook-marketplace-posting"

  if [[ ! -d "$log_dir" ]]; then
    print_warning "Diretório não encontrado: $log_dir"
    return 1
  fi

  # Mostrar fila de grupos
  local fila_file="$log_dir/fila-grupos-postagens.csv"
  if [[ -f "$fila_file" ]]; then
    print_info "Fila de Grupos: $(count_lines "$fila_file") linhas"
    echo ""
    echo "Últimas $MAX_LINES linhas:"
    show_tail "$fila_file" "$MAX_LINES"
  fi

  echo ""
}

show_messenger_logs() {
  print_section "LOGS — Messenger Inbox"

  local log_file="$LOGS_PATH/messenger-rodadas.md"

  if [[ ! -f "$log_file" ]]; then
    print_warning "Arquivo de log não encontrado: $log_file"
    return 1
  fi

  echo "Arquivo: $(basename "$log_file")"
  echo "Linhas: $(count_lines "$log_file")"
  echo "Tamanho: $(get_file_size "$log_file")"
  echo ""

  print_section "Últimas $MAX_LINES linhas"
  show_tail "$log_file" "$MAX_LINES"

  echo ""
}

show_whatsapp_logs() {
  print_section "LOGS — WhatsApp"

  print_warning "WhatsApp está OFFLINE — logs históricos apenas"
  echo ""

  local log_file="$LOGS_PATH/whatsapp-rodadas.md"

  if [[ ! -f "$log_file" ]]; then
    print_info "Nenhum arquivo de log de WhatsApp encontrado"
    return 0
  fi

  echo "Arquivo: $(basename "$log_file")"
  echo "Linhas: $(count_lines "$log_file")"
  echo "Tamanho: $(get_file_size "$log_file")"
  echo ""

  print_section "Últimas $MAX_LINES linhas"
  show_tail "$log_file" "$MAX_LINES"

  echo ""
}

show_leads_logs() {
  print_section "LOGS — Leads Chaves na Mão"

  local checkpoint_file="$HOME/.local/impar-automation/chaves-na-mao/checkpoint.json"
  local log_dir="$AUTOMATION_PATH/impar-leads-chaves-na-mao"

  if [[ -f "$checkpoint_file" ]]; then
    echo "Checkpoint: $(basename "$checkpoint_file")"
    echo "Tamanho: $(get_file_size "$checkpoint_file")"
    echo "Modificado: $(get_file_mtime "$checkpoint_file")"
    echo ""
    echo "Conteúdo:"
    show_tail "$checkpoint_file" "$MAX_LINES"
  else
    print_info "Nenhum checkpoint de leads encontrado"
  fi

  echo ""
}

show_nfse_logs() {
  print_section "LOGS — Emissão de NFS-e"

  local log_file="$LOGS_PATH/nfse-emissoes.md"

  if [[ ! -f "$log_file" ]]; then
    print_info "Nenhum arquivo de log de NFS-e encontrado"
    return 0
  fi

  echo "Arquivo: $(basename "$log_file")"
  echo "Linhas: $(count_lines "$log_file")"
  echo "Tamanho: $(get_file_size "$log_file")"
  echo ""

  print_section "Últimas $MAX_LINES linhas"
  show_tail "$log_file" "$MAX_LINES"

  echo ""
}

show_memory_logs() {
  print_section "LOGS — Memória Persistente"

  local memory_path="$PROJECT_ROOT/.claude/projects/-Users-usuario-Library-Mobile-Documents-com-apple-CloudDocs-Kit-Piloto-Automatico-V30-DISTRIB/memory"

  if [[ ! -d "$memory_path" ]]; then
    print_error "Diretório de memória não encontrado"
    return 1
  fi

  echo "Diretório: $memory_path"
  echo ""
  echo "Arquivos de memória:"
  list_files_formatted "$memory_path" "*.md"

  echo ""

  local latest_file=$(ls -t "$memory_path"/*.md 2>/dev/null | head -1)
  if [[ -n "$latest_file" ]]; then
    print_section "Arquivo mais recente: $(basename "$latest_file")"
    show_tail "$latest_file" "$MAX_LINES"
  fi

  echo ""
}

show_launchagents_logs() {
  print_section "LOGS — LaunchAgents"

  # Mostrar LaunchAgents do sistema
  if command -v launchctl &>/dev/null; then
    echo "LaunchAgents Impar ativos:"
    launchctl list | grep "impar" || print_info "Nenhum LaunchAgent Impar ativo"
  else
    print_warning "launchctl não disponível"
  fi

  echo ""
  echo "Arquivo de plist da VPS:"
  local vps_agent="$HOME/Library/LaunchAgents/com.impar.messenger-bridge.plist"
  if [[ -f "$vps_agent" ]]; then
    echo "Status: $(get_file_mtime "$vps_agent")"
  else
    print_info "VPS agent não encontrado (esperado se desabilitado)"
  fi

  echo ""
}

main "$@"
