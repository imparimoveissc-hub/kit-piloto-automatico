# Convencoes V30 — Builder Reference

> Lei pra qualquer elemento novo no kit. Forge segue isso. Voce tambem deveria.

## Nomenclatura

| Elemento | Padrao | Exemplo |
|---|---|---|
| Agent file | `02_AGENTS/<nome>.md` ou stack/agents/<nome>.md | `copy-director.md` |
| Skill | `XX_STACK/skills/<nome>/SKILL.md` | `direct-response-br/SKILL.md` |
| Task | `03_TASKS/T<NN>-<descricao>.md` | `T03-copy-nucleus.md` |
| Diretriz | `04_DIRETRIZES/<topico>.md` | `voz-ptbr.md` |
| MCP connector | `20_MCP_SETUP/connectors/<nome>.md` | `whatsapp-mcp.md` |
| Wrapper Claude | `.claude/agents/<nome>.md` | `cos.md` |
| Command | `.claude/commands/<nome>.md` | `preflight-acessos.md` |
| Output | `06_OUTPUTS/YYYY-MM-DD_<projeto>/` | `2026-05-09_kpa-v30-lp-audit/` |

## Estilo de nome

- **kebab-case** sempre. Sem underscores, sem CamelCase.
- **descritivo, nao generico.** `customer-success-bot` > `cs-bot` > `helper`.
- **prefixo `T` em tasks** com 2 digitos. T00, T01... T09, T10.
- **prefixo `@` ao referenciar** agentes em texto. `@copy-director`, `@forge`.

## Header obrigatorio

### Agent

```markdown
---
name: <kebab-case>
description: <1 frase do que faz>
tier: 0 | 1 | 2 | 3   # opcional
---

# @<nome>

## Papel
...

## Boot
...

## Inputs
...

## Output
...

## Gate
...

## Regras
...
```

### Skill

```markdown
---
name: <kebab-case>
description: <quando ativar>
metadata:
  priority: <numero>
  triggers:
    phrases: []
    pathPatterns: []
---

# Skill: <Nome>

## Quando usar

## Workflow

## Output esperado

## Anti-patterns
```

### Task

```markdown
# T<NN> - <Nome>

```yaml
owner: <agent>
model_profile: <slot>
objective: <1 frase>
inputs:
  required: []
  optional: []
output_contract: []
acceptance_gate: GATE-<NOME>
budget: baixo | medio | alto
```

## Action items
- ...
```

### Diretriz

```markdown
# <Topico>

## Objetivo

## Princpios

## Anti-patterns

## Gate de uso
```

### MCP Connector

```markdown
# <Nome> — <Descricao curta>

## Setup

## Tools

## Casos de uso

## Seguranca
```

## Gates (resumo)

| Tipo | Quando aplica |
|---|---|
| GATE-INTAKE | Entrada de pedido / task contract |
| GATE-RESEARCH | VOC, mercado, concorrente |
| GATE-STRATEGY | Oferta, mecanismo, promessa |
| GATE-COPY | Copy final, ad, LP, VSL, email |
| GATE-PRODUCTION | Pagina, criativo, video, asset |
| GATE-TRAFFIC | Campanha paga ao vivo |
| GATE-WHATSAPP | Fluxo WhatsApp / Cowork |
| GATE-AUTOMATION | Processo automatizado |
| GATE-PRODUCT | LP vs entrega real |
| GATE-DELIVERY | Entregavel final pro cliente/aluno |

Pra criar gate novo, use prefixo `GATE-` + topico. Documenta em `00_OS/gates.md`.

## Severidade (matriz)

S0 cosmetico | S1 nota | S2 rework | S3 bloqueio | S4 escalar.

Documentado em `00_OS/gate-matrix.md`.

## Model profile (router)

Slots em `00_OS/model-router.yaml`. Use:

- `router-cheap` — triagem, ledger, classificacao
- `research-balanced` — pesquisa, sintese
- `strategy-frontier` — decisao irreversivel
- `copy-balanced` / `copy-frontier` — rascunho/final
- `production-balanced` — assets
- `analytics-balanced` — metricas
- `conversation-balanced` — WhatsApp, SDR
- `automation-balanced` — blueprints
- `reviewer-frontier` — gate bloqueante

## Wrapper

Agente em `02_AGENTS/<nome>.md` PRECISA de wrapper em `.claude/agents/<nome>.md`:

```markdown
---
name: <nome>
description: <descricao curta>
---

# Wrapper Claude Agent - <Nome>

Leia e siga `02_AGENTS/<nome>.md`.

[notas opcionais]
```

Command em `00_OS/commands/<nome>.md` PRECISA de wrapper em `.claude/commands/<nome>.md`:

```markdown
# /<nome>

Use `00_OS/commands/<nome>.md`.
```

## Indices a atualizar

Toda criacao toca:

1. **`00_INDEX.md`** — adicionar na tabela de camadas + rotas + arquivos-chave
2. **`00_OS/router.md`** — adicionar linha na tabela de roteamento primario
3. **`00_OS/cos.md`** — adicionar linha na tabela de classificacao
4. **`00_OS/knowledge-loader.md`** — se diretriz, adicionar mapa
5. **`02_AGENTS/README.md`** — se agente, adicionar tabela
6. **`22_CLAUDE_DESKTOP/knowledge-files.md`** — adicionar arquivo no Project
7. **`22_CLAUDE_DESKTOP/commands-keywords.md`** — adicionar palavra-chave

## Restricoes finais

- **Tudo em pt-BR.** Comentarios, descricoes, exemplos.
- **Tudo em modo `draft`** ate validacao.
- **Sem cliente real** em scaffold (use `[A PREENCHER]` ou `Empresa X`).
- **Sem token/credencial** em arquivo do kit.
- **Sem promessa nao-validada.** Se nao testou, nao afirma.
