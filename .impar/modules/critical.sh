#!/bin/bash

# impar critical module - List critical files and components

set -euo pipefail

LIB_DIR="$(dirname "$0")/../lib"
source "$LIB_DIR/common.sh"
source "$LIB_DIR/format.sh"

CRITICAL_FILES_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/critical-files.json"
RISKS_FILE="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/knowledge/risks.json"

main() {
  format_header "CRITICAL — Componentes Críticos"
  echo ""

  python3 << PYSCRIPT
import json

critical_files = "$CRITICAL_FILES_FILE"
risks_file = "$RISKS_FILE"

try:
  with open(critical_files) as f:
    cf = json.load(f)

  with open(risks_file) as f:
    risks = json.load(f)

  files = cf.get('files', [])
  all_risks = risks.get('risks', [])

  print("📁 ARQUIVOS CRÍTICOS (10 mapeados)")
  print()

  critical = [f for f in files if f.get('criticality') == 'CRITICAL']
  print(f"🔴 CRÍTICOS ({len(critical)}):")
  for f in critical:
    print(f"  • {f.get('path', 'Unknown')}")
    print(f"    Tipo: {f.get('type', 'N/A')}")
    print(f"    Impacto de perda: {f.get('loss_impact', 'N/A')[:60]}...")
  print()

  high = [f for f in files if f.get('criticality') == 'HIGH']
  print(f"🟠 ALTOS ({len(high)}):")
  for f in high:
    print(f"  • {f.get('path', 'Unknown')}")
    print(f"    Tipo: {f.get('type', 'N/A')}")
  print()

  print("⏸️  COMPONENTES DESLIGADOS INTENCIONALMENTE:")
  print()
  print("  • WhatsApp Bridge (status: offline)")
  print("    Motivo: Testes de segurança")
  print("    Reativação: ❌ PROIBIDA sem autorização formal")
  print()

  print("📊 RISCOS CRÍTICOS (6 identificados):")
  print()
  critical_risks = [r for r in all_risks if r.get('severity') == 'CRITICAL']
  for risk in critical_risks[:3]:
    print(f"  • {risk.get('title', 'Unknown')}")
    print(f"    Frequência: {risk.get('frequency', 'N/A')}")
  if len(critical_risks) > 3:
    print(f"  ... e {len(critical_risks) - 3} mais")
  print()

  print("⚠️  RECOMENDAÇÕES:")
  print()
  print("  ✓ Nunca modificar filas CSV manualmente")
  print("  ✓ Nunca deletar checkpoints")
  print("  ✓ Nunca expor .env files")
  print("  ✓ Backup diário de checkpoints/filas")
  print("  ✓ Restaurar apenas com autorização explícita")
  print()

except Exception as e:
  print(f"❌ Erro: {e}", file=__import__('sys').stderr)
  import sys
  sys.exit(1)

PYSCRIPT

  echo ""
  format_sources "critical-files.json", "risks.json"
}

main "$@"
