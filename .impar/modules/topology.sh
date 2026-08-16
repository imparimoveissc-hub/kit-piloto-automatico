#!/bin/bash

# impar topology module - Show hierarchical structure

set -euo pipefail

LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

TOPOLOGY_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/topology.json"

main() {
  format_header "TOPOLOGY — Estrutura Hierárquica"
  echo ""

  python3 << PYSCRIPT
import json

topology_file = "$TOPOLOGY_FILE"

try:
  with open(topology_file) as f:
    data = json.load(f)

  automations = data.get('automations', {})

  for auto_key, auto in automations.items():
    name = auto.get('name', 'Unknown')
    status = auto.get('status', 'unknown')
    risk = auto.get('risk', 'UNKNOWN')

    # Status emoji
    status_emoji = "✅" if status == 'active' else "🔴" if status == 'offline' else "⏸️"

    print(f"{status_emoji} {name} ({risk})")
    print(f"   Entrada: {auto.get('entry_point', 'N/A')[:50]}")
    print()

    # LaunchAgents
    agents = auto.get('launchagents', [])
    if agents:
      print(f"   📅 LaunchAgents ({len(agents)}):")
      for agent in agents[:2]:
        if isinstance(agent, dict):
          schedule = agent.get('schedule', 'N/A')
          print(f"      • {agent.get('name', 'Unknown')}: {schedule}")
        else:
          print(f"      • {agent}")
      if len(agents) > 2:
        print(f"      ... +{len(agents) - 2} mais")
    print()

    # Dependencies
    deps = auto.get('dependencies', [])
    if deps:
      print(f"   📦 Dependências ({len(deps)}):")
      for dep in deps[:3]:
        dep_type = dep.get('type', 'unknown')
        criticality = dep.get('criticality', 'N/A')
        print(f"      • {dep.get('name', 'Unknown')} ({dep_type}) — {criticality}")
      if len(deps) > 3:
        print(f"      ... +{len(deps) - 3} mais")
    print()

    # Checkpoints
    checkpoints = auto.get('checkpoints', [])
    if checkpoints:
      print(f"   💾 Checkpoints ({len(checkpoints)}):")
      for cp in checkpoints:
        print(f"      • {cp.get('file', 'Unknown')} ({cp.get('type', 'N/A')})")
    print()

    # Integrations
    integrations = auto.get('integrations', [])
    if integrations:
      print(f"   🔌 Integrações ({len(integrations)}):")
      for integration in integrations[:3]:
        print(f"      • {integration}")
      if len(integrations) > 3:
        print(f"      ... +{len(integrations) - 3} mais")
    print()

    # Risks
    risks = auto.get('risks', [])
    if risks:
      print(f"   ⚠️  Riscos ({len(risks)}):")
      for risk_text in risks[:2]:
        print(f"      • {risk_text[:60]}")
      if len(risks) > 2:
        print(f"      ... +{len(risks) - 2} mais")
    print()

    print()

except Exception as e:
  print(f"❌ Erro: {e}", file=__import__('sys').stderr)
  import sys
  sys.exit(1)

PYSCRIPT

  echo ""
  format_sources "topology.json"
}

main "$@"
