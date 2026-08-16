# Release Notes — Kernel IMPAR v3.0.0

**Versão:** 3.0.0  
**Stage:** ETAPA 3A.5 (Certificado)  
**Data de Release:** 2026-07-23  
**Status:** Production Candidate  

---

## Visão Geral

Kernel IMPAR v3.0.0 é a primeira versão **certificada** do sistema de automação operacional para Impar Imóveis. Combina:

- **Conhecimento estruturado** (grafo operacional)
- **Planejamento seguro** (dry-run + simulação)
- **Execução controlada** (aprovação + auditoria)
- **Certificação** (hashes + versionamento)

---

## Arquitetura

### Camadas

```
┌─────────────────────────────────────────┐
│  User Interface                         │
│  (CLI: impar <comando> <args>)          │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Intent Router & Security               │
│  (Routing + Execution Blockers)         │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Knowledge Layer                        │
│  (Registry + Graph + Services)          │
└─────────────┬───────────────────────────┘
              │
      ┌───────┴────────┬─────────────┐
      │                │             │
┌─────▼──────┐ ┌──────▼──────┐ ┌───▼────────┐
│   Planning │ │  Validation │ │  Execution │
│  (Planner) │ │ (Validator) │ │ (Executor) │
└────────────┘ └─────────────┘ └────────────┘
              │
┌─────────────▼───────────────────────────┐
│  Auditoria & Rollback                   │
│  (EXECUTION_AUDIT.jsonl + Backups)      │
└─────────────────────────────────────────┘
```

### Componentes Principais

**Kernel Inteligente (22 módulos)**
- ask.sh — Perguntas em linguagem natural
- search.sh — Busca full-text
- explain.sh — Explicação de componentes
- suggest.sh — Recomendações
- ... (18 outros módulos de análise, execução, etc.)

**Grafo Operacional (7 JSON)**
- automations.json — 9 automações
- launchagents.json — 17 agentes
- topology.json — Hierarquia
- dependencies.json — 10 relações
- critical-files.json — 10 arquivos críticos
- risks.json — 10 riscos
- sources.json — 9 fontes de dados

**Bibliotecas de Suporte (10 arquivos)**
- intent.sh — Routing determinístico
- query.sh — Lookup de dados
- format.sh — Formatação
- planner.sh — Planejamento
- validator.sh — Validação (leitura)
- simulator.sh — Simulação
- executor.sh — Execução controlada
- ... (3 others)

---

## Fluxo de Operação

### Cenário: Executar impar-update-current-state

```
1. PLANEJAMENTO (impar plan-execution)
   ├─ Validar whitelist
   ├─ Gerar hash SHA-256
   └─ Output: Plano + Hash

2. APROVAÇÃO (impar approve <hash>)
   ├─ Verificar plano
   ├─ Criar token temporário (60s, 1 uso)
   └─ Output: Token

3. EXECUÇÃO (impar execute <service> --approval <token>)
   ├─ Validar 6 critérios
   ├─ Criar backup
   ├─ Executar serviço
   ├─ Registrar auditoria
   └─ Output: Resultado + Exit Code

4. AUDITORIA (cat 07_LOGS/EXECUTION_AUDIT.jsonl)
   ├─ Timestamp
   ├─ Serviço
   ├─ Status
   └─ Detalhes (exit_code, duration)

5. ROLLBACK (impar rollback-last <service>) [Opcional]
   ├─ Mostrar preview
   ├─ Pedir confirmação
   └─ Restaurar backup
```

---

## Segurança

### Bloqueios Implementados

**Whitelist Explícita:**
- ✅ Apenas `impar-update-current-state` autorizado em ETAPA 3A
- ✅ Todas as demais automações retornam erro

**Fail-Closed:**
- ❌ Hash inválido? BLOQUEADO
- ❌ Aprovação expirada? BLOQUEADO
- ❌ Arquivo não existe? BLOQUEADO
- ❌ Validação falhar? BLOQUEADO

**Auditoria Imutável:**
- ✅ EXECUTION_AUDIT.jsonl (append-only)
- ✅ Cada execução registrada com timestamp
- ✅ Sem credenciais, sem senhas

**Proteções do WhatsApp:**
- ✅ Status: offline
- ✅ disabled_intentionally = true
- ✅ must_not_reauthenticate = true
- ✅ requires_explicit_authorization = true

---

## Whitelist (ETAPA 3A)

```json
{
  "authorized_services": [
    "impar-update-current-state"
  ],
  "stage": "ETAPA 3A - Piloto"
}
```

---

## Auditoria

### Formato EXECUTION_AUDIT.jsonl

```json
{
  "timestamp": "2026-07-23T02:42:28Z",
  "service": "impar-update-current-state",
  "status": "EXECUTED",
  "details": {
    "exit_code": 0,
    "duration": 1
  }
}
```

