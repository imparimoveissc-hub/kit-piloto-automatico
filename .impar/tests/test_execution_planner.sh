#!/bin/bash
# Testes para ETAPA 2.95 — Execution Planner

set -euo pipefail

PROJECT_ROOT="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
IMPAR="${PROJECT_ROOT}/.impar"
BINARY="$PROJECT_ROOT/.local/bin/impar"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

test_command() {
    local test_number="$1"
    local test_name="$2"
    local command="$3"
    local expected_pattern="$4"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TESTE $test_number: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Comando: $command"
    echo ""

    output=$(eval "$command" 2>&1 || true)

    if echo "$output" | grep -q "$expected_pattern"; then
        echo -e "${GREEN}✅ PASSOU${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FALHOU${NC}"
        echo "Saída:"
        echo "$output" | head -20
        ((FAILED++))
    fi
}

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║         TESTES DE ETAPA 2.95 — EXECUTION PLANNER                 ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Teste 1: Gerar plano do Marketplace
test_command "1" "Gerar plano do Marketplace" \
    "$BINARY plan impar-facebook-marketplace-posting" \
    "PLANO DE EXECUÇÃO"

# Teste 2: Validar Messenger
test_command "2" "Validar automação Messenger" \
    "$BINARY validate impar-messenger-bridge" \
    "VALIDAÇÃO DE AUTOMAÇÃO"

# Teste 3: Simular Leads
test_command "3" "Simular execução de Leads" \
    "$BINARY dry-run chaves-na-mao-lead-checker" \
    "SIMULAÇÃO DRY-RUN"

# Teste 4: Tentar executar (deve ser bloqueado)
test_command "4" "Bloquear comando --execute" \
    "$BINARY plan impar-facebook-marketplace-posting --execute" \
    "EXECUÇÃO BLOQUEADA|ainda não está habilitada"

# Teste 5: Tentar publicar (deve ser bloqueado)
test_command "5" "Bloquear comando --publish" \
    "$BINARY ask 'rodar marketplace --publish'" \
    "EXECUÇÃO BLOQUEADA|ainda não está habilitada"

# Teste 6: Rotina completa (validate + plan + dry-run)
test_command "6" "Rotina completa: validate + plan" \
    "$BINARY validate impar-facebook-marketplace-posting && $BINARY plan impar-facebook-marketplace-posting" \
    "PLANO DE EXECUÇÃO"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RESUMO DE TESTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "  ✅ Testes passaram:  ${GREEN}$PASSED${NC}"
echo -e "  ❌ Testes falharam:  ${RED}$FAILED${NC}"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✅ TODOS OS TESTES PASSARAM${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ ALGUNS TESTES FALHARAM${NC}"
    echo ""
    exit 1
fi
