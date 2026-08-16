#!/bin/bash

# impar info module - Show details about an automation

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
REGISTRY_FILE="$PROJECT_ROOT/.impar/registry.json"
AUTOMATION_PATH="$PROJECT_ROOT/18_AUTOMATION_STACK"

main() {
  local automation_name="${1:-}"

  if [[ -z "$automation_name" ]]; then
    print_error "Uso: impar info <nome>"
    echo ""
    echo "Exemplos:"
    echo "  impar info impar-facebook-marketplace-posting"
    echo "  impar info chaves-na-mao-lead-checker"
    echo ""
    return 1
  fi

  print_section "INFO — Detalhes da Automação"

  if [[ ! -f "$REGISTRY_FILE" ]]; then
    print_warning "Registry não encontrado. Execute 'impar discover' primeiro."
    return 1
  fi

  show_automation_info "$automation_name"
}

show_automation_info() {
  local automation_name="$1"
  local automation_dir="$AUTOMATION_PATH/$automation_name"

  if [[ ! -d "$automation_dir" ]]; then
    print_error "Automação não encontrada: $automation_name"
    return 1
  fi

  print_success "$automation_name"
  echo ""

  # Básico
  print_section "Informações Básicas"

  echo "Nome: $automation_name"
  echo "Caminho: 18_AUTOMATION_STACK/$automation_name"

  if [[ -f "$automation_dir/README.md" ]]; then
    local description=$(head -1 "$automation_dir/README.md" | sed 's/^[#]* //')
    echo "Descrição: $description"
  fi

  echo ""

  # Arquivos
  print_section "Arquivos"

  local file_count=0

  if [[ -f "$automation_dir/main.py" ]]; then
    echo "  ✓ main.py"
    file_count=$((file_count + 1))
  fi

  if [[ -f "$automation_dir/automation.py" ]]; then
    echo "  ✓ automation.py"
    file_count=$((file_count + 1))
  fi

  if [[ -f "$automation_dir/README.md" ]]; then
    echo "  ✓ README.md"
    file_count=$((file_count + 1))
  fi

  if [[ -f "$automation_dir/requirements.txt" ]]; then
    echo "  ✓ requirements.txt"
    file_count=$((file_count + 1))
  fi

  if [[ -f "$automation_dir/checkpoint.json" ]]; then
    echo "  ✓ checkpoint.json"
    file_count=$((file_count + 1))
  fi

  if [[ -d "$automation_dir/logs" ]]; then
    local log_count=$(find "$automation_dir/logs" -type f 2>/dev/null | wc -l)
    echo "  ✓ logs/ ($log_count arquivos)"
    file_count=$((file_count + 1))
  fi

  if [[ -f "$automation_dir/.env" ]]; then
    echo "  ✓ .env (credenciais)"
    file_count=$((file_count + 1))
  fi

  echo ""
  print_info "Total de arquivos: $file_count"
  echo ""

  # LaunchAgent
  print_section "LaunchAgent"

  local agents_dir="$(expand_path ~/Library/LaunchAgents)"
  local found_agents=0

  # Procurar por agentes relacionados
  while IFS= read -r plist; do
    if [[ -n "$plist" ]]; then
      local agent_name=$(basename "$plist" .plist)
      echo "  ✓ $agent_name"
      found_agents=$((found_agents + 1))
    fi
  done < <(find "$agents_dir" -name "*${automation_name}*.plist" 2>/dev/null)

  if [[ $found_agents -eq 0 ]]; then
    print_info "Nenhum LaunchAgent específico encontrado"
  else
    print_info "Agentes encontrados: $found_agents"
  fi

  echo ""

  # Checkpoints
  print_section "Checkpoints"

  if [[ -f "$automation_dir/checkpoint.json" ]]; then
    local mtime=$(get_file_mtime "$automation_dir/checkpoint.json")
    local size=$(get_file_size "$automation_dir/checkpoint.json")
    echo "  Arquivo: checkpoint.json"
    echo "  Tamanho: $size"
    echo "  Última modificação: $mtime"

    # Mostrar resumo do checkpoint (sem expor dados sensíveis)
    if is_valid_json "$automation_dir/checkpoint.json"; then
      echo "  Status: ✓ JSON válido"
    else
      echo "  Status: ✗ JSON inválido"
    fi
  else
    print_info "Nenhum checkpoint encontrado"
  fi

  echo ""

  # Logs
  print_section "Logs"

  if [[ -d "$automation_dir/logs" ]]; then
    local log_count=$(find "$automation_dir/logs" -type f 2>/dev/null | wc -l)
    local log_size=$(du -sh "$automation_dir/logs" 2>/dev/null | awk '{print $1}')

    echo "  Diretório: logs/"
    echo "  Arquivos: $log_count"
    echo "  Tamanho: $log_size"

    # Arquivos mais recentes
    echo ""
    echo "  Arquivos mais recentes:"
    ls -t "$automation_dir/logs" 2>/dev/null | head -5 | while read -r file; do
      echo "    • $file"
    done
  else
    print_info "Nenhum log encontrado"
  fi

  echo ""

  # Ações
  print_section "Ações Disponíveis"

  echo "  impar open $automation_name   — Abrir pasta"
  echo "  impar health $automation_name — Verificar saúde"
  echo "  impar logs $automation_name   — Ver logs"
  echo ""
}

main "$@"
