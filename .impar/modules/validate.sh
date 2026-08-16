#!/bin/bash
# Módulo: validate — Validar automação (leitura apenas)
# Uso: impar validate <automacao>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/validator.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/validator.sh"

AUTOMATION="${1:-}"

if [ -z "$AUTOMATION" ]; then
    echo "Erro: Especifique uma automação"
    echo "Uso: impar validate <automacao>"
    exit 1
fi

echo ""
format_header "VALIDAÇÃO DE AUTOMAÇÃO (LEITURA APENAS)"
echo "Automação: $AUTOMATION"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Contadores
PASSED=0
FAILED=0
WARNINGS=0

# 1. Validar existência
echo "▶ Verificando existência da automação..."
if validate_automation_exists "$AUTOMATION"; then
    ((PASSED++))
else
    ((FAILED++))
    echo "❌ Automação não encontrada, encerrando"
    exit 1
fi
echo ""

# 2. Validar integridade do registry
echo "▶ Validando integridade do registry..."
if validate_registry_integrity; then
    ((PASSED++))
else
    ((FAILED++))
fi
echo ""

# 3. Validar integridade do grafo
echo "▶ Validando integridade do grafo operacional..."
if validate_graph_integrity; then
    ((PASSED++))
else
    ((FAILED++))
fi
echo ""

# 4. Validar LaunchAgents
echo "▶ Validando LaunchAgents..."
if validate_launchagents "$AUTOMATION"; then
    ((PASSED++))
else
    ((WARNINGS++))
fi
echo ""

# 5. Validar checkpoints
echo "▶ Validando checkpoints..."
if validate_checkpoints "$AUTOMATION"; then
    ((PASSED++))
else
    ((WARNINGS++))
fi
echo ""

# 6. Verificar conflitos
echo "▶ Verificando conflitos com outras automações..."
if check_for_conflicts "$AUTOMATION"; then
    ((PASSED++))
else
    ((WARNINGS++))
fi
echo ""

# 7. Verificar riscos bloqueantes
echo "▶ Verificando riscos bloqueantes..."
if check_blocking_risks "$AUTOMATION"; then
    ((PASSED++))
else
    ((FAILED++))
fi
echo ""

# Resumo
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ RESUMO DE VALIDAÇÃO                                             │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  ✅ Validações passaram:  $PASSED"
echo "  ⚠️  Avisos:              $WARNINGS"
echo "  ❌ Validações falharam:  $FAILED"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "✅ Automação está pronta para simulação"
    echo "   Execute 'impar plan $AUTOMATION' para gerar plano"
    echo "   Execute 'impar dry-run $AUTOMATION' para simular execução"
    echo ""
    exit 0
else
    echo "❌ Automação não está validada, corrija os problemas"
    echo ""
    exit 1
fi
