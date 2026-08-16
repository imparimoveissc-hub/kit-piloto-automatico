# Knowledge Files — Upload no Project

> Lista priorizada de arquivos do kit pra upload no Project do Claude Desktop. Limite tipico: 20 arquivos / 30MB.

## Project 1: CoS V30 (geral)

### Tier 1 — Obrigatorios (10 arquivos)

| # | Arquivo | Por que |
|---|---|---|
| 1 | `00_INDEX.md` | Indice mestre |
| 2 | `00_OS/cos.md` | Definicao do CoS |
| 3 | `00_OS/router.md` | Roteamento |
| 4 | `00_OS/gates.md` | Gates de qualidade |
| 5 | `00_OS/access-preflight.md` | Preflight de acessos |
| 6 | `00_OS/proactivity-policy.md` | Politica full-auto |
| 7 | `15_PRODUCT_RELEASE/CLAUDE.md` | CoS publico V30 |
| 8 | `15_PRODUCT_RELEASE/nichos/family-classifier.md` | 8 familias operacionais |
| 9 | `15_PRODUCT_RELEASE/nichos/setup-nicho-playbook.md` | Setup adaptativo |
| 10 | `13_ADAPTIVE_SQUADS/README.md` | Squads adaptativos |

### Tier 2 — Recomendados (8 arquivos)

| # | Arquivo | Por que |
|---|---|---|
| 11 | `02_AGENTS/README.md` | Mapa de agentes |
| 12 | `04_DIRETRIZES/copy-goat-lite.md` | Copy framework |
| 13 | `04_DIRETRIZES/voz-ptbr.md` | Voz humana |
| 14 | `04_DIRETRIZES/pesquisa-voc.md` | VOC |
| 15 | `20_MCP_SETUP/README.md` | MCPs disponiveis |
| 16 | `20_MCP_SETUP/recommended-stack.md` | Stack por uso |
| 17 | `21_BUILDER_KIT/README.md` | Forge agent |
| 18 | `15_PRODUCT_RELEASE/PRIMEIRA_TAREFA.md` | Primeira entrega |

### Tier 3 — Opcionais (use os que sobrarem)

| Arquivo | Quando |
|---|---|
| `15_PRODUCT_RELEASE/.claude/agents/briefing-agent.md` | Briefing |
| `15_PRODUCT_RELEASE/.claude/agents/criacao-agent.md` | Criacao |
| `15_PRODUCT_RELEASE/exemplos/familias/agencia-servico-digital.md` | Se for agencia |
| `15_PRODUCT_RELEASE/exemplos/familias/clinica-saude.md` | Se for clinica |
| (escolher a familia certa do mentorado) | |

## Project 2: Trafego DR

### Tier 1 — Obrigatorios

| # | Arquivo |
|---|---|
| 1 | `11_TRAFFIC_STACK/README.md` |
| 2 | `11_TRAFFIC_STACK/PLAYBOOK.html` (export pra md se possivel) |
| 3 | `11_TRAFFIC_STACK/skills/direct-response-br/SKILL.md` |
| 4 | `11_TRAFFIC_STACK/agents/traffic-orchestrator.md` |
| 5 | `11_TRAFFIC_STACK/agents/meta-dr-specialist.md` |
| 6 | `11_TRAFFIC_STACK/agents/creative-analyst.md` |
| 7 | `11_TRAFFIC_STACK/agents/funnel-analyst.md` |
| 8 | `11_TRAFFIC_STACK/agents/attribution-auditor.md` |
| 9 | `11_TRAFFIC_STACK/agents/traffic-diagnostician.md` |
| 10 | `11_TRAFFIC_STACK/agents/scaling-strategist.md` |
| 11 | `11_TRAFFIC_STACK/agents/competitor-spy.md` |
| 12 | `04_DIRETRIZES/traffic-diretrizes.md` |

### Tier 2

| Arquivo |
|---|
| `11_TRAFFIC_STACK/tasks/diagnosticar-campanha-meta-cli.md` |
| `00_OS/gates.md` (GATE-TRAFFIC) |

## Project 3: WhatsApp + Cowork

### Tier 1 — Obrigatorios

| # | Arquivo |
|---|---|
| 1 | `12_WHATSAPP_STACK/README.md` |
| 2 | `12_WHATSAPP_STACK/agents/whatsapp-orchestrator.md` |
| 3 | `12_WHATSAPP_STACK/agents/prospecting-bot.md` |
| 4 | `12_WHATSAPP_STACK/agents/sdr-attendant.md` |
| 5 | `12_WHATSAPP_STACK/agents/customer-success-bot.md` |
| 6 | `12_WHATSAPP_STACK/agents/sales-followup-bot.md` |
| 7 | `12_WHATSAPP_STACK/agents/cowork-automation-architect.md` |
| 8 | `12_WHATSAPP_STACK/agents/conversation-qa.md` |
| 9 | `04_DIRETRIZES/whatsapp-diretrizes.md` |
| 10 | `12_WHATSAPP_STACK/skills/whatsapp-conversation-design/SKILL.md` |

### Tier 2

| Arquivo |
|---|
| `12_WHATSAPP_STACK/templates/conversation-map.md` |
| `12_WHATSAPP_STACK/templates/cowork-agent-spec.yaml` |
| `12_WHATSAPP_STACK/templates/handoff-schema.md` |
| `15_PRODUCT_RELEASE/whatsapp/fluxos/prospeccao.md` |
| `15_PRODUCT_RELEASE/whatsapp/fluxos/sdr-atendimento.md` |
| `15_PRODUCT_RELEASE/cowork/agent-spec.yaml` |
| `15_PRODUCT_RELEASE/cowork/test-checklist.md` |
| `00_OS/gates.md` (GATE-WHATSAPP) |

## Project 4 (opcional): Automacoes

### Tier 1

| Arquivo |
|---|
| `18_AUTOMATION_STACK/README.md` |
| `18_AUTOMATION_STACK/agents/automation-orchestrator.md` |
| `18_AUTOMATION_STACK/tasks/build-process-automation.md` |
| `18_AUTOMATION_STACK/templates/automation-blueprint.yaml` |
| `18_AUTOMATION_STACK/templates/sop-template.md` |
| `04_DIRETRIZES/automation-diretrizes.md` |
| `15_PRODUCT_RELEASE/exemplos/automacao-onboarding-cliente.md` |

## Project 5 (opcional): Builder (pra quem quer expandir kit)

### Tier 1

| Arquivo |
|---|
| `21_BUILDER_KIT/README.md` |
| `21_BUILDER_KIT/agents/forge.md` |
| `21_BUILDER_KIT/conventions.md` |
| `21_BUILDER_KIT/scaffolds/agent-scaffold.md` |
| `21_BUILDER_KIT/scaffolds/skill-scaffold.md` |
| `21_BUILDER_KIT/scaffolds/task-scaffold.md` |
| `21_BUILDER_KIT/scaffolds/diretriz-scaffold.md` |
| `21_BUILDER_KIT/checklists/new-agent-checklist.md` |
| `21_BUILDER_KIT/checklists/index-update-checklist.md` |

## NUNCA fazer upload

- `_DONO_PRODUTO/*` — coisa do dono
- `.env` — credencial
- `05_WORKSPACE/clientes/*` com dado real — privacidade
- Arquivos PDF antigos do V29
- Tudo em `*.json.local`, `*.csv.local`

## Pacote ZIP automatizado

Forge pode gerar `knowledge-bundle-<projeto>.zip` com os arquivos certos pra cada Project. Pede:

```text
"forge: gera knowledge bundle pro Project CoS V30"
```

E ele consolida em ZIP pronto pra upload.
