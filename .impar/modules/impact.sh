#!/bin/bash

# impar impact module - Simulate impact of stopping an automation

set -euo pipefail

LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

TOPOLOGY_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/topology.json"
RISKS_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/risks.json"

main() {
  local name="${1:-}"

  if [[ -z "$name" ]]; then
    print_error "Forneça um nome de componente."
    echo ""
    echo "Exemplos:"
    echo "  impar impact marketplace"
    echo "  impar impact messenger"
    echo "  impar impact browser-pane"
    return 1
  fi

  format_header "IMPACT — Simulação de Parada"
  echo "⚠️  SIMULAÇÃO — Nenhuma ação foi executada"
  echo "Componente: $name"
  echo ""

  python3 << PYSCRIPT
import json
import sys

topology_file = "$TOPOLOGY_FILE"
risks_file = "$RISKS_FILE"
name = "$name".lower()

try:
  # Load data
  with open(topology_file) as f:
    topology = json.load(f)
  with open(risks_file) as f:
    risks = json.load(f)

  automations = topology.get('automations', {})
  all_risks = risks.get('risks', [])

  # Find automation
  target_auto = None
  for auto_key, auto_data in automations.items():
    if name in auto_data.get('name', '').lower() or \
       name in auto_key.lower():
      target_auto = auto_key
      break

  if not target_auto:
    print(f"❌ Componente '{name}' não encontrado")
    sys.exit(1)

  auto = automations[target_auto]
  auto_name = auto.get('name', 'Unknown')

  print(f"📊 CENÁRIO: Se '{auto_name}' for parado/removido")
  print()

  # Direct impact
  print("🔴 IMPACTO DIRETO:")
  print()
  print(f"  • {auto_name} deixaria de funcionar completamente")
  if auto.get('status') == 'active':
    print(f"  • Cadência interrompida")
  if auto.get('launchagents'):
    print(f"  • {len(auto.get('launchagents', []))} LaunchAgent(s) sem efeito")
  print()

  # Dependent automations
  print("🔶 AUTOMAÇÕES DEPENDENTES:")
  print()
  dependents = []
  for auto_key2, auto_data2 in automations.items():
    if auto_key2 != target_auto:
      deps = [d.get('name', '') for d in auto_data2.get('dependencies', [])]
      if any(auto_name.lower() in d.lower() for d in deps):
        dependents.append(auto_data2.get('name', auto_key2))

  if dependents:
    for dep in dependents:
      print(f"  • {dep} deixaria de funcionar (falta dependência)")
  else:
    print("  • Nenhuma automação depende diretamente")
  print()

  # Checkpoint impact
  print("💾 RISCO DE CHECKPOINT:")
  print()
  checkpoints = auto.get('checkpoints', [])
  if checkpoints:
    critical_cps = [cp for cp in checkpoints if cp.get('criticality') == 'CRITICAL']
    if critical_cps:
      print(f"  🔴 {len(critical_cps)} checkpoint(s) CRÍTICO(S):")
      for cp in critical_cps:
        loss = cp.get('loss_impact', 'Desconhecido')
        print(f"     • {cp.get('file', 'Unknown')}: {loss}")
    else:
      print("  ✅ Nenhum checkpoint crítico")
  else:
    print("  ✅ Nenhum checkpoint")
  print()

  # Queue impact
  print("📋 RISCO DE FILA:")
  print()
  artifacts = auto.get('artifacts', {})
  queues = artifacts.get('queues', [])
  if queues:
    print(f"  🔴 {len(queues)} fila(s) afetada(s):")
    for queue in queues:
      print(f"     • {queue}")
  else:
    print("  ✅ Nenhuma fila será afetada")
  print()

  # Duplicate risk
  print("⚠️  RISCO DE DUPLICAÇÃO:")
  print()
  auto_risks = [r for r in all_risks if name in r.get('automation', '').lower()]
  dup_risks = [r for r in auto_risks if 'duplicate' in r.get('title', '').lower()]
  if dup_risks:
    print(f"  🔴 Alto risco de duplicatas ao reiniciar:")
    for risk in dup_risks:
      print(f"     • {risk.get('title', 'Unknown')}")
  else:
    print("  ✅ Baixo risco de duplicatas")
  print()

  # Recommendation
  print("💡 RECOMENDAÇÃO:")
  print()
  print("  ⚠️  SIMULAÇÃO APENAS — Nenhuma ação foi tomada")
  print("  • Para parar com segurança: Contactar Jonata para autorização")
  print("  • Antes de parar: Fazer backup de checkpoints")
  print("  • Após parar: Monitorar automações dependentes")
  print()

except Exception as e:
  print(f"❌ Erro: {e}", file=sys.stderr)
  sys.exit(1)

PYSCRIPT

  echo ""
  format_sources "topology.json", "risks.json"
}

main "$@"
