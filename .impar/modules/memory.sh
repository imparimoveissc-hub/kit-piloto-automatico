#!/bin/bash

# impar memory module - Show persistent memory state

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
MEMORY_PATH="$(expand_path $(get_config memory_path))"
MEMORY_INDEX="$MEMORY_PATH/MEMORY.md"

main() {
  print_section "MEMORY — Estado da Memória Persistente"

  validate_memory_index
  show_memory_stats
  show_memory_categories
  show_memory_files
  show_last_updates

  print_section "FIM — MEMORY"
}

validate_memory_index() {
  print_section "Validar Índice de Memória"

  if [[ ! -f "$MEMORY_INDEX" ]]; then
    print_error "MEMORY.md não encontrado em $MEMORY_PATH"
    return 1
  fi

  print_success "MEMORY.md presente"

  # Verificar se o arquivo contém as 4 categorias
  local categories=(
    "CONHECIMENTO ESTRUTURAL"
    "CONFIRMADO AGORA"
    "MEMÓRIA/HISTÓRICO"
    "NECESSITA VERIFICAÇÃO"
  )

  for category in "${categories[@]}"; do
    if grep -q "$category" "$MEMORY_INDEX"; then
      print_success "Categoria: $category"
    else
      print_warning "Categoria não encontrada: $category"
    fi
  done

  echo ""
}

show_memory_stats() {
  print_section "Estatísticas de Memória"

  if [[ ! -d "$MEMORY_PATH" ]]; then
    print_error "Diretório de memória não encontrado"
    return 1
  fi

  local file_count=$(find "$MEMORY_PATH" -name "*.md" -type f 2>/dev/null | wc -l)
  local total_size=$(du -sh "$MEMORY_PATH" 2>/dev/null | awk '{print $1}')
  local total_lines=$(find "$MEMORY_PATH" -name "*.md" -type f -exec wc -l {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}')

  echo "Arquivos de memória: $file_count"
  echo "Tamanho total: $total_size"
  echo "Linhas totais: $total_lines"
  echo ""
}

show_memory_categories() {
  print_section "Categorias de Memória"

  echo "1. CONHECIMENTO ESTRUTURAL (Arquitetura permanente)"
  echo "   - Decisões arquiteturais"
  echo "   - Fluxos de automação confirmados"
  echo "   - Pegadinhas de UI/UX"
  echo "   - Aprendizados de diagnóstico"
  echo ""

  echo "2. CONFIRMADO AGORA (Verificado 2026-07-23)"
  echo "   - Tecnologia de publicação em grupos (Playwright)"
  echo "   - Status do bloqueio Facebook (resolvido)"
  echo "   - Quantidades atualizadas"
  echo ""

  echo "3. MEMÓRIA/HISTÓRICO (Dados potencialmente antigos)"
  echo "   - Snapshots prévios"
  echo "   - Informações de 3+ dias"
  echo "   - Sempre verificar com arquivo-fonte"
  echo ""

  echo "4. NECESSITA VERIFICAÇÃO (Pendente)"
  echo "   - Contagens dinâmicas"
  echo "   - Filas variáveis (3x/dia)"
  echo "   - Taxa de sucesso"
  echo ""
}

show_memory_files() {
  print_section "Arquivos de Memória"

  if [[ ! -d "$MEMORY_PATH" ]]; then
    print_error "Diretório de memória não encontrado"
    return 1
  fi

  echo "Listando arquivos em: $MEMORY_PATH"
  echo ""

  local file_count=0
  while IFS= read -r file; do
    if [[ -f "$file" ]]; then
      local filename=$(basename "$file")
      local lines=$(count_lines "$file")
      local size=$(get_file_size "$file")
      local mtime=$(get_file_mtime "$file")

      printf "  %-60s %6s linhas  %8s  %s\n" "$filename" "$lines" "$size" "$mtime"
      file_count=$((file_count + 1))
    fi
  done < <(find "$MEMORY_PATH" -name "*.md" -type f 2>/dev/null | sort)

  echo ""
  print_info "Total: $file_count arquivos"
  echo ""
}

show_last_updates() {
  print_section "Últimas Atualizações"

  if [[ ! -d "$MEMORY_PATH" ]]; then
    return 1
  fi

  local latest_file=$(ls -t "$MEMORY_PATH"/*.md 2>/dev/null | head -1)
  if [[ -z "$latest_file" ]]; then
    print_info "Nenhum arquivo de memória encontrado"
    return 0
  fi

  local latest_mtime=$(get_file_mtime "$latest_file")
  print_info "Arquivo mais recente: $(basename "$latest_file")"
  print_info "Modificado em: $latest_mtime"
  echo ""

  # Mostrar últimas 3 atualizações
  echo "Últimas 3 atualizações:"
  echo ""
  ls -t "$MEMORY_PATH"/*.md 2>/dev/null | head -3 | while read -r file; do
    local filename=$(basename "$file")
    local mtime=$(get_file_mtime "$file")
    local size=$(get_file_size "$file")
    printf "  %-50s %8s  %s\n" "$filename" "$size" "$mtime"
  done

  echo ""
}

main "$@"
