# Changelog — Kernel IMPAR

Todas as mudanças notáveis neste projeto são documentadas neste arquivo.

---

## [3.0.0] — 2026-07-23

### ETAPA 3A.5: Certificação e Versionamento
- ✅ Criado comando `impar certify`
- ✅ Implementado sistema de certificação (hashes SHA-256)
- ✅ Criado versionamento (VERSION, CHANGELOG, RELEASE_NOTES)
- ✅ Gerado certificado de build
- ✅ Expandido comando `impar status`
- ✅ Certificado kernel como Production Candidate

### ETAPA 3A: Executor Controlado em Piloto
- ✅ Implementado executor com aprovação temporária (60s, 1 uso)
- ✅ Criado sistema de whitelist explícita
- ✅ Auditoria imutável (EXECUTION_AUDIT.jsonl)
- ✅ Bloqueios confirmados para 9 automações
- ✅ Backup automático + rollback manual
- ✅ Teste piloto bem-sucedido de impar-update-current-state

**Módulos adicionados:**
- `.impar/modules/plan-execution.sh`
- `.impar/modules/approve.sh`
- `.impar/modules/execute.sh`
- `.impar/modules/rollback-last.sh`

**Bibliotecas adicionadas:**
- `.impar/lib/executor.sh`

---

## [2.95.0] — 2026-07-22

### ETAPA 2.95: Execution Planner
- ✅ Implementado comando `impar plan` (plano completo com 16 campos)
- ✅ Implementado comando `impar validate` (7 validações de leitura)
- ✅ Implementado comando `impar dry-run` (simulação passo a passo)
- ✅ Criadas 3 bibliotecas de simulação
- ✅ 100% simulação, zero execução
- ✅ Testes: 6/6 passaram

**Módulos adicionados:**
- `.impar/modules/plan.sh`
- `.impar/modules/validate.sh`
- `.impar/modules/dry-run.sh`

**Bibliotecas adicionadas:**
- `.impar/lib/planner.sh`
- `.impar/lib/validator.sh`
- `.impar/lib/simulator.sh`

---

## [2.9.1] — 2026-07-22

### ETAPA 2.9.1: Correção de Inconsistências do Grafo
- ✅ Corrigidas 6 discrepâncias críticas
- ✅ Adicionada automação ausente (impar-notificar-leads)
- ✅ Corrigidas contagens de LaunchAgents (8 → 17)
- ✅ Corrigidas contagens de dependências (45 fictício → 31 real)
- ✅ Testes: 10/10 passaram
- ✅ Backup criado (`/private/tmp/impar-graph-correction-backup-1784773020/`)
- ✅ Rollback documentado

**Arquivos corrigidos:**
- `.impar/knowledge/automations.json`
- `.impar/knowledge/launchagents.json`
- `.impar/knowledge/topology.json`
- `.impar/graph.json`

---

## [2.9.0] — 2026-07-22

### ETAPA 2.9: Auditoria de Consistência do Grafo
- ✅ Auditoria rigorosa: registry.json vs. knowledge files
- ✅ Identificadas 6 discrepâncias críticas
- ✅ Discrepâncias documentadas (AUDITORIA_CONSISTENCIA_GRAFO_V1.md)
- ✅ Nenhuma correção automática (aguardou autorização)
- ✅ Teste anterior: 6/10 falharam, pós-correção: 10/10 passaram

---

## [2.8.0] — 2026-07-21

### ETAPA 2.8: Grafo Operacional do Kernel
- ✅ Criadas 7 knowledge files (JSON estruturado)
- ✅ Implementados 6 comandos de análise (graph, deps, impact, critical, topology, relations)
- ✅ Integração com kernel inteligente
- ✅ Source attribution em todas as respostas

**Arquivos criados:**
- `.impar/knowledge/automations.json` (9 nós)
- `.impar/knowledge/launchagents.json` (17 agentes)
- `.impar/knowledge/topology.json` (hierarquia)
- `.impar/knowledge/dependencies.json` (10 relações)
- `.impar/knowledge/critical-files.json` (10 arquivos)
- `.impar/knowledge/risks.json` (10 riscos)
- `.impar/knowledge/sources.json` (9 fontes)

**Módulos adicionados:**
- `.impar/modules/graph.sh`
- `.impar/modules/deps.sh`
- `.impar/modules/impact.sh`
- `.impar/modules/critical.sh`
- `.impar/modules/topology.sh`
- `.impar/modules/relations.sh`

---

## [2.5.0] — 2026-07-21

### ETAPA 2.5: Kernel Inteligente
- ✅ Implementados 4 comandos de query (ask, search, explain, suggest)
- ✅ Deterministic keyword-based routing (sem ML, sem APIs)
- ✅ Bloqueios de execução (--execute, --run, --start, etc.)
- ✅ WhatsApp offline protection integrada

**Módulos criados:**
- `.impar/modules/ask.sh`
- `.impar/modules/search.sh`
- `.impar/modules/explain.sh`
- `.impar/modules/suggest.sh`

**Bibliotecas criadas:**
- `.impar/lib/intent.sh` (routing)
- `.impar/lib/query.sh` (data lookup)
- `.impar/lib/format.sh` (formatting)
- `.impar/lib/common.sh` (utilities)

---

## [1.0.0] — 2026-07-20

### Estrutura Base
- ✅ Criado diretório `.impar/`
- ✅ Criado registry.json (9 automações)
- ✅ Criado graph.json (índice central)
- ✅ Criados diretórios: modules/, lib/, knowledge/, tests/
- ✅ Criado ~/.local/bin/impar (CLI wrapper)

---

## Release Timeline

| Versão | Etapa | Data | Status |
|--------|-------|------|--------|
| 1.0.0 | Base | 2026-07-20 | ✅ Concluído |
| 2.5.0 | Kernel Inteligente | 2026-07-21 | ✅ Concluído |
| 2.8.0 | Grafo Operacional | 2026-07-21 | ✅ Concluído |
| 2.9.0 | Auditoria | 2026-07-22 | ✅ Concluído |
| 2.9.1 | Correção | 2026-07-22 | ✅ Concluído |
| 2.95.0 | Execution Planner | 2026-07-22 | ✅ Concluído |
| 3.0.0 | Executor + Certif. | 2026-07-23 | ✅ Concluído |

---

## Próximas Versões

### [3.1.0] — ETAPA 3B (Pending Authorization)
- Marketplace Pilot
- Playwright integration
- Cadência automation

### [3.2.0] — ETAPA 3C (Pending Authorization)
- Messenger Pilot
- AppleScript automation

### [3.3.0] — ETAPA 3D (Pending Authorization)
- Leads Pilot
- WhatsApp Desktop integration

### [3.4.0] — ETAPA 3E (Pending Authorization)
- NFS-e Integration
- Portal Nacional

### [4.0.0] — Full Production Release
- All automations active
- Full auditability
- Multi-team support
