#!/bin/bash

# impar relations module - Show all relations for a component

set -euo pipefail

LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

DEPENDENCIES_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/dependencies.json"

main() {
  local name="${1:-}"

  if [[ -z "$name" ]]; then
    print_error "Forneça um nome de componente."
    echo ""
    echo "Exemplos:"
    echo "  impar relations marketplace"
    echo "  impar relations whatsapp"
    echo "  impar relations browser-pane"
    return 1
  fi

  format_header "RELATIONS — Relações de Componente"
  echo "Componente: $name"
  echo ""

  python3 << PYSCRIPT
import json
import sys

deps_file = "$DEPENDENCIES_FILE"
name = "$name".lower()

try:
  with open(deps_file) as f:
    data = json.load(f)

  relations = data.get('relations', [])

  # Find outgoing and incoming relations
  outgoing = []
  incoming = []

  for rel in relations:
    source = rel.get('source', '').lower()
    target = rel.get('target', '').lower()

    if name in source or name in rel.get('source', '').lower():
      outgoing.append(rel)
    if name in target or name in rel.get('target', '').lower():
      incoming.append(rel)

  if not outgoing and not incoming:
    print(f"❌ Componente '{name}' não encontrado em relações")
    sys.exit(1)

  print("🔗 RELAÇÕES OUTGOING (dependências):")
  print()
  if outgoing:
    for rel in outgoing:
      rel_type = rel.get('relation_type', 'unknown')
      target = rel.get('target', 'Unknown')
      criticality = rel.get('criticality', 'N/A')
      print(f"  → {target}")
      print(f"    Tipo: {rel_type}")
      print(f"    Criticidade: {criticality}")
      print(f"    Descrição: {rel.get('description', 'N/A')}")
      print()
  else:
    print("  Nenhuma relação outgoing")
  print()

  print("⬅️  RELAÇÕES INCOMING (dependentes):")
  print()
  if incoming:
    for rel in incoming:
      rel_type = rel.get('relation_type', 'unknown')
      source = rel.get('source', 'Unknown')
      criticality = rel.get('criticality', 'N/A')
      print(f"  ← {source}")
      print(f"    Tipo: {rel_type}")
      print(f"    Criticidade: {criticality}")
      print(f"    Descrição: {rel.get('description', 'N/A')}")
      print()
  else:
    print("  Nenhuma relação incoming")
  print()

  print(f"📊 RESUMO:")
  print(f"  Relações outgoing: {len(outgoing)}")
  print(f"  Relações incoming: {len(incoming)}")
  print(f"  Total: {len(outgoing) + len(incoming)}")
  print()

except Exception as e:
  print(f"❌ Erro: {e}", file=sys.stderr)
  sys.exit(1)

PYSCRIPT

  echo ""
  format_sources "dependencies.json"
}

main "$@"
