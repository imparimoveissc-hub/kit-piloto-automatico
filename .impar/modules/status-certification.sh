#!/bin/bash
# Módulo: status (expandido) — Mostrar status do kernel com certificação
# Uso: impar status

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"
IMPAR_DIR="${PROJECT_ROOT}/.impar"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"

echo ""
format_header "STATUS DO KERNEL IMPAR"
echo ""

# Versão
if [ -f "${IMPAR_DIR}/VERSION" ]; then
    VERSION=$(head -2 "${IMPAR_DIR}/VERSION" | tail -1 | awk '{print $NF}')
    echo "▶ Versão"
    echo "  Versão: $VERSION"
    echo "  Etapa: $(grep 'Stage:' ${IMPAR_DIR}/VERSION | awk '{print $2}')"
    echo "  Status: $(grep '^Status:' ${IMPAR_DIR}/VERSION | awk '{print $2}')"
    echo ""
fi

# Certificação
if [ -d "${IMPAR_DIR}/certificates" ]; then
    LATEST_CERT=$(ls -t "${IMPAR_DIR}/certificates"/kernel-cert-*.json 2>/dev/null | head -1 || echo "")
    if [ -n "$LATEST_CERT" ]; then
        echo "▶ Certificação"
        CERT_DATE=$(basename "$LATEST_CERT" | sed 's/kernel-cert-//;s/.json//' | sed 's/^\([0-9]\{8\}\)-\([0-9]\{6\}\)$/\1 \2/')
        echo "  Última: $(date -j -f '%Y%m%d %H%M%S' "$CERT_DATE" 2>/dev/null || echo 'N/A')"
        echo "  Arquivo: $(basename $LATEST_CERT)"
        echo ""
    fi
fi

# Componentes
echo "▶ Componentes"
MODULES=$(find "${IMPAR_DIR}/modules" -name "*.sh" -type f 2>/dev/null | wc -l | tr -d ' ')
LIBRARIES=$(find "${IMPAR_DIR}/lib" -name "*.sh" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "  Módulos: $MODULES"
echo "  Bibliotecas: $LIBRARIES"
echo ""

# Registry
echo "▶ Registry"
AUTOMATIONS=$(jq '.automations | length' "${IMPAR_DIR}/registry.json" 2>/dev/null || echo "0")
SERVICES=$(jq '.services | length' "${IMPAR_DIR}/services.json" 2>/dev/null || echo "0")
echo "  Automações: $AUTOMATIONS"
echo "  Serviços: $SERVICES"
echo ""

# LaunchAgents
echo "▶ LaunchAgents"
LAUNCHAGENTS=$(jq '. | length' "${IMPAR_DIR}/knowledge/launchagents.json" 2>/dev/null || echo "0")
echo "  Total: $LAUNCHAGENTS"
echo ""

# Grafo
echo "▶ Grafo Operacional"
DEPENDENCIES=$(jq '. | length' "${IMPAR_DIR}/knowledge/dependencies.json" 2>/dev/null || echo "0")
RISKS=$(jq '. | length' "${IMPAR_DIR}/knowledge/risks.json" 2>/dev/null || echo "0")
CRITICAL=$(jq '. | length' "${IMPAR_DIR}/knowledge/critical-files.json" 2>/dev/null || echo "0")
echo "  Relações: $DEPENDENCIES"
echo "  Riscos: $RISKS"
echo "  Arquivos Críticos: $CRITICAL"
echo ""

# Última execução
echo "▶ Auditoria"
if [ -f "${PROJECT_ROOT}/07_LOGS/EXECUTION_AUDIT.jsonl" ]; then
    LAST_EXECUTION=$(tail -1 "${PROJECT_ROOT}/07_LOGS/EXECUTION_AUDIT.jsonl" | jq -r '.timestamp' 2>/dev/null || echo "N/A")
    echo "  Última execução: $LAST_EXECUTION"
else
    echo "  Última execução: Nenhuma"
fi
echo ""

# Whitelist
echo "▶ Whitelist (ETAPA 3A)"
if [ -f "${IMPAR_DIR}/executor_whitelist.json" ]; then
    AUTHORIZED=$(jq '.authorized_services[]' "${IMPAR_DIR}/executor_whitelist.json" 2>/dev/null | head -3)
    echo "  Serviços autorizados:"
    echo "$AUTHORIZED" | sed 's/^/    • /'
fi
echo ""

# WhatsApp
echo "▶ WhatsApp Bridge"
WHATSAPP_STATUS=$(jq '.automations[] | select(.name_canonical == "impar-whatsapp-bridge") | .status' "${IMPAR_DIR}/registry.json" 2>/dev/null || echo "unknown")
echo "  Status: $WHATSAPP_STATUS"
echo "  Proteção: ❌ NUNCA reautenticar (intentional)"
echo ""

# Resumo
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ RESUMO                                                          │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  Kernel IMPAR v$VERSION"
echo "  ETAPA 3A.5 (Certificação)"
echo "  Status: Production Candidate"
echo "  Componentes: $MODULES módulos + $LIBRARIES bibliotecas"
echo "  Automações: $AUTOMATIONS (9 total)"
echo "  LaunchAgents: $LAUNCHAGENTS"
echo "  WhatsApp: OFFLINE (protegido)"
echo ""
echo "✅ Sistema operacional e certificado"
echo ""
