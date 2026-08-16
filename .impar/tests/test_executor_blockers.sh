#!/bin/bash
# Testes de Bloqueio — ETAPA 3A Executor
# Verifica que automações proibidas são bloqueadas

set -euo pipefail

PROJECT_ROOT="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB"
BINARY="$PROJECT_ROOT/.local/bin/impar"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PASSED=0
FAILED=0

test_blocker() {
    local test_number="$1"
    local test_name="$2"
    local service="$3"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "TESTE $test_number: $test_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Tentativa: plan-execution $service"
    echo ""

    output=$("$BINARY" plan-execution "$service" 2>&1 || true)

    if echo "$output" | grep -q "não autorizado\|não está na whitelist"; then
        echo -e "${GREEN}✅ PASSOU — Serviço bloqueado corretamente${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FALHOU — Serviço deveria estar bloqueado${NC}"
        echo "Saída:"
        echo "$output" | head -10
        ((FAILED++))
    fi
}

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║    TESTES DE BLOQUEIO — ETAPA 3A EXECUTOR                         ║"
echo "║    Verificar que apenas impar-update-current-state é permitido    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Testes de bloqueio para automações proibidas
test_blocker "1" "Bloquear WhatsApp Bridge" "impar-whatsapp-bridge"
test_blocker "2" "Bloquear Messenger Bridge" "impar-messenger-bridge"
test_blocker "3" "Bloquear Marketplace Publishing" "impar-facebook-marketplace-posting"
test_blocker "4" "Bloquear Notificar Leads" "impar-notificar-leads"
test_blocker "5" "Bloquear Chaves na Mão Leads" "chaves-na-mao-lead-checker"
test_blocker "6" "Bloquear NFS-e" "nfem-joinville"
test_blocker "7" "Bloquear Cadastrar Imóveis" "impar-cadastrar-imoveis"
test_blocker "8" "Bloquear Rogga Sync" "impar-atualizacao-rogga-imobibrasil"
test_blocker "9" "Bloquear Grupo JM Sync" "impar-atualizacao-grupo-jm-imobibrasil"

# Teste de autorização válida
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TESTE 10: Autorizar impar-update-current-state"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tentativa: plan-execution impar-update-current-state"
echo ""

output=$("$BINARY" plan-execution "impar-update-current-state" 2>&1 || true)

if echo "$output" | grep -q "Hash do plano"; then
    echo -e "${GREEN}✅ PASSOU — Serviço autorizado, plano gerado${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ FALHOU — Serviço deveria estar autorizado${NC}"
    echo "Saída:"
    echo "$output" | head -10
    ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RESUMO DE TESTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "  ✅ Testes passaram:  ${GREEN}$PASSED${NC}"
echo -e "  ❌ Testes falharam:  ${RED}$FAILED${NC}"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}✅ TODOS OS TESTES DE BLOQUEIO PASSARAM${NC}"
    echo ""
    echo "CONCLUSÃO: Executor está seguro para piloto"
    echo "           Apenas impar-update-current-state é autorizado"
    echo ""
    exit 0
else
    echo -e "${RED}❌ ALGUNS TESTES FALHARAM${NC}"
    echo ""
    exit 1
fi
