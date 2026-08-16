#!/bin/bash

# impar health module - Check automation health (read-only diagnostics)

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
AUTOMATION_PATH="$PROJECT_ROOT/18_AUTOMATION_STACK"

CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

main() {
  local automation_name="${1:-}"

  if [[ -z "$automation_name" ]]; then
    print_error "Uso: impar health <nome>"
    echo ""
    echo "Exemplos:"
    echo "  impar health impar-facebook-marketplace-posting"
    echo "  impar health chaves-na-mao-lead-checker"
    echo ""
    return 1
  fi

  print_section "HEALTH — Verificação de Saúde"

  local automation_dir="$AUTOMATION_PATH/$automation_name"

  if [[ ! -d "$automation_dir" ]]; then
    print_error "Automação não encontrada: $automation_name"
    return 1
  fi

  print_success "$automation_name"
  echo ""

  check_files "$automation_dir"
  check_launchagents "$automation_name"
  check_logs "$automation_dir"
  check_checkpoints "$automation_dir"
  check_permissions "$automation_dir"

  print_section "Resultado da Verificação"

  echo -e "  ${GREEN}✓ Passou: $CHECKS_PASSED${NC}"
  echo -e "  ${YELLOW}⚠ Avisos: $CHECKS_WARNING${NC}"
  echo -e "  ${RED}✗ Falhas: $CHECKS_FAILED${NC}"
  echo ""

  if [[ $CHECKS_FAILED -eq 0 ]]; then
    print_success "Automação em bom estado"
    return 0
  else
    print_warning "Verificar os problemas acima"
    return 1
  fi
}

check_files() {
  local automation_dir="$1"

  print_section "Verificar Arquivos"

  local required_files=(
    "README.md"
  )

  for file in "${required_files[@]}"; do
    if [[ -f "$automation_dir/$file" ]]; then
      print_success "$file"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      print_warning "$file — não encontrado"
      CHECKS_WARNING=$((CHECKS_WARNING + 1))
    fi
  done

  # Verificar scripts
  if [[ -f "$automation_dir/main.py" ]] || \
     [[ -f "$automation_dir/automation.py" ]] || \
     [[ -f "$automation_dir/run.py" ]]; then
    print_success "Script Python encontrado"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    print_warning "Nenhum script Python principal encontrado"
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
  fi

  echo ""
}

check_launchagents() {
  local automation_name="$1"

  print_section "Verificar LaunchAgents"

  local agents_dir="$(expand_path ~/Library/LaunchAgents)"
  local agent_count=0

  while IFS= read -r plist; do
    if [[ -n "$plist" ]]; then
      local agent_name=$(basename "$plist" .plist)

      if launchctl list 2>/dev/null | grep -q "$agent_name"; then
        print_success "$agent_name (ativo)"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
      else
        print_warning "$agent_name (inativo)"
        CHECKS_WARNING=$((CHECKS_WARNING + 1))
      fi

      agent_count=$((agent_count + 1))
    fi
  done < <(find "$agents_dir" -name "*${automation_name}*.plist" 2>/dev/null)

  if [[ $agent_count -eq 0 ]]; then
    print_info "Nenhum LaunchAgent específico encontrado"
  fi

  echo ""
}

check_logs() {
  local automation_dir="$1"

  print_section "Verificar Logs"

  if [[ ! -d "$automation_dir/logs" ]]; then
    print_info "Diretório de logs não encontrado"
    echo ""
    return 0
  fi

  local log_count=$(find "$automation_dir/logs" -type f 2>/dev/null | wc -l)
  local log_size=$(du -sh "$automation_dir/logs" 2>/dev/null | awk '{print $1}')

  if [[ $log_count -gt 0 ]]; then
    print_success "Logs encontrados: $log_count arquivos"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))

    print_info "Tamanho: $log_size"

    # Verificar idade dos logs
    local latest=$(ls -t "$automation_dir/logs" 2>/dev/null | head -1)
    if [[ -n "$latest" ]]; then
      local mtime=$(get_file_mtime "$automation_dir/logs/$latest")
      print_info "Log mais recente: $mtime"
    fi
  else
    print_warning "Nenhum log encontrado"
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
  fi

  echo ""
}

check_checkpoints() {
  local automation_dir="$1"

  print_section "Verificar Checkpoints"

  if [[ ! -f "$automation_dir/checkpoint.json" ]]; then
    print_info "Nenhum checkpoint encontrado"
    echo ""
    return 0
  fi

  print_success "Checkpoint encontrado"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))

  local size=$(get_file_size "$automation_dir/checkpoint.json")
  local mtime=$(get_file_mtime "$automation_dir/checkpoint.json")

  print_info "Tamanho: $size"
  print_info "Última modificação: $mtime"

  if is_valid_json "$automation_dir/checkpoint.json"; then
    print_success "JSON válido"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    print_error "JSON inválido"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
  fi

  echo ""
}

check_permissions() {
  local automation_dir="$1"

  print_section "Verificar Permissões"

  if [[ -r "$automation_dir" ]]; then
    print_success "Permissão de leitura: OK"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    print_error "Sem permissão de leitura"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
  fi

  echo ""
}

main "$@"
