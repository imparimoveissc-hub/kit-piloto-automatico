#!/bin/bash

# Library of common functions for impar wrapper

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
GRAY='\033[0;90m'
NC='\033[0m'

# Get project root
get_project_root() {
  local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
  echo "$script_dir"
}

# Get config value from config.json
get_config() {
  local key="$1"
  local config_file="$(get_project_root)/.impar/config.json"

  if [[ ! -f "$config_file" ]]; then
    echo "ERROR: Config file not found: $config_file" >&2
    return 1
  fi

  local value=$(python3 -c "import json; c=json.load(open('$config_file')); print(c.get('$key', ''))" 2>/dev/null || echo "")

  # Expand ~ in paths
  if [[ "$value" == ~* ]]; then
    value="${value/#\~/$HOME}"
  fi

  echo "$value"
}

# Print colored message
print_info() {
  echo -e "${BLUE}ℹ${NC}  $*"
}

print_success() {
  echo -e "${GREEN}✓${NC}  $*"
}

print_warning() {
  echo -e "${YELLOW}⚠${NC}  $*"
}

print_error() {
  echo -e "${RED}✗${NC}  $*"
}

print_section() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  $*${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

# Expand ~ paths
expand_path() {
  local path="$1"
  echo "${path/#\~/$HOME}"
}

# Check if file exists
file_exists() {
  [[ -f "$1" ]]
}

# Check if directory exists
dir_exists() {
  [[ -d "$1" ]]
}

# Get file modification time in human format
get_file_mtime() {
  local file="$1"
  if [[ -f "$file" ]]; then
    stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" "$file" 2>/dev/null || echo "unknown"
  else
    echo "n/a"
  fi
}

# Get file size in human format
get_file_size() {
  local file="$1"
  if [[ -f "$file" ]]; then
    du -h "$file" | awk '{print $1}'
  else
    echo "n/a"
  fi
}

# List files in directory with formatting
list_files_formatted() {
  local dir="$1"
  local pattern="${2:-.}"

  if [[ ! -d "$dir" ]]; then
    print_warning "Diretório não encontrado: $dir"
    return 1
  fi

  find "$dir" -maxdepth 1 -name "$pattern" -type f | while read -r file; do
    local filename=$(basename "$file")
    local size=$(get_file_size "$file")
    local mtime=$(get_file_mtime "$file")
    printf "  %-50s %8s  %s\n" "$filename" "$size" "$mtime"
  done
}

# Get launchagent status
get_launchagent_status() {
  local agent_name="$1"
  local agents_dir="$(expand_path ~/Library/LaunchAgents)"

  if [[ ! -f "$agents_dir/$agent_name.plist" ]]; then
    echo "not_found"
    return 1
  fi

  if launchctl list | grep -q "^.*$agent_name"; then
    echo "active"
    return 0
  else
    echo "inactive"
    return 0
  fi
}

# Count lines in file
count_lines() {
  local file="$1"
  if [[ -f "$file" ]]; then
    wc -l < "$file" | tr -d ' '
  else
    echo "0"
  fi
}

# Check JSON validity
is_valid_json() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    return 1
  fi
  python3 -c "import json; json.load(open('$file'))" 2>/dev/null
}

# Create backup with timestamp
create_backup() {
  local source="$1"
  local backup_base="$(expand_path $(get_config backup_base_path))"
  local timestamp=$(date +%Y%m%d-%H%M%S)
  local backup_dir="$backup_base/$timestamp"

  if [[ ! -d "$backup_base" ]]; then
    mkdir -p "$backup_base"
  fi

  mkdir -p "$backup_dir"
  cp -r "$source" "$backup_dir/" 2>/dev/null || true

  echo "$backup_dir"
}

# Show last N lines of file
show_tail() {
  local file="$1"
  local lines="${2:-50}"

  if [[ ! -f "$file" ]]; then
    print_warning "Arquivo não encontrado: $file"
    return 1
  fi

  tail -n "$lines" "$file"
}

# Validate memory structure
validate_memory() {
  local memory_path="$(get_project_root)/$(get_config memory_path)"
  local memory_index="$memory_path/$(get_config memory_index_file)"

  if [[ ! -d "$memory_path" ]]; then
    print_error "Diretório de memória não encontrado: $memory_path"
    return 1
  fi

  if [[ ! -f "$memory_index" ]]; then
    print_error "Arquivo de índice de memória não encontrado: $memory_index"
    return 1
  fi

  print_success "Memória estrutura válida"
  return 0
}

# Get memory stats
get_memory_stats() {
  local memory_path="$(get_project_root)/$(get_config memory_path)"

  if [[ ! -d "$memory_path" ]]; then
    return 1
  fi

  local file_count=$(find "$memory_path" -name "*.md" -type f | wc -l)
  local total_size=$(du -sh "$memory_path" 2>/dev/null | awk '{print $1}')
  local latest_file=$(ls -t "$memory_path"/*.md 2>/dev/null | head -1)
  local latest_mtime=$(get_file_mtime "$latest_file" 2>/dev/null || echo "n/a")

  echo "$file_count"
  echo "$total_size"
  echo "$latest_mtime"
}

export -f get_project_root get_config print_info print_success print_warning print_error print_section
export -f expand_path file_exists dir_exists get_file_mtime get_file_size list_files_formatted
export -f get_launchagent_status count_lines is_valid_json create_backup show_tail
export -f validate_memory get_memory_stats
export RED GREEN YELLOW BLUE GRAY NC
