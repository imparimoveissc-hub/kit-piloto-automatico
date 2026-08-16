#!/usr/bin/env bash
set -Eeuo pipefail

RESULTS_FILE="${1:?Arquivo de resultados não fornecido}"

if [ ! -f "$RESULTS_FILE" ]; then
    echo "❌ Arquivo não encontrado: $RESULTS_FILE"
    exit 1
fi

# Validar estrutura JSON
jq empty "$RESULTS_FILE" || { echo "❌ JSON inválido"; exit 1; }

# Extrair valores
EXECUTED=$(jq '.executed' "$RESULTS_FILE")
CORRECTLY_REJECTED=$(jq '.correctly_rejected' "$RESULTS_FILE")
FALSE_ACCEPTS=$(jq '.false_accepts' "$RESULTS_FILE")
TEST_COUNT=$(jq '.tests | length' "$RESULTS_FILE")
FAIL_CLOSED=$(jq -r '.fail_closed_test' "$RESULTS_FILE")

# Validar contagem
if [ "$EXECUTED" -ne 20 ]; then
    echo "❌ Testes executados incorreto: $EXECUTED (esperado 20)"
    exit 1
fi

if [ "$TEST_COUNT" -ne 20 ]; then
    echo "❌ Contagem de testes incorreta: $TEST_COUNT (esperado 20)"
    exit 1
fi

# Validar números
if [ "$CORRECTLY_REJECTED" -ne 20 ]; then
    echo "❌ Testes rejeitados: $CORRECTLY_REJECTED (esperado 20)"
    exit 1
fi

if [ "$FALSE_ACCEPTS" -ne 0 ]; then
    echo "❌ Falsos aceites: $FALSE_ACCEPTS (esperado 0)"
    exit 1
fi

if [ "$FAIL_CLOSED" != "PASS" ]; then
    echo "❌ Fail-closed: $FAIL_CLOSED (esperado PASS)"
    exit 1
fi

# Validar que não há gaps nos números
for i in {1..20}; do
    if ! jq -e ".tests[] | select(.number == $i)" "$RESULTS_FILE" >/dev/null; then
        echo "❌ Falta teste número $i"
        exit 1
    fi
done

# Validar que todos têm passed=true
FAILED_COUNT=$(jq '[.tests[] | select(.passed == false)] | length' "$RESULTS_FILE")
if [ "$FAILED_COUNT" -ne 0 ]; then
    echo "❌ $FAILED_COUNT testes com passed=false"
    exit 1
fi

echo "✅ VALIDAÇÃO COMPLETA"
echo "✅ Executed: $EXECUTED"
echo "✅ Correctly Rejected: $CORRECTLY_REJECTED"
echo "✅ False Accepts: $FALSE_ACCEPTS"
echo "✅ Fail-Closed: $FAIL_CLOSED"
exit 0
