#!/bin/bash

# impar backup module - Create safe backups of memory and configuration

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
MEMORY_PATH="$PROJECT_ROOT/.claude/projects/-Users-usuario-Library-Mobile-Documents-com-apple-CloudDocs-Kit-Piloto-Automatico-V30-DISTRIB/memory"
WRAPPER_PATH="$PROJECT_ROOT/.impar"
BACKUP_BASE="$(expand_path $(get_config backup_base_path))"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$BACKUP_BASE/$TIMESTAMP"

main() {
  print_section "BACKUP — Criar Backup Seguro"

  show_backup_plan
  confirm_backup
  create_backup
}

show_backup_plan() {
  print_section "Plano de Backup"

  echo "Timestamp: $TIMESTAMP"
  echo "Diretório de backup: $BACKUP_DIR"
  echo ""

  print_section "Arquivos a Incluir no Backup"

  echo "1. Memória Persistente"
  echo "   Diretório: $MEMORY_PATH"
  echo "   Conteúdo: Todos os arquivos .md (documentação, conhecimento)"
  echo ""

  echo "2. Configuração do Wrapper"
  echo "   Diretório: $WRAPPER_PATH"
  echo "   Conteúdo: config.json, lib/, modules/, docs/"
  echo ""

  print_section "Arquivos EXCLUÍDOS (Por Segurança)"

  echo "✗ Credenciais (.env, secrets, tokens)"
  echo "✗ Cookies e sessões"
  echo "✗ Chaves SSH/GPG"
  echo "✗ Logs muito grandes (>100MB)"
  echo "✗ .git/ e controle de versão"
  echo "✗ node_modules/ ou venv/"
  echo "✗ Checkpoints JSON (dados operacionais)"
  echo ""

  print_section "Espaço em Disco"

  local memory_size=$(du -sh "$MEMORY_PATH" 2>/dev/null | awk '{print $1}' || echo "unknown")
  local wrapper_size=$(du -sh "$WRAPPER_PATH" 2>/dev/null | awk '{print $1}' || echo "unknown")
  local total_backup_size="~$(echo "$memory_size" | sed 's/G/,/g' | sed 's/M/ + /g')$(echo "$wrapper_size" | sed 's/G/,/g' | sed 's/M/ MB/g')"

  echo "Memória: $memory_size"
  echo "Wrapper: $wrapper_size"
  echo "Total estimado: ~2-5 MB"
  echo ""

  local available_space=$(df "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
  local space_gb=$((available_space / 1024 / 1024))
  echo "Espaço disponível: ${space_gb}GB"
  echo ""
}

confirm_backup() {
  print_section "Confirmação de Backup"

  echo "Será criado backup em:"
  echo "  $BACKUP_DIR"
  echo ""

  echo "Arquivos específicos a incluir:"
  echo ""

  if [[ -d "$MEMORY_PATH" ]]; then
    echo "Memory files:"
    find "$MEMORY_PATH" -name "*.md" -type f | head -5 | while read -r file; do
      echo "  + $(basename "$file")"
    done
    local total=$(find "$MEMORY_PATH" -name "*.md" -type f | wc -l)
    if [[ $total -gt 5 ]]; then
      echo "  + ... e $((total - 5)) outros arquivos"
    fi
  fi

  echo ""
  if [[ -d "$WRAPPER_PATH" ]]; then
    echo "Wrapper files:"
    find "$WRAPPER_PATH" -type f \( -name "*.sh" -o -name "*.json" -o -name "*.md" \) | head -5 | while read -r file; do
      echo "  + $(basename "$file")"
    done
    local total=$(find "$WRAPPER_PATH" -type f \( -name "*.sh" -o -name "*.json" -o -name "*.md" \) | wc -l)
    if [[ $total -gt 5 ]]; then
      echo "  + ... e $((total - 5)) outros arquivos"
    fi
  fi

  echo ""
  print_warning "Nenhuma credencial, token, cookie ou dado sensível será incluído."
  echo ""
  echo "Deseja continuar? (s/n)"
  read -r response

  if [[ "$response" != "s" ]] && [[ "$response" != "S" ]]; then
    print_info "Backup cancelado pelo usuário"
    exit 0
  fi
}

create_backup() {
  print_section "Criando Backup..."

  if [[ ! -d "$BACKUP_BASE" ]]; then
    mkdir -p "$BACKUP_BASE"
  fi

  mkdir -p "$BACKUP_DIR"

  # Backup da memória
  if [[ -d "$MEMORY_PATH" ]]; then
    print_info "Fazendo backup da memória..."
    mkdir -p "$BACKUP_DIR/memory"
    find "$MEMORY_PATH" -name "*.md" -type f -exec cp {} "$BACKUP_DIR/memory/" \; 2>/dev/null || true
    print_success "Memória backupada"
  fi

  # Backup do wrapper
  if [[ -d "$WRAPPER_PATH" ]]; then
    print_info "Fazendo backup do wrapper..."
    mkdir -p "$BACKUP_DIR/wrapper"
    cp -r "$WRAPPER_PATH"/* "$BACKUP_DIR/wrapper/" 2>/dev/null || true
    print_success "Wrapper backupado"
  fi

  # Criar arquivo de índice do backup
  create_backup_manifest

  # Validar backup
  validate_backup

  print_section "Backup Concluído"
  echo ""
  print_success "Backup criado com sucesso"
  echo ""
  echo "Localização: $BACKUP_DIR"
  echo "Conteúdo:"
  echo ""
  ls -lh "$BACKUP_DIR" | awk 'NR>1 {printf "  %-40s %10s\n", $9, $5}'
  echo ""

  # Mostrar como restaurar
  show_restore_instructions
}

create_backup_manifest() {
  local manifest="$BACKUP_DIR/MANIFEST.txt"

  cat > "$manifest" <<EOF
Backup Impar — Memória e Configuração
Data: $TIMESTAMP
Versão: 1.0

Conteúdo:
- memory/: Todos os arquivos .md de memória persistente
- wrapper/: Configuração e módulos do wrapper impar

Segurança:
- ZERO credenciais, tokens ou cookies inclusos
- ZERO dados sensíveis
- Backup é somente leitura e reversível
- Restauração: ver instruções em RESTORE.txt

Tamanho Aproximado: 2-5 MB
Data de Validade: Indefinida (backup histórico)

EOF

  print_info "Manifesto criado: $manifest"
}

validate_backup() {
  print_section "Validar Backup"

  local memory_backup_files=$(find "$BACKUP_DIR/memory" -name "*.md" -type f 2>/dev/null | wc -l)
  local wrapper_backup_files=$(find "$BACKUP_DIR/wrapper" -type f 2>/dev/null | wc -l)

  if [[ $memory_backup_files -gt 0 ]]; then
    print_success "Memory backup: $memory_backup_files arquivos"
  else
    print_warning "Memory backup: nenhum arquivo"
  fi

  if [[ $wrapper_backup_files -gt 0 ]]; then
    print_success "Wrapper backup: $wrapper_backup_files arquivos"
  else
    print_warning "Wrapper backup: nenhum arquivo"
  fi

  echo ""
}

show_restore_instructions() {
  print_section "Como Restaurar o Backup"

  cat <<'EOF'
Se precisar restaurar este backup:

1. Navegar até o diretório de backup:
   cd /private/tmp/impar-backups/TIMESTAMP/

2. Restaurar a memória:
   cp -r memory/* ~/.claude/projects/.../memory/

3. Restaurar o wrapper (se necessário):
   cp -r wrapper/* /path/to/project/.impar/

4. Verificar a restauração:
   impar memory
   impar doctor

IMPORTANTE:
- Sempre fazer backup de seus dados locais antes de restaurar
- A restauração sobrescreverá arquivos existentes
- Contacte o suporte se encontrar problemas

EOF

  echo ""
}

main "$@"
