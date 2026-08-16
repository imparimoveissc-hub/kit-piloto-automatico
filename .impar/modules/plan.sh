#!/bin/bash
# Módulo: plan — Gerar plano completo de automação
# Uso: impar plan <automacao>

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
LIB_DIR="$(dirname "$0")/../lib"

# Source libraries
source "${LIB_DIR}/common.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/common.sh"
source "${LIB_DIR}/format.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/format.sh"
source "${LIB_DIR}/planner.sh" 2>/dev/null || source "${PROJECT_ROOT}/.impar/lib/planner.sh"

AUTOMATION="${1:-}"

if [ -z "$AUTOMATION" ]; then
    echo "Erro: Especifique uma automação"
    echo "Uso: impar plan <automacao>"
    exit 1
fi

echo ""
format_header "PLANO DE EXECUÇÃO (SIMULADO)"
echo "Automação: $AUTOMATION"
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Carregar dados do registry
REGISTRY_FILE="${PROJECT_ROOT}/.impar/registry.json"
AUTOMATION_DATA=$(jq -r ".automations[] | select(.name_canonical == \"${AUTOMATION}\")" "$REGISTRY_FILE" 2>/dev/null || echo "")

if [ -z "$AUTOMATION_DATA" ]; then
    echo "❌ Automação não encontrada: $AUTOMATION"
    exit 1
fi

# Extrair campos principais
CANONICAL_NAME=$(echo "$AUTOMATION_DATA" | jq -r '.name_canonical // "N/A"')
OBJECTIVE=$(echo "$AUTOMATION_DATA" | jq -r '.description // "N/A"' | head -c 100)
ENTRY_POINT=$(echo "$AUTOMATION_DATA" | jq -r '.entry_point // "unknown"')
RISK_LEVEL=$(echo "$AUTOMATION_DATA" | jq -r '.risk_level // "UNKNOWN"')
STATUS=$(echo "$AUTOMATION_DATA" | jq -r '.status // "unknown"')

echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ INFORMAÇÕES GERAIS                                              │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  Nome:                 $CANONICAL_NAME"
echo "  Status:               $STATUS"
echo "  Nível de Risco:       $RISK_LEVEL"
echo "  Objetivo:             $OBJECTIVE"
echo "  Entry Point:          $ENTRY_POINT"
echo ""

# LaunchAgents
LAUNCHAGENTS=$(echo "$AUTOMATION_DATA" | jq -r '.launchagents[]?' 2>/dev/null || echo "")
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ LAUNCHAGENTS                                                    │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
if [ -z "$LAUNCHAGENTS" ]; then
    echo "  Nenhum LaunchAgent"
else
    while IFS= read -r la; do
        [ -z "$la" ] && continue
        echo "  • $la"
    done <<<"$LAUNCHAGENTS"
fi
echo ""

# Dependências
DEPENDENCIES=$(echo "$AUTOMATION_DATA" | jq -r '.dependencies[]?' 2>/dev/null || echo "")
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ DEPENDÊNCIAS                                                    │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
if [ -z "$DEPENDENCIES" ]; then
    echo "  Nenhuma dependência"
else
    while IFS= read -r dep; do
        [ -z "$dep" ] && continue
        echo "  • $dep"
    done <<<"$DEPENDENCIES"
fi
echo ""

# Checkpoints
CHECKPOINTS=$(echo "$AUTOMATION_DATA" | jq -r '.checkpoints[]?' 2>/dev/null || echo "")
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ CHECKPOINTS                                                     │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
if [ -z "$CHECKPOINTS" ]; then
    echo "  Nenhum checkpoint"
else
    while IFS= read -r cp; do
        [ -z "$cp" ] && continue
        echo "  • $cp"
    done <<<"$CHECKPOINTS"
fi
echo ""

# Riscos
GRAPH_FILE="${PROJECT_ROOT}/.impar/graph.json"
RISKS=$(jq -r ".risks[] | select(.automation == \"$CANONICAL_NAME\") | .title" "$GRAPH_FILE" 2>/dev/null || echo "")
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ RISCOS CONHECIDOS                                               │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
if [ -z "$RISKS" ]; then
    echo "  Nenhum risco catalogado"
else
    while IFS= read -r risk; do
        [ -z "$risk" ] && continue
        echo "  • $risk"
    done <<<"$RISKS"
fi
echo ""

# Estimativa
case "$RISK_LEVEL" in
    CRITICAL) DURATION=30 ;;
    HIGH) DURATION=20 ;;
    MEDIUM) DURATION=15 ;;
    *) DURATION=10 ;;
esac

echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ ESTIMATIVAS                                                     │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  Duração estimada:      ~$DURATION minutos"
echo "  Nível de confiança:    $([ -n "$LAUNCHAGENTS" ] && echo "ALTO" || echo "MÉDIO")"
echo "  Fontes utilizadas:     registry.json, graph.json"
echo ""

# Pré e Pós condições
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ PRÉ-CONDIÇÕES                                                   │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  • Sistema operacional: macOS"
echo "  • Kernel IMPAR v30 ativo"
echo "  • LaunchAgents devem estar disponíveis"
echo ""

echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ PÓS-CONDIÇÕES                                                   │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  • Executor recebe confirmação de conclusão"
echo "  • Logs são gravados em 07_LOGS/"
echo "  • Estado retorna ao esperado"
echo ""

# Rollback
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│ ESTRATÉGIA DE ROLLBACK                                          │"
echo "└─────────────────────────────────────────────────────────────────┘"
echo ""
echo "  1. Parar todos os LaunchAgents associados"
echo "  2. Restaurar checkpoints do backup mais recente"
echo "  3. Verificar integridade dos arquivos críticos"
echo "  4. Reiniciar os LaunchAgents em modo seguro"
echo ""

echo "✅ Plano de execução gerado com sucesso (SIMULADO)"
echo "   Execute 'impar validate $CANONICAL_NAME' para validar"
echo "   Execute 'impar dry-run $CANONICAL_NAME' para simular passo a passo"
echo ""
