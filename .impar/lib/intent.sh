#!/bin/bash

# Library for intent routing in the impar kernel

set -euo pipefail

# Route question to appropriate module
# Returns: module_name automation_name
route_intent() {
  local question="${1:-}"
  question=$(echo "$question" | tr '[:upper:]' '[:lower:]')

  # Planning/Simulation keywords (ETAPA 2.95)
  if [[ "$question" =~ ^plan[[:space:]]|^validate[[:space:]]|^dry-run[[:space:]]|^simulate|^rehearse ]]; then
    local cmd=$(echo "$question" | awk '{print $1}')
    local automation=$(echo "$question" | awk '{$1=""; print $0}' | xargs)
    if [[ "$cmd" == "plan" ]]; then
      echo "plan $automation"
    elif [[ "$cmd" == "validate" ]]; then
      echo "validate $automation"
    elif [[ "$cmd" == "dry-run" || "$cmd" == "simulate" || "$cmd" == "rehearse" ]]; then
      echo "dry-run $automation"
    fi
    return 0
  fi

  # Marketplace keywords
  if [[ "$question" =~ marketplace|publicação|imóvel|grupo|facebook|venda|post ]]; then
    echo "marketplace impar-facebook-marketplace-posting"
    return 0
  fi

  # Messenger keywords
  if [[ "$question" =~ messenger|inbox|respond|d1|auto-respond ]]; then
    echo "messenger impar-messenger-bridge"
    return 0
  fi

  # WhatsApp keywords
  if [[ "$question" =~ whatsapp|bridge|d0|offline|online|reenableit|ativar ]]; then
    echo "whatsapp impar-whatsapp-bridge"
    return 0
  fi

  # NFS-e keywords
  if [[ "$question" =~ "nota fiscal"|nfse|nfs-e|fiscal|lote|avulsa|emissão ]]; then
    echo "nfse nfem-joinville"
    return 0
  fi

  # Leads keywords
  if [[ "$question" =~ leads|"chaves na mão"|lead|whatsapp|notif ]]; then
    echo "leads chaves-na-mao-lead-checker"
    return 0
  fi

  # CRM sync keywords
  if [[ "$question" =~ rogga|"grupo jm"|crm|sincroniz|sync|imobibrasil ]]; then
    echo "crm impar-atualizacao-rogga-imobibrasil"
    return 0
  fi

  # Memory/context keywords
  if [[ "$question" =~ memória|contexto|token|histórico|conhecimento ]]; then
    echo "memory"
    return 0
  fi

  # Health/error keywords
  if [[ "$question" =~ erro|falha|crash|problema|crítico|saúde|health|status ]]; then
    echo "health"
    return 0
  fi

  # General status
  if [[ "$question" =~ status|estado|como|ativid ]]; then
    echo "general"
    return 0
  fi

  # Not found
  echo "unknown"
  return 0
}

# Check if question requests execution
is_execution_request() {
  local question="${1:-}"
  question=$(echo "$question" | tr '[:upper:]' '[:lower:]')

  if [[ "$question" =~ --execute|--run|--start|--restart|--stop|--send|--publish|--login|--auth|--delete|--remove|executar|rodar|iniciar|parar|reiniciar|enviar|publicar|fazer|disparar|deletar|remover|ligar|ativar|reativar|autenticar ]]; then
    return 0  # True — is execution
  fi

  return 1  # False — not execution
}

# Check if question contains execution blockers and return blocker message
is_execution_blocked() {
  local question="${1:-}"
  question=$(echo "$question" | tr '[:upper:]' '[:lower:]')

  if is_execution_request "$question"; then
    return 0  # True — is blocked
  fi

  return 1  # False — not blocked
}

# Return execution blocker message
get_execution_blocker_message() {
  cat << 'EOF'

⛔ EXECUÇÃO BLOQUEADA

A execução real ainda não está habilitada.

ETAPA 2.95 (Execution Planner) fornece três comandos de simulação:

  • impar plan <automacao>
    Gera um plano completo descrevendo exatamente o que aconteceria

  • impar validate <automacao>
    Realiza validações de leitura apenas, sem executar

  • impar dry-run <automacao>
    Simula passo a passo toda a execução, sem executar nada

USE ESSES COMANDOS PARA:
  1. Entender exatamente o que cada automação faria
  2. Validar antes de executar
  3. Simular passo a passo
  4. Identificar bloqueios e riscos
  5. Preparar rollback

PRÓXIMA ETAPA:
  Quando ETAPA 3 for autorizada explicitamente, você terá acesso a:
  • impar execute <automacao>
  • impar run <automation>
  • ... (outros comandos de execução)

Aguardando sua autorização para ETAPA 3.

EOF
}

# Get automation info from registry
get_automation_info() {
  local name="${1:-}"
  local registry_path="/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/.impar/registry.json"

  if [[ ! -f "$registry_path" ]]; then
    echo ""
    return 1
  fi

  python3 << 'PYSCRIPT' 2>/dev/null || echo ""
import json
import sys

registry_path = "$registry_path"
name = "$name"

try:
  with open(registry_path) as f:
    data = json.load(f)
    for auto in data.get('automations', []):
      if auto['name_canonical'] == name or name in auto.get('aliases', []):
        print(json.dumps(auto))
        sys.exit(0)
except:
  pass
PYSCRIPT
}

export -f route_intent is_execution_request is_execution_blocked get_execution_blocker_message get_automation_info
