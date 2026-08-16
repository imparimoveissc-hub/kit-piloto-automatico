#!/bin/bash

# impar run module - Show how to execute automation (READ-ONLY, no execution)

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
AUTOMATION_PATH="$PROJECT_ROOT/18_AUTOMATION_STACK"

main() {
  local automation_name="${1:-}"

  if [[ -z "$automation_name" ]]; then
    print_error "Uso: impar run <nome>"
    echo ""
    echo "Exemplos:"
    echo "  impar run impar-facebook-marketplace-posting"
    echo "  impar run chaves-na-mao-lead-checker"
    echo ""
    return 1
  fi

  print_section "RUN — Como Executar Automação"

  local automation_dir="$AUTOMATION_PATH/$automation_name"

  if [[ ! -d "$automation_dir" ]]; then
    print_error "Automação não encontrada: $automation_name"
    return 1
  fi

  print_warning "MODO SOMENTE LEITURA — Nenhuma execução será realizada"
  echo ""

  print_success "$automation_name"
  echo ""

  show_execution_plan "$automation_name" "$automation_dir"
}

show_execution_plan() {
  local automation_name="$1"
  local automation_dir="$2"

  print_section "Plano de Execução"

  # Descobrir script principal
  local main_script=""
  if [[ -f "$automation_dir/main.py" ]]; then
    main_script="main.py"
  elif [[ -f "$automation_dir/automation.py" ]]; then
    main_script="automation.py"
  elif [[ -f "$automation_dir/run.py" ]]; then
    main_script="run.py"
  fi

  if [[ -z "$main_script" ]]; then
    print_warning "Nenhum script Python principal encontrado"
    return 1
  fi

  echo "Script: $main_script"
  echo ""

  # Verificar dependências
  if [[ -f "$automation_dir/requirements.txt" ]]; then
    print_section "Dependências"

    echo "Arquivo: requirements.txt"
    echo ""
    echo "Instalar com:"
    echo "  cd $automation_dir"
    echo "  pip install -r requirements.txt"
    echo ""
  fi

  # Comandos de execução
  print_section "Comandos de Execução"

  echo "Opção 1: Execução direta"
  echo "  cd $automation_dir"
  echo "  python3 $main_script"
  echo ""

  echo "Opção 2: Com variáveis de ambiente"
  if [[ -f "$automation_dir/.env" ]]; then
    echo "  source .env"
    echo "  python3 $main_script"
  else
    echo "  # Configurar variáveis de ambiente conforme necessário"
  fi
  echo ""

  echo "Opção 3: Via LaunchAgent (agendado)"
  echo "  launchctl load ~/Library/LaunchAgents/com.impar.${automation_name}.plist"
  echo ""

  # LaunchAgents existentes
  print_section "LaunchAgents Registrados"

  local agents_dir="$(expand_path ~/Library/LaunchAgents)"
  local agent_count=0

  while IFS= read -r plist; do
    if [[ -n "$plist" ]]; then
      local agent_name=$(basename "$plist" .plist)
      echo "  • $agent_name"
      agent_count=$((agent_count + 1))
    fi
  done < <(find "$agents_dir" -name "*${automation_name}*.plist" 2>/dev/null)

  if [[ $agent_count -eq 0 ]]; then
    print_info "Nenhum LaunchAgent registrado para esta automação"
  fi

  echo ""

  # Logs e checkpoint
  print_section "Estado Persistente"

  if [[ -f "$automation_dir/checkpoint.json" ]]; then
    local mtime=$(get_file_mtime "$automation_dir/checkpoint.json")
    echo "Checkpoint: checkpoint.json"
    echo "  Última modificação: $mtime"
  else
    echo "Checkpoint: Não encontrado"
  fi

  echo ""

  if [[ -d "$automation_dir/logs" ]]; then
    local log_count=$(find "$automation_dir/logs" -type f 2>/dev/null | wc -l)
    echo "Logs: logs/ ($log_count arquivos)"
  else
    echo "Logs: Não encontrados"
  fi

  echo ""

  # Aviso final
  print_section "Aviso"

  print_warning "Este é um modo SOMENTE LEITURA"
  echo "Nenhuma automação será executada neste wrapper"
  echo ""
  echo "Para realmente executar a automação:"
  echo "  1. Abra a pasta com: impar open $automation_name"
  echo "  2. Execute manualmente conforme os comandos acima"
  echo "  3. Ou configure um LaunchAgent para agendamento"
  echo ""
}

main "$@"
