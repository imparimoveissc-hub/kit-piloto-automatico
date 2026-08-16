#!/bin/bash
# Biblioteca de Executor Controlado (ETAPA 3A)
# Gerencia execução com aprovação, hash, expiração e auditoria

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB}"
AUDIT_LOG="${PROJECT_ROOT}/07_LOGS/EXECUTION_AUDIT.jsonl"
APPROVAL_DIR="${PROJECT_ROOT}/.impar/approvals"
WHITELIST="${PROJECT_ROOT}/.impar/executor_whitelist.json"

# Criar diretórios se não existirem
mkdir -p "$APPROVAL_DIR"
mkdir -p "$(dirname "$AUDIT_LOG")"

# Whitelist explícita (apenas impar-update-current-state em ETAPA 3A)
ensure_whitelist() {
    if [ ! -f "$WHITELIST" ]; then
        cat > "$WHITELIST" << 'EOF'
{
  "version": "1.0.0",
  "stage": "ETAPA 3A - Piloto",
  "authorized_services": [
    "impar-update-current-state"
  ],
  "notes": "Apenas impar-update-current-state autorizado. Outras automações retornarão erro."
}
EOF
    fi
}

# Verificar se serviço está na whitelist
is_whitelisted() {
    local service="$1"
    ensure_whitelist

    if jq -e ".authorized_services[] | select(. == \"$service\")" "$WHITELIST" >/dev/null 2>&1; then
        return 0  # Whitelisted
    else
        return 1  # Not whitelisted
    fi
}

# Gerar hash do plano
generate_plan_hash() {
    local plan_content="$1"
    echo "$plan_content" | shasum -a 256 | awk '{print $1}'
}

# Criar aprovação temporária com expiração
create_approval() {
    local hash="$1"
    local service="$2"
    local expiration_seconds=60

    local expires_at=$(($(date +%s) + expiration_seconds))
    local approval_file="${APPROVAL_DIR}/${hash}.approval"

    cat > "$approval_file" << EOF
{
  "hash": "$hash",
  "service": "$service",
  "created_at": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "expires_at": $expires_at,
  "used": false
}
EOF

    chmod 600 "$approval_file"
    echo "$approval_file"
}

# Validar aprovação
validate_approval() {
    local hash="$1"
    local service="$2"
    local approval_file="${APPROVAL_DIR}/${hash}.approval"

    # Arquivo existe?
    if [ ! -f "$approval_file" ]; then
        echo "❌ Aprovação não encontrada"
        return 1
    fi

    # Já foi usada?
    if jq -e '.used == true' "$approval_file" >/dev/null 2>&1; then
        echo "❌ Aprovação já foi usada"
        return 1
    fi

    # Expirou?
    local now=$(date +%s)
    local expires_at=$(jq -r '.expires_at' "$approval_file")
    if [ "$now" -gt "$expires_at" ]; then
        echo "❌ Aprovação expirou"
        rm -f "$approval_file"
        return 1
    fi

    # Serviço correto?
    local approved_service=$(jq -r '.service' "$approval_file")
    if [ "$approved_service" != "$service" ]; then
        echo "❌ Aprovação é para outro serviço"
        return 1
    fi

    echo "✅ Aprovação válida"
    return 0
}

# Marcar aprovação como usada
mark_approval_used() {
    local hash="$1"
    local approval_file="${APPROVAL_DIR}/${hash}.approval"

    if [ -f "$approval_file" ]; then
        jq '.used = true | .used_at = "'$(date -u +'%Y-%m-%dT%H:%M:%SZ')'"' "$approval_file" > "${approval_file}.tmp"
        mv "${approval_file}.tmp" "$approval_file"
    fi
}

# Log de auditoria (append-only)
audit_log() {
    local service="$1"
    local status="$2"
    local details="$3"

    cat >> "$AUDIT_LOG" << EOF
{"timestamp":"$(date -u +'%Y-%m-%dT%H:%M:%SZ')","service":"$service","status":"$status","details":$details}
EOF
}

# Exportar funções
export -f ensure_whitelist is_whitelisted generate_plan_hash create_approval validate_approval mark_approval_used audit_log
