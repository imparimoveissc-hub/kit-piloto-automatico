#!/bin/bash
# Biblioteca de Planejamento de Execução
# Fornece funções para gerar planos completos de automações

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
REGISTRY_FILE="${PROJECT_ROOT}/.impar/registry.json"
GRAPH_FILE="${PROJECT_ROOT}/.impar/graph.json"

load_automation_plan() {
    local automation="$1"

    jq ".automations[] | select(.name_canonical == \"$automation\")" "$REGISTRY_FILE"
}

build_plan_object() {
    local automation="$1"
    local data="$2"

    python3 << PYTHON
import json
import sys

data = json.loads('''$data''')

plan = {
    "canonical_name": data.get("name_canonical"),
    "objective": data.get("description", "N/A"),
    "entry_point": data.get("entry_point", "unknown"),
    "launchagents": data.get("launchagents", []),
    "dependencies": data.get("dependencies", []),
    "checkpoints": data.get("checkpoints", []),
    "risk_level": data.get("risk_level", "UNKNOWN"),
    "status": data.get("status", "unknown"),
    "cadence": data.get("cadence", "N/A"),
    "estimated_duration_minutes": estimate_duration(data.get("risk_level")),
    "confidence_level": "HIGH" if len(data.get("launchagents", [])) > 0 else "MEDIUM",
    "preconditions": identify_preconditions(data),
    "postconditions": identify_postconditions(data),
    "rollback_strategy": get_rollback_strategy(data),
    "verified_at": data.get("verified_at", "unknown")
}

print(json.dumps(plan, indent=2, ensure_ascii=False))

def estimate_duration(risk_level):
    duration_map = {
        "CRITICAL": 30,
        "HIGH": 20,
        "MEDIUM": 15,
        "LOW": 10
    }
    return duration_map.get(risk_level, 15)

def identify_preconditions(data):
    preconditions = ["Sistema operacional: macOS", "Kernel IMPAR v30 ativo"]
    if "launchagents" in data and len(data["launchagents"]) > 0:
        preconditions.append("LaunchAgents devem estar disponíveis")
    if "dependencies" in data and len(data["dependencies"]) > 0:
        preconditions.append("Dependências externas devem estar instaladas")
    if "checkpoints" in data and len(data["checkpoints"]) > 0:
        preconditions.append("Arquivos de checkpoint devem ser acessíveis")
    return preconditions

def identify_postconditions(data):
    postconditions = ["Executor recebe confirmação de conclusão", "Logs são gravados"]
    if data.get("status") == "active":
        postconditions.append("Automação retorna ao estado esperado")
    return postconditions

def get_rollback_strategy(data):
    name = data.get("name_canonical", "automacao")
    if "checkpoints" in data and len(data["checkpoints"]) > 0:
        return f"Restaurar checkpoints da automação {name} a partir de backup"
    return f"Parar todos os LaunchAgents de {name} e restaurar estado anterior"
PYTHON
}

estimate_duration() {
    local risk_level="$1"
    case "$risk_level" in
        CRITICAL) echo 30 ;;
        HIGH) echo 20 ;;
        MEDIUM) echo 15 ;;
        *) echo 10 ;;
    esac
}

get_known_risks() {
    local automation="$1"

    jq ".risks[] | select(.automation == \"$automation\")" "$GRAPH_FILE" 2>/dev/null || echo "[]"
}

get_rollback_strategy() {
    local automation="$1"

    echo "Estratégia de rollback para $automation:"
    echo "  1. Parar todos os LaunchAgents associados"
    echo "  2. Restaurar checkpoints do backup mais recente"
    echo "  3. Verificar integridade dos arquivos críticos"
    echo "  4. Reiniciar os LaunchAgents em modo seguro"
}

export -f load_automation_plan
export -f build_plan_object
export -f estimate_duration
export -f get_known_risks
export -f get_rollback_strategy
