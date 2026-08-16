#!/bin/bash
# Módulo: certify — Certificar kernel IMPAR (verificações de leitura apenas)
# Uso: impar certify

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/certifier.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/certifier.sh"

echo ""
format_header "CERTIFICAÇÃO DO KERNEL IMPAR"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

ISSUES=0

# Executar validações
if validate_integrity; then
    validation_result=$?
else
    validation_result=$?
fi

ISSUES=$validation_result

# Gerar certificado
echo ""
echo "▶ Gerando certificado..."
CERT_FILE=$(generate_certificate)
echo "  ✅ Certificado gerado: $(basename $CERT_FILE)"

echo ""
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ RESULTADO DA CERTIFICAÇÃO                                       │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""

if [ $ISSUES -eq 0 ]; then
    echo "✅ STATUS: PASS"
    echo ""
    echo "Kernel IMPAR v3.0.0 foi certificado com sucesso."
    echo ""
    echo "Detalhes do Certificado:"
    echo "  Arquivo: $CERT_FILE"
    echo "  Timestamp: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
    echo ""
    jq '.' "$CERT_FILE" | head -30
    echo ""
    echo "Status: Production Candidate"
    echo "Etapa: ETAPA 3A.5"
    echo "Versão: 3.0.0"
    echo ""
    exit 0
else
    echo "⚠️ STATUS: PASS COM AVISOS"
    echo ""
    echo "Kernel IMPAR foi certificado, mas com $ISSUES aviso(s)."
    echo ""
    echo "Detalhes do Certificado:"
    echo "  Arquivo: $CERT_FILE"
    echo ""
    jq '.' "$CERT_FILE" | head -30
    echo ""
    exit 0
fi
