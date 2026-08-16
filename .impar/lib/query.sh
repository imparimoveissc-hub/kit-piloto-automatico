#!/bin/bash

# Library for querying authorized sources

set -euo pipefail

# Query current state
get_current_state() {
  local file="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/07_LOGS/CURRENT_STATE.md"

  if [[ -f "$file" ]]; then
    head -50 "$file"
  fi
}

# Get automation status from registry
get_status() {
  local name="${1:-}"
  local registry="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"

  python3 << 'PYSCRIPT' 2>/dev/null || echo "unknown"
import json
import sys

registry = "$registry"
name = "$name"

try:
  with open(registry) as f:
    data = json.load(f)
    for auto in data.get('automations', []):
      if auto['name_canonical'] == name:
        print(f"{auto['status']} ({auto['risk_level']})")
        return
except:
  pass

print("unknown")
PYSCRIPT
}

# Get offline automations
get_offline_automations() {
  local registry="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"

  python3 << 'PYSCRIPT' 2>/dev/null || echo ""
import json

registry = "$registry"

try:
  with open(registry) as f:
    data = json.load(f)
    for auto in data.get('automations', []):
      if auto['status'] in ['offline', 'paused']:
        print(f"  - {auto['name_canonical']}: {auto['status']}")
except:
  pass
PYSCRIPT
}

# Get critical automations
get_critical_automations() {
  local registry="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"

  python3 << 'PYSCRIPT' 2>/dev/null || echo ""
import json

registry = "$registry"

try:
  with open(registry) as f:
    data = json.load(f)
    for auto in data.get('automations', []):
      if auto['risk_level'] == 'CRITICAL':
        print(f"  - {auto['name_canonical']}: {auto['status']}")
except:
  pass
PYSCRIPT
}

# Get memory status
get_memory_info() {
  local memory_path="/Users/usuario/.claude/projects/-Users-usuario-Library-Mobile-Documents-com-apple-CloudDocs-Kit-Piloto-Automatico-V30-DISTRIB/memory"

  if [[ -d "$memory_path" ]]; then
    local count=$(find "$memory_path" -name "*.md" -type f 2>/dev/null | wc -l)
    local size=$(du -sh "$memory_path" 2>/dev/null | awk '{print $1}')
    echo "Memória: $count arquivos, $size"
  fi
}

# Get last logs
get_last_logs() {
  local module="${1:-}"
  local logs_path="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/07_LOGS"

  case "$module" in
    marketplace)
      tail -5 "$logs_path/marketplace-rodadas.md" 2>/dev/null || echo "Sem logs"
      ;;
    messenger)
      tail -5 "$logs_path/messenger-rodadas.md" 2>/dev/null || echo "Sem logs"
      ;;
    *)
      echo "Logs não disponíveis"
      ;;
  esac
}

export -f get_current_state get_status get_offline_automations get_critical_automations get_memory_info get_last_logs
