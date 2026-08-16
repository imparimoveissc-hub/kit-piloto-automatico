#!/bin/bash

# impar explain module - Detailed component explanation

set -euo pipefail

# Source libraries from .impar/lib
LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/intent.sh"
source "$LIB_DIR/format.sh"

main() {
  local name="${1:-}"

  if [[ -z "$name" ]]; then
    print_error "Forneça um nome de automação."
    echo ""
    echo "Exemplos:"
    echo "  impar explain marketplace"
    echo "  impar explain messenger"
    echo "  impar explain leads"
    return 1
  fi

  format_header "EXPLAIN — Detalhes da Automação"
  echo "Automação: $name"
  echo ""

  local registry="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"

  if [[ ! -f "$registry" ]]; then
    print_error "Registry não encontrado"
    return 1
  fi

  # Get and display automation info
  python3 << PYSCRIPT
import json
import sys

name = "$name".lower()
registry = "$registry"

try:
  with open(registry) as f:
    data = json.load(f)

    # Search by canonical name or alias
    target = None
    for auto in data.get('automations', []):
      if auto['name_canonical'].lower() == name or name in [a.lower() for a in auto.get('aliases', [])]:
        target = auto
        break

    if not target:
      print(f"Automação '{name}' não encontrada", file=sys.stderr)
      sys.exit(1)

    # Display all fields
    print(f"Nome Canônico: {target['name_canonical']}")
    print(f"Aliases: {', '.join(target.get('aliases', []))}")
    print()

    print("Informações Gerais:")
    print(f"  • Tipo: {target['type']}")
    print(f"  • Categoria: {target['category']}")
    print(f"  • Status: {target['status']}")
    print(f"  • Risco: {target['risk_level']}")
    print()

    print("Descrição:")
    print(f"  {target['description']}")
    print()

    if target.get('entry_point'):
      print(f"Ponto de Entrada: {target['entry_point']}")
      print()

    if target.get('launchagents'):
      print(f"LaunchAgents Associados:")
      for agent in target['launchagents']:
        print(f"  • {agent}")
      print()

    if target.get('dependencies'):
      print(f"Dependências:")
      for dep in target['dependencies']:
        print(f"  • {dep}")
      print()

    if target.get('security_notes'):
      print(f"Notas de Segurança:")
      print(f"  {target['security_notes']}")
      print()

    if target.get('known_issues'):
      print(f"Problemas Conhecidos:")
      for issue in target['known_issues']:
        print(f"  • {issue}")
      print()

    print(f"Modo: {target.get('mode', 'N/A')}")
    print(f"Restrições: {target.get('restrictions', 'Nenhuma')}")
    print()

except Exception as e:
  print(f"Erro: {e}", file=sys.stderr)
  sys.exit(1)

PYSCRIPT

  echo ""
  echo "Para mais informações:"
  echo "  impar run $name        — Como executar manualmente"
  echo "  impar ask \"sobre $name\"  — Pergunta em linguagem natural"
  echo ""
  format_sources "registry.json"
}

main "$@"
