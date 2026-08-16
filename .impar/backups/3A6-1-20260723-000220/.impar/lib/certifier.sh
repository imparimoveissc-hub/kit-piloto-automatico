#!/bin/bash
# Biblioteca de Certificação do Kernel IMPAR
# Calcula hashes, detecta inconsistências, valida arquivos

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
IMPAR_DIR="${PROJECT_ROOT}/.impar"
CERTS_DIR="${IMPAR_DIR}/certificates"

mkdir -p "$CERTS_DIR"

# Calcular hash SHA-256 de arquivo
file_hash() {
    local file="$1"
    if [ -f "$file" ]; then
        shasum -a 256 "$file" | awk '{print $1}'
    else
        echo "FILE_NOT_FOUND"
    fi
}

# Validar JSON
validate_json() {
    local file="$1"
    if [ ! -f "$file" ]; then
        return 1  # Not valid (file doesn't exist)
    fi

    if jq empty "$file" 2>/dev/null; then
        return 0  # Valid
    else
        return 1  # Invalid
    fi
}

# Contar arquivos
count_files() {
    local pattern="$1"
    find "$IMPAR_DIR" $pattern -type f 2>/dev/null | wc -l | tr -d ' '
}

# Contar linhas em arquivo
count_lines() {
    local file="$1"
    if [ -f "$file" ]; then
        wc -l < "$file" | tr -d ' '
    else
        echo "0"
    fi
}

# Gerar certificado
generate_certificate() {
    local timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    local filename=$(date +'%Y%m%d-%H%M%S')
    local cert_file="${CERTS_DIR}/kernel-cert-${filename}.json"

    # Calcular hashes
    local registry_hash=$(file_hash "${IMPAR_DIR}/registry.json")
    local graph_hash=$(file_hash "${IMPAR_DIR}/graph.json")
    local whitelist_hash=$(file_hash "${IMPAR_DIR}/executor_whitelist.json")
    local version_hash=$(file_hash "${IMPAR_DIR}/VERSION")

    # Contar componentes
    local modules=$(count_files "-name '*.sh' -path '${IMPAR_DIR}/modules/*'")
    local libraries=$(count_files "-name '*.sh' -path '${IMPAR_DIR}/lib/*'")
    local automations=$(jq '.automations | length' "${IMPAR_DIR}/registry.json" 2>/dev/null || echo "0")
    local launchagents=$(jq '.[] | .launchagents | length' "${IMPAR_DIR}/knowledge/launchagents.json" 2>/dev/null | paste -sd+ | bc || echo "0")
    local tests=$(count_files "-name '*.sh' -path '${IMPAR_DIR}/tests/*'")

    # Criar JSON de certificado
    cat > "$cert_file" << EOF
{
  "version": "3.0.0",
  "stage": "ETAPA 3A.5",
  "status": "Certified Candidate",
  "timestamp": "$timestamp",
  "kernel": {
    "version_hash": "$version_hash",
    "registry_hash": "$registry_hash",
    "graph_hash": "$graph_hash",
    "whitelist_hash": "$whitelist_hash"
  },
  "components": {
    "modules": $modules,
    "libraries": $libraries,
    "automations": $automations,
    "launchagents": $launchagents,
    "tests": $tests,
    "knowledge_files": 7
  },
  "files_verified": {
    "registry.json": "$(validate_json "${IMPAR_DIR}/registry.json" && echo 'valid' || echo 'invalid')",
    "graph.json": "$(validate_json "${IMPAR_DIR}/graph.json" && echo 'valid' || echo 'invalid')",
    "VERSION": "$([ -f "${IMPAR_DIR}/VERSION" ] && echo 'present' || echo 'missing')",
    "CHANGELOG.md": "$([ -f "${IMPAR_DIR}/CHANGELOG.md" ] && echo 'present' || echo 'missing')",
    "RELEASE_NOTES.md": "$([ -f "${IMPAR_DIR}/RELEASE_NOTES.md" ] && echo 'present' || echo 'missing')"
  },
  "certificate_file": "$cert_file"
}
EOF

    echo "$cert_file"
}

# Validar integridade
validate_integrity() {
    local issues=0

    # Verificar arquivos críticos
    local critical_files=(
        "${IMPAR_DIR}/registry.json"
        "${IMPAR_DIR}/graph.json"
        "${IMPAR_DIR}/VERSION"
        "${IMPAR_DIR}/CHANGELOG.md"
        "${IMPAR_DIR}/RELEASE_NOTES.md"
        "${IMPAR_DIR}/executor_whitelist.json"
    )

    echo "▶ Verificando arquivos críticos..."
    for file in "${critical_files[@]}"; do
        if [ -f "$file" ]; then
            echo "  ✅ $(basename $file)"
        else
            echo "  ❌ $(basename $file) — AUSENTE"
            ((issues++))
        fi
    done

    # Validar JSON
    echo ""
    echo "▶ Validando JSON..."
    for json_file in "${IMPAR_DIR}/registry.json" "${IMPAR_DIR}/graph.json" "${IMPAR_DIR}/executor_whitelist.json"; do
        if validate_json "$json_file"; then
            echo "  ✅ $(basename $json_file) — válido"
        else
            echo "  ❌ $(basename $json_file) — INVÁLIDO"
            ((issues++))
        fi
    done

    # Verificar conhecimento
    echo ""
    echo "▶ Verificando arquivos de conhecimento..."
    local knowledge_files=(
        "automations.json"
        "launchagents.json"
        "topology.json"
        "dependencies.json"
        "critical-files.json"
        "risks.json"
        "sources.json"
    )

    for kfile in "${knowledge_files[@]}"; do
        local path="${IMPAR_DIR}/knowledge/${kfile}"
        if validate_json "$path"; then
            echo "  ✅ $kfile — válido"
        else
            echo "  ❌ $kfile — INVÁLIDO"
            ((issues++))
        fi
    done

    # Verificar módulos
    echo ""
    echo "▶ Verificando módulos..."
    local modules_found=$(count_files "-name '*.sh' -path '${IMPAR_DIR}/modules/*'")
    echo "  ✅ $modules_found módulos encontrados"

    # Verificar bibliotecas
    echo ""
    echo "▶ Verificando bibliotecas..."
    local libraries_found=$(count_files "-name '*.sh' -path '${IMPAR_DIR}/lib/*'")
    echo "  ✅ $libraries_found bibliotecas encontradas"

    # Verificar testes
    echo ""
    echo "▶ Verificando testes..."
    local tests_found=$(count_files "-name '*.sh' -path '${IMPAR_DIR}/tests/*'")
    echo "  ✅ $tests_found testes encontrados"

    return $issues
}

# Exporter funções
export -f file_hash validate_json count_files count_lines generate_certificate validate_integrity
