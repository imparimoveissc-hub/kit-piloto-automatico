#!/bin/bash

# impar deps module - Show dependencies for an automation

set -euo pipefail

LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

TOPOLOGY_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/topology.json"
DEPENDENCIES_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/dependencies.json"

main() {
  local name="${1:-}"

  if [[ -z "$name" ]]; then
    print_error "Forneça um nome de automação."
    echo ""
    echo "Exemplos:"
    echo "  impar deps marketplace"
    echo "  impar deps messenger"
    echo "  impar deps leads"
    return 1
  fi

  format_header "DEPS — Dependências"
  echo "Componente: $name"
  echo ""

  python3 << PYSCRIPT
import json
import sys

topology_file = "$TOPOLOGY_FILE"
dependencies_file = "$DEPENDENCIES_FILE"
name = "$name".lower()

try:
  # Load topology
  with open(topology_file) as f:
    topology = json.load(f)

  automations = topology.get('automations', {})
  target_auto = None

  # Find automation by name or alias
  for auto_key, auto_data in automations.items():
    if name in auto_data.get('name', '').lower() or \
       name in auto_key.lower() or \
       any(name in alias.lower() for alias in [auto_data.get('name', '')]):
      target_auto = auto_key
      break

  if not target_auto:
    print(f"❌ Automação '{name}' não encontrada")
    print()
    print("Automações disponíveis:")
    for auto_key, auto_data in automations.items():
      print(f"  • {auto_data.get('name', auto_key)}")
    sys.exit(1)

  auto = automations[target_auto]
  print(f"✅ {auto.get('name', 'Unknown')}")
  print()

  print("🔗 DEPENDÊNCIAS DIRETAS:")
  print()
  deps = auto.get('dependencies', [])
  if deps:
    for dep in deps:
      criticality = dep.get('criticality', 'UNKNOWN')
      dep_type = dep.get('type', 'unknown')
      print(f"  • {dep['name']} ({dep_type}) — {criticality}")
  else:
    print("  Nenhuma")
  print()

  print("📍 LAUNCHAGENTS:")
  print()
  agents = auto.get('launchagents', [])
  if agents:
    for agent in agents:
      if isinstance(agent, dict):
        print(f"  • {agent.get('name', 'Unknown')}")
        print(f"    Agendamento: {agent.get('schedule', 'N/A')}")
        print(f"    Status: {agent.get('status', 'N/A')}")
      else:
        print(f"  • {agent}")
  else:
    print("  Nenhum")
  print()

  print("📁 CHECKPOINTS:")
  print()
  checkpoints = auto.get('checkpoints', [])
  if checkpoints:
    for cp in checkpoints:
      print(f"  • {cp.get('file', 'Unknown')}")
      print(f"    Tipo: {cp.get('type', 'N/A')}")
      print(f"    Criticidade: {cp.get('criticality', 'N/A')}")
  else:
    print("  Nenhum")
  print()

  print("🔌 INTEGRAÇÕES:")
  print()
  integrations = auto.get('integrations', [])
  if integrations:
    for integration in integrations:
      print(f"  • {integration}")
  else:
    print("  Nenhuma")
  print()

  print("⚠️  RISCOS CONHECIDOS:")
  print()
  risks = auto.get('risks', [])
  if risks:
    for risk in risks:
      print(f"  • {risk}")
  else:
    print("  Nenhum")

except Exception as e:
  print(f"❌ Erro: {e}", file=sys.stderr)
  import traceback
  traceback.print_exc()
  sys.exit(1)

PYSCRIPT

  echo ""
  format_sources "topology.json", "dependencies.json"
}

main "$@"