**Propriedades:**
- Append-only (não pode ser deletado)
- Uma linha por execução
- Timestamps UTC
- Sem dados sensíveis

---

## Rollback

### Automático
- Backup criado antes de cada execução
- Localização: `.impar/backups/<timestamp>/`
- Estrutura: Cópia exata dos arquivos

### Manual
```bash
impar rollback-last <service>
```

**Processo:**
1. Encontra último backup
2. Mostra preview
3. Pede confirmação explícita
4. Restaura arquivos

**Segurança:**
- Não toca em LaunchAgents
- Não toca em .plist
- Não toca em automações
- Não toca em credenciais

---

## Planejamento (Execution Planner)

### impar plan <automacao>

Simula a execução com 16 campos:

- canonical_name
- objective
- entry_point
- launchagents[]
- dependencies[]
- checkpoints[]
- risk_level
- status
- estimated_duration_minutes
- confidence_level
- preconditions[]
- postconditions[]
- rollback_strategy
- known_risks[]
- sources_used[]
- verified_at

**Exemplo:**
```
Automação: impar-update-current-state
Objetivo: Atualizar CURRENT_STATE.md
Entry Point: /Users/usuario/.local/impar-automation/update-current-state.py
LaunchAgents: 0
Dependências: 3
Riscos: BAIXO
Duração: 5-10s
```

---

## Validação (Execution Planner)

### impar validate <automacao>

Realiza 7 verificações de leitura:

1. ✅ Existência da automação
2. ✅ Integridade JSON (registry + grafo)
3. ✅ Existência de LaunchAgents
4. ✅ Existência de checkpoints
5. ✅ Conflitos com outras automações
6. ✅ Riscos bloqueantes
7. ✅ Resumo de validação

---

## Simulação (Execution Planner)

### impar dry-run <automacao>

Simula passo a passo com:

- PASSO N: Descrição
- AÇÃO: O que faria
- ARQUIVOS LIDOS: Lista
- ARQUIVOS MODIFICADOS: Lista
- RISCO: CRÍTICO/ALTO/MÉDIO/BAIXO
- ROLLBACK: Como desfazer
- STATUS: ✓ SIMULADO

**Exemplo para impar-update-current-state:**
```
PASSO 1: Ler checkpoint.json
PASSO 2: Ler task-ledger.md
PASSO 3: Validar dados
PASSO 4: Atualizar CURRENT_STATE.md
PASSO 5: Registrar sucesso
```

---

## Limitações Conhecidas

**ETAPA 3A (Produção Controlada):**
- ❌ Apenas 1 serviço autorizado (impar-update-current-state)
- ❌ Sem execução de Marketplace
- ❌ Sem execução de Messenger
- ❌ Sem execução de Leads
- ❌ Sem execução de NFS-e
- ❌ Sem execução de LaunchAgents diretos
- ❌ Sem modificação de .plist

**Planejado para futuras versões:**
- ✅ Marketplace (ETAPA 3B)
- ✅ Messenger (ETAPA 3C)
- ✅ Leads (ETAPA 3D)
- ✅ NFS-e (ETAPA 3E)
- ✅ LaunchAgent management (ETAPA 4+)

---

## Próximos Passos

### ETAPA 3B (Marketplace Pilot)
- Adicionar impar-facebook-marketplace-posting à whitelist
- Testes com Playwright bloqueado
- Simulação de cadência

### ETAPA 3C (Messenger Pilot)
- Adicionar impar-messenger-bridge à whitelist
- Testes com AppleScript

### ETAPA 3D (Leads Pilot)
- Adicionar chaves-na-mao-lead-checker à whitelist
- Testes com WhatsApp Desktop

### ETAPA 3E (NFS-e Pilot)
- Adicionar nfem-joinville à whitelist
- Integração com Portal Nacional

### ETAPA 4.0 (Full Production)
- Todas as automações ativas
- Multi-team suporte
- SLAs de execução

---

## Dicas de Uso

### Gerar Plano
```bash
impar plan impar-update-current-state
```

### Validar
```bash
impar validate impar-update-current-state
```

### Simular
```bash
impar dry-run impar-update-current-state
```

### Ver Status
```bash
impar status
```

### Certificar
```bash
impar certify
```

### Ver Auditoria
```bash
tail -f 07_LOGS/EXECUTION_AUDIT.jsonl
```

---

## Suporte

Para reportar problemas ou sugestões:

1. Verifique a certificação: `impar certify`
2. Verifique o status: `impar status`
3. Verifique os logs: `tail -f 07_LOGS/EXECUTION_AUDIT.jsonl`
4. Consulte a documentação: `.impar/knowledge/`

---

## Licença & Propriedade

Kernel IMPAR — Impar Imóveis  
Propriedade: Impar Imóveis  
Uso: Automação operacional interna  
Status: Production Candidate (v3.0.0)

---

**Versão:** 3.0.0  
**Data:** 2026-07-23  
**Status:** ✅ Certificado
