#!/bin/bash

# impar graph module - Show operational graph summary

set -euo pipefail

LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

GRAPH_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/graph.json"
KNOWLEDGE_DIR="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge"

main() {
  format_header "GRAPH — Grafo Operacional"
  echo ""

  if [[ ! -f "$GRAPH_FILE" ]]; then
    print_error "Grafo não encontrado. Execute: impar graph --refresh"
    return 1
  fi

  python3 << PYSCRIPT
import json
import os
from datetime import datetime

graph_file = "$GRAPH_FILE"

try:
  with open(graph_file) as f:
    graph = json.load(f)

  # Display summary
  summary = graph.get('summary', {})
  print("📊 RESUMO DO GRAFO")
  print()
  print(f"  Automações:")
  print(f"    • Ativas: {summary.get('active_automations', 0)}")
  print(f"    • Offline: {summary.get('offline_automations', 0)}")
  print(f"    • Pausadas: {summary.get('paused_automations', 0)}")
  print(f"    • Total: {summary.get('total_automations', 0)}")
  print()

  print(f"  Componentes:")
  print(f"    • LaunchAgents: {summary.get('total_launchagents', 0)}")
  print(f"    • Dependências: {summary.get('total_dependencies', 0)}")
  print(f"    • Arquivos críticos: {summary.get('critical_files', 0)}")
  print()

  print(f"  Riscos:")
  print(f"    • Identificados: {summary.get('identified_risks', 0)}")
  print(f"    • CRÍTICOS: {summary.get('critical_risks', 0)}")
  print()

  print(f"  Qualidade:")
  print(f"    • Fontes consultadas: {summary.get('sources_consulted', 0)}")
  print(f"    • Última verificação: {summary.get('verified_at', 'N/A')}")
  print()

  # Display health
  health = graph.get('health', {})
  print(f"🏥 SAÚDE DO SISTEMA")
  print()
  print(f"  Status Geral: {health.get('overall_status', 'UNKNOWN')}")
  print(f"  Problemas Críticos: {health.get('critical_issues', 0)}")
  print(f"  Recomendações: {health.get('recommendations', 0)}")
  print(f"  Último Incidente: {health.get('last_incident', 'Nenhum')}")
  print()

  # Display commands
  print("📡 COMANDOS DISPONÍVEIS")
  print()
  endpoints = graph.get('query_endpoints', {})
  for cmd, desc in endpoints.items():
    print(f"  • {cmd}: {desc}")
  print()

except Exception as e:
  print(f"❌ Erro: {e}", file=__import__('sys').stderr)
  import sys
  sys.exit(1)

PYSCRIPT

  echo ""
  echo "💡 Para mais detalhes:"
  echo "  impar deps <automação>         — Dependências"
  echo "  impar impact <automação>       — Simular impacto"
  echo "  impar critical                 — Arquivos críticos"
  echo "  impar topology                 — Estrutura hierárquica"
  echo "  impar relations <componente>   — Todas as relações"
  echo ""
  format_sources "graph.json", "knowledge/*.json"
}

main "$@"
