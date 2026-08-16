#!/bin/bash
# Biblioteca de Validação (Leitura Apenas)
# Fornece funções para validar automações sem executá-las

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
REGISTRY_FILE="${PROJECT_ROOT}/.impar/registry.json"
GRAPH_FILE="${PROJECT_ROOT}/.impar/graph.json"

validate_file_existence() {
    local file_path="$1"
    local file_type="${2:-file}"

    if [ -e "$file_path" ]; then
        echo "✅ $file_type existe: $file_path"
        return 0
    else
        echo "❌ $file_type NÃO existe: $file_path"
        return 1
    fi
}

validate_json_integrity() {
    local json_file="$1"

    if [ ! -f "$json_file" ]; then
        echo "❌ Arquivo JSON não encontrado: $json_file"
        return 1
    fi

    if jq empty "$json_file" 2>/dev/null; then
        echo "✅ JSON válido: $json_file"
        return 0
    else
        echo "❌ JSON inválido: $json_file"
        return 1
    fi
}

validate_automation_exists() {
    local automation="$1"

    if jq -e ".automations[] | select(.name_canonical == \"${automation}\")" "$REGISTRY_FILE" >/dev/null 2>&1; then
        echo "✅ Automação existe: $automation"
        return 0
    else
        echo "❌ Automação NÃO encontrada: $automation"
        return 1
    fi
}

validate_launchagents() {
    local automation="$1"
    local la_dir="$HOME/Library/LaunchAgents"

    local las=$(jq -r ".automations[] | select(.name_canonical == \"${automation}\") | .launchagents[]" "$REGISTRY_FILE" 2>/dev/null || true)

    if [ -z "$las" ]; then
        echo "⚠️ Nenhum LaunchAgent encontrado para: $automation"
        return 0
    fi

    local found=0
    local total=0

    while IFS= read -r la; do
        [ -z "$la" ] && continue
        ((total++))
        if [ -f "$la_dir/$la.plist" ] || [ -f "$la_dir/$la" ]; then
            echo "✅ LaunchAgent encontrado: $la"
            ((found++))
        else
            echo "⚠️ LaunchAgent NÃO encontrado no sistema: $la"
        fi
    done <<<"$las"

    if [ "$total" -eq 0 ]; then
        echo "ℹ️ Nenhum LaunchAgent para validar"
        return 0
    fi

    if [ "$found" -eq "$total" ]; then
        return 0
    else
        return 1
    fi
}

validate_checkpoints() {
    local automation="$1"

    local checkpoints=$(jq -r ".automations[] | select(.name_canonical == \"${automation}\") | .checkpoints[]?" "$REGISTRY_FILE" 2>/dev/null || true)

    if [ -z "$checkpoints" ]; then
        echo "ℹ️ Nenhum checkpoint definido para: $automation"
        return 0
    fi

    local found=0
    local total=0

    while IFS= read -r checkpoint; do
        [ -z "$checkpoint" ] && continue
        ((total++))
        if [ -f "$checkpoint" ] || [ -d "$checkpoint" ]; then
            echo "✅ Checkpoint encontrado: $checkpoint"
            ((found++))
        else
            echo "⚠️ Checkpoint NÃO encontrado: $checkpoint"
        fi
    done <<<"$checkpoints"

    if [ "$total" -eq 0 ]; then
        return 0
    fi

    if [ "$found" -eq "$total" ]; then
        return 0
    else
        return 1
    fi
}

check_blocking_risks() {
    local automation="$1"

    local risks=$(jq -r ".risks[] | select(.automation == \"$automation\" and .severity == \"CRITICAL\") | .title" "$GRAPH_FILE" 2>/dev/null || true)

    if [ -z "$risks" ]; then
        echo "✅ Nenhum risco bloqueante encontrado"
        return 0
    fi

    echo "❌ Riscos CRÍTICOS detectados:"
    while IFS= read -r risk; do
        [ -z "$risk" ] && continue
        echo "   - $risk"
    done <<<"$risks"

    return 1
}

check_for_conflicts() {
    local automation="$1"

    echo "ℹ️ Verificando conflitos com outras automações..."

    local deps=$(jq -r ".automations[] | select(.name_canonical == \"${automation}\") | .dependencies[]?" "$REGISTRY_FILE" 2>/dev/null || true)

    if [ -z "$deps" ]; then
        echo "✅ Nenhuma dependência detectada"
        return 0
    fi

    echo "ℹ️ Dependências encontradas:"
    while IFS= read -r dep; do
        [ -z "$dep" ] && continue
        echo "   - $dep"
    done <<<"$deps"

    return 0
}

validate_registry_integrity() {
    echo "Validando integridade do registry..."

    if validate_json_integrity "$REGISTRY_FILE"; then
        echo "✅ Registry é válido"
        return 0
    else
        echo "❌ Registry tem problemas"
        return 1
    fi
}

validate_graph_integrity() {
    echo "Validando integridade do grafo operacional..."

    if validate_json_integrity "$GRAPH_FILE"; then
        echo "✅ Grafo é válido"
        return 0
    else
        echo "❌ Grafo tem problemas"
        return 1
    fi
}

export -f validate_file_existence
export -f validate_json_integrity
export -f validate_automation_exists
export -f validate_launchagents
export -f validate_checkpoints
export -f check_blocking_risks
export -f check_for_conflicts
export -f validate_registry_integrity
export -f validate_graph_integrity
