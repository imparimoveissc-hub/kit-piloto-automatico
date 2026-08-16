#!/bin/bash

# impar discover module - Discover and register automations

set -euo pipefail

source "$(dirname "$0")/../lib/common.sh"

PROJECT_ROOT="$(get_project_root)"
AUTOMATION_PATH="$PROJECT_ROOT/18_AUTOMATION_STACK"
REGISTRY_FILE="$PROJECT_ROOT/.impar/registry.json"

main() {
  print_section "DISCOVER — Encontrar e Registrar Automações"

  if [[ ! -d "$AUTOMATION_PATH" ]]; then
    print_error "Diretório de automações não encontrado: $AUTOMATION_PATH"
    return 1
  fi

  print_info "Buscando automações em: $AUTOMATION_PATH"
  echo ""

  discover_automations
  generate_registry

  print_section "Descoberta Concluída"
  print_success "Registry atualizado: $REGISTRY_FILE"
  echo ""
}

discover_automations() {
  local automation_dirs=()
  local count=0

  # Procurar por diretórios de automação
  while IFS= read -r dir; do
    local dirname=$(basename "$dir")

    # Skip: templates, skills, tasks, agents, deploy, .cache, .venv, .pytest_cache
    if [[ "$dirname" == "templates" ]] || \
       [[ "$dirname" == "skills" ]] || \
       [[ "$dirname" == "tasks" ]] || \
       [[ "$dirname" == "agents" ]] || \
       [[ "$dirname" == "deploy" ]] || \
       [[ "$dirname" == ".enhance_cache" ]] || \
       [[ "$dirname" == ".venv" ]] || \
       [[ "$dirname" == ".pytest_cache" ]]; then
      continue
    fi

    # Skip: subdirectórios de automações
    if [[ "$dirname" == "logs" ]] || \
       [[ "$dirname" == "config" ]] || \
       [[ "$dirname" == "data" ]] || \
       [[ "$dirname" == "src" ]] || \
       [[ "$dirname" == "tests" ]]; then
      continue
    fi

    automation_dirs+=("$dir")
    count=$((count + 1))
  done < <(find "$AUTOMATION_PATH" -maxdepth 1 -type d | grep -v "^$AUTOMATION_PATH$")

  print_info "Automações encontradas: $count"
  echo ""

  # Processar cada automação
  for automation_dir in "${automation_dirs[@]}"; do
    register_automation "$automation_dir"
  done

  echo ""
}

register_automation() {
  local automation_dir="$1"
  local automation_name=$(basename "$automation_dir")

  print_info "Registrando: $automation_name"

  # Descobrir arquivos principais
  local main_script=""
  local readme=""
  local requirements=""

  if [[ -f "$automation_dir/main.py" ]]; then
    main_script="main.py"
  elif [[ -f "$automation_dir/automation.py" ]]; then
    main_script="automation.py"
  elif [[ -f "$automation_dir/run.py" ]]; then
    main_script="run.py"
  fi

  if [[ -f "$automation_dir/README.md" ]]; then
    readme="README.md"
  fi

  if [[ -f "$automation_dir/requirements.txt" ]]; then
    requirements="requirements.txt"
  fi

  # Procurar por LaunchAgent
  local launchagent=""
  if grep -l "com.impar.*${automation_name}" ~/Library/LaunchAgents/*.plist 2>/dev/null | head -1 > /dev/null; then
    launchagent=$(grep -l "com.impar.*${automation_name}" ~/Library/LaunchAgents/*.plist 2>/dev/null | head -1 | xargs basename | sed 's/.plist//')
  fi

  # Procurar por logs
  local log_file=""
  local log_dir="$automation_dir/logs"
  if [[ -d "$log_dir" ]]; then
    log_file="logs"
  fi

  # Procurar por checkpoint
  local checkpoint=""
  if [[ -f "$automation_dir/checkpoint.json" ]]; then
    checkpoint="checkpoint.json"
  fi

  # Gerar descrição (extrair de README se disponível)
  local description="Automação: $automation_name"
  if [[ -f "$automation_dir/README.md" ]]; then
    description=$(head -1 "$automation_dir/README.md" | sed 's/^# //' | sed 's/^## //')
  fi

  echo "  ✓ $automation_name"
  [[ -n "$main_script" ]] && echo "    Script: $main_script"
  [[ -n "$launchagent" ]] && echo "    LaunchAgent: $launchagent"
  [[ -n "$checkpoint" ]] && echo "    Checkpoint: $checkpoint"
}

generate_registry() {
  print_section "Gerar Registry Central"

  # Python script para gerar JSON registry
  local python_script='
import json
import os
from pathlib import Path

automation_path = "'$AUTOMATION_PATH'"
registry = {
  "version": "1.0.0",
  "generated": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
  "automations": []
}

# Procurar automações
for item in sorted(os.listdir(automation_path)):
  item_path = os.path.join(automation_path, item)

  # Skip diretórios do sistema
  if item in ["templates", "skills", "tasks", "agents", "deploy", ".enhance_cache", ".venv", ".pytest_cache"]:
    continue

  if not os.path.isdir(item_path):
    continue

  # Descobrir informações da automação
  auto = {
    "name": item,
    "path": "18_AUTOMATION_STACK/" + item,
    "type": "unknown",
    "description": "",
    "files": {
      "main_script": "",
      "readme": "",
      "requirements": "",
      "checkpoint": "",
      "logs": ""
    },
    "launchagent": "",
    "status": "unknown"
  }

  # Descobrir tipo
  if "marketplace" in item:
    auto["type"] = "marketplace"
  elif "leads" in item or "chaves-na-mao" in item:
    auto["type"] = "leads"
  elif "nfem" in item or "nfse" in item:
    auto["type"] = "nfse"
  elif "rogga" in item or "imobibrasil" in item:
    auto["type"] = "crm_sync"
  elif "video" in item:
    auto["type"] = "video"

  # Procurar arquivos
  if os.path.isfile(os.path.join(item_path, "main.py")):
    auto["files"]["main_script"] = "main.py"
  elif os.path.isfile(os.path.join(item_path, "automation.py")):
    auto["files"]["main_script"] = "automation.py"
  elif os.path.isfile(os.path.join(item_path, "run.py")):
    auto["files"]["main_script"] = "run.py"

  if os.path.isfile(os.path.join(item_path, "README.md")):
    auto["files"]["readme"] = "README.md"
    try:
      with open(os.path.join(item_path, "README.md")) as f:
        auto["description"] = f.readline().replace("#", "").strip()
    except:
      pass

  if os.path.isfile(os.path.join(item_path, "requirements.txt")):
    auto["files"]["requirements"] = "requirements.txt"

  if os.path.isfile(os.path.join(item_path, "checkpoint.json")):
    auto["files"]["checkpoint"] = "checkpoint.json"

  if os.path.isdir(os.path.join(item_path, "logs")):
    auto["files"]["logs"] = "logs/"

  registry["automations"].append(auto)

# Escrever registry
with open("'$REGISTRY_FILE'", "w") as f:
  json.dump(registry, f, indent=2, ensure_ascii=False)
'

  python3 << EOF 2>/dev/null || true
$python_script
EOF

  if [[ -f "$REGISTRY_FILE" ]]; then
    print_success "Registry criado: $REGISTRY_FILE"
    local count=$(python3 -c "import json; print(len(json.load(open('$REGISTRY_FILE'))))" 2>/dev/null || echo "?")
    print_info "Automações registradas: $count"
  else
    print_warning "Registry não foi criado"
  fi

  echo ""
}

main "$@"
