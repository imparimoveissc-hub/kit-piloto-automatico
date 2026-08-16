#!/bin/bash

# impar doctor module - Read-only diagnostics

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
LOGS_PATH="$PROJECT_ROOT/$(get_config logs_path)"
MEMORY_PATH="$(expand_path $(get_config memory_path))"
WORKSPACE_PATH="$PROJECT_ROOT/$(get_config workspace_path)"
AUTOMATION_PATH="$PROJECT_ROOT/$(get_config automation_stack_path)"

CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

main() {
  print_section "DOCTOR — Diagnóstico Somente Leitura"

  check_project_structure
  check_critical_files
  check_json_validity
  check_launchagents
  check_memory_integrity
  check_logs
  check_permissions
  check_disk_space
  check_checkpoints

  print_section "Resultado do Diagnóstico"
  echo -e "  ${GREEN}✓ Passou: $CHECKS_PASSED${NC}"
  echo -e "  ${YELLOW}⚠ Avisos: $CHECKS_WARNING${NC}"
  echo -e "  ${RED}✗ Falhas: $CHECKS_FAILED${NC}"
  echo ""

  if [[ $CHECKS_FAILED -eq 0 ]]; then
    print_success "Diagnóstico concluído — sem problemas críticos"
    return 0
  else
    print_error "Diagnóstico concluído — há problemas para investigar"
    return 1
  fi
}

check_project_structure() {
  print_section "Verificar Estrutura do Projeto"

  local required_dirs=(
    ".impar"
    "07_LOGS"
    "05_WORKSPACE"
    "18_AUTOMATION_STACK"
  )

  for dir in "${required_dirs[@]}"; do
    if [[ -d "$PROJECT_ROOT/$dir" ]]; then
      print_success "$dir/"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      print_error "$dir/ — não encontrado"
      CHECKS_FAILED=$((CHECKS_FAILED + 1))
    fi
  done
  echo ""
}

check_critical_files() {
  print_section "Verificar Arquivos Críticos"

  local critical_files=(
    ".impar/config.json"
    ".impar/lib/common.sh"
    "CLAUDE.md"
    ".claude/projects/-Users-usuario-Library-Mobile-Documents-com-apple-CloudDocs-Kit-Piloto-Automatico-V30-DISTRIB/memory/MEMORY.md"
  )

  for file in "${critical_files[@]}"; do
    if [[ -f "$PROJECT_ROOT/$file" ]] || [[ -f "$HOME/$file" ]]; then
      print_success "$file"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      print_error "$file — não encontrado"
      CHECKS_FAILED=$((CHECKS_FAILED + 1))
    fi
  done
  echo ""
}

check_json_validity() {
  print_section "Validar JSON"

  local json_files=(
    ".impar/config.json"
  )

  while IFS= read -r jsonfile; do
    if [[ -f "$jsonfile" ]]; then
      if is_valid_json "$jsonfile"; then
        print_success "$(basename "$jsonfile")"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
      else
        print_error "$(basename "$jsonfile") — JSON inválido"
        CHECKS_FAILED=$((CHECKS_FAILED + 1))
      fi
    fi
  done < <(find "$PROJECT_ROOT" -maxdepth 3 -name "*.json" -type f)

  echo ""
}

check_launchagents() {
  print_section "Verificar LaunchAgents"

  local agents_dir="$(expand_path ~/Library/LaunchAgents)"
  local impar_count=0

  if [[ -d "$agents_dir" ]]; then
    while IFS= read -r plist; do
      impar_count=$((impar_count + 1))
    done < <(find "$agents_dir" -name "*impar*.plist" -o -name "com.impar*.plist" 2>/dev/null)

    if [[ $impar_count -gt 0 ]]; then
      print_success "$impar_count LaunchAgents Impar encontrados"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      print_warning "Nenhum LaunchAgent Impar encontrado"
      CHECKS_WARNING=$((CHECKS_WARNING + 1))
    fi
  else
    print_warning "Diretório LaunchAgents não acessível"
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
  fi
  echo ""
}

check_memory_integrity() {
  print_section "Verificar Integridade de Memória"

  if [[ ! -d "$MEMORY_PATH" ]]; then
    print_error "Diretório de memória não encontrado"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
    echo ""
    return 1
  fi

  local memory_index="$MEMORY_PATH/MEMORY.md"
  if [[ ! -f "$memory_index" ]]; then
    print_error "MEMORY.md não encontrado"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
  else
    print_success "MEMORY.md presente"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  fi

  local file_count=$(find "$MEMORY_PATH" -name "*.md" -type f 2>/dev/null | wc -l)
  if [[ $file_count -gt 0 ]]; then
    print_success "$file_count arquivos de memória"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    print_warning "Nenhum arquivo de memória encontrado"
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
  fi

  echo ""
}

check_logs() {
  print_section "Verificar Logs"

  if [[ ! -d "$LOGS_PATH" ]]; then
    print_error "Diretório de logs não encontrado"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
    echo ""
    return 1
  fi

  local log_count=$(find "$LOGS_PATH" -name "*.md" -o -name "*.csv" -o -name "*.log" 2>/dev/null | wc -l)
  if [[ $log_count -gt 0 ]]; then
    print_success "$log_count arquivos de log"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    print_warning "Nenhum arquivo de log encontrado"
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
  fi

  echo ""
}

check_permissions() {
  print_section "Verificar Permissões"

  local wrapper_path="$(expand_path ~/.local/bin/impar)"
  if [[ -f "$wrapper_path" ]]; then
    if [[ -x "$wrapper_path" ]]; then
      print_success "impar wrapper é executável"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      print_warning "impar wrapper não é executável"
      CHECKS_WARNING=$((CHECKS_WARNING + 1))
    fi
  else
    print_info "impar wrapper ainda não instalado"
  fi

  # Verificar se o usuário pode ler a memória
  if [[ -r "$MEMORY_PATH" ]]; then
    print_success "Permissão de leitura: memória"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    print_error "Sem permissão de leitura: memória"
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
  fi

  echo ""
}

check_disk_space() {
  print_section "Verificar Espaço em Disco"

  local available_space=$(df "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
  local threshold=$((1000000)) # 1GB in KB

  if [[ $available_space -gt $threshold ]]; then
    local space_gb=$((available_space / 1024 / 1024))
    print_success "Espaço disponível: ${space_gb}GB"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
  else
    local space_gb=$((available_space / 1024 / 1024))
    print_warning "Espaço disponível baixo: ${space_gb}GB"
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
  fi

  echo ""
}

check_checkpoints() {
  print_section "Verificar Integridade de Checkpoints"

  local checkpoint_count=0
  local valid_count=0

  while IFS= read -r checkpoint; do
    if [[ -f "$checkpoint" ]]; then
      checkpoint_count=$((checkpoint_count + 1))
      if is_valid_json "$checkpoint"; then
        valid_count=$((valid_count + 1))
      fi
    fi
  done < <(find "$WORKSPACE_PATH" -name "*checkpoint*.json" 2>/dev/null)

  if [[ $checkpoint_count -gt 0 ]]; then
    if [[ $valid_count -eq $checkpoint_count ]]; then
      print_success "$checkpoint_count checkpoints — todos válidos"
      CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
      print_warning "$checkpoint_count checkpoints — $((checkpoint_count - valid_count)) com JSON inválido"
      CHECKS_WARNING=$((CHECKS_WARNING + 1))
    fi
  else
    print_info "Nenhum checkpoint encontrado"
  fi

  echo ""
}

main "$@"
