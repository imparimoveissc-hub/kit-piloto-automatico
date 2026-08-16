#!/bin/bash

# impar map module - Generate architecture map

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
AUTOMATION_PATH="$PROJECT_ROOT/18_AUTOMATION_STACK"

main() {
  print_section "MAP — Mapa de Arquitetura"

  generate_architecture_map
}

generate_architecture_map() {
  echo "Automações Impar Imóveis"
  echo "========================"
  echo ""

  # Marketplace
  local marketplace_dir="$AUTOMATION_PATH/impar-facebook-marketplace-posting"
  if [[ -d "$marketplace_dir" ]]; then
    print_automation_tree "Marketplace + Grupos" "$marketplace_dir"
  fi

  # Leads
  local leads_dir="$AUTOMATION_PATH/chaves-na-mao-lead-checker"
  if [[ -d "$leads_dir" ]]; then
    print_automation_tree "Leads Chaves na Mão" "$leads_dir"
  fi

  # CRM Sync Rogga
  local rogga_dir="$AUTOMATION_PATH/impar-atualizacao-rogga-imobibrasil"
  if [[ -d "$rogga_dir" ]]; then
    print_automation_tree "Sincronização Rogga" "$rogga_dir"
  fi

  # CRM Sync Grupo JM
  local grupo_dir="$AUTOMATION_PATH/impar-atualizacao-grupo-jm-imobibrasil"
  if [[ -d "$grupo_dir" ]]; then
    print_automation_tree "Sincronização Grupo JM" "$grupo_dir"
  fi

  # NFS-e
  local nfse_dir="$AUTOMATION_PATH/nfem-joinville"
  if [[ -d "$nfse_dir" ]]; then
    print_automation_tree "Emissão NFS-e" "$nfse_dir"
  fi

  # Vídeo
  local video_dir="$AUTOMATION_PATH/cinematic-video-editor"
  if [[ -d "$video_dir" ]]; then
    print_automation_tree "Vídeo Cinematográfico" "$video_dir"
  fi

  echo ""
  print_section "Legenda"

  echo "  ├─ Scripts     — Código Python/Shell"
  echo "  ├─ LaunchAgent — Agendamento no macOS"
  echo "  ├─ Logs        — Histórico de execução"
  echo "  └─ Checkpoint  — Estado persistente"
  echo ""
}

print_automation_tree() {
  local name="$1"
  local path="$2"

  echo "$(basename "$path")"
  echo "├─ Nome: $name"

  # Scripts
  if [[ -f "$path/main.py" ]] || \
     [[ -f "$path/automation.py" ]] || \
     [[ -f "$path/run.py" ]]; then
    echo "├─ Scripts"
    [[ -f "$path/main.py" ]] && echo "│  └─ main.py"
    [[ -f "$path/automation.py" ]] && echo "│  └─ automation.py"
    [[ -f "$path/run.py" ]] && echo "│  └─ run.py"
  fi

  # LaunchAgents
  local agents_dir="$(expand_path ~/Library/LaunchAgents)"
  local agent_count=$(find "$agents_dir" -name "*$(basename "$path")*" -type f 2>/dev/null | wc -l)

  if [[ $agent_count -gt 0 ]]; then
    echo "├─ LaunchAgents ($agent_count)"
    find "$agents_dir" -name "*$(basename "$path")*" -type f 2>/dev/null | head -3 | while read -r plist; do
      local agent_name=$(basename "$plist" .plist)
      echo "│  └─ $agent_name"
    done
  fi

  # Logs
  if [[ -d "$path/logs" ]]; then
    local log_count=$(find "$path/logs" -type f 2>/dev/null | wc -l)
    echo "├─ Logs ($log_count arquivos)"
  fi

  # Checkpoint
  if [[ -f "$path/checkpoint.json" ]]; then
    local size=$(get_file_size "$path/checkpoint.json")
    echo "├─ Checkpoint ($size)"
  fi

  # README
  if [[ -f "$path/README.md" ]]; then
    local desc=$(head -1 "$path/README.md" | sed 's/^[#]* //')
    echo "└─ 📄 $desc"
  fi

  echo ""
}

main "$@"
