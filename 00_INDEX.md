# Indice Mestre V30

> Entry point: `00_OS/cos.md`
> Modo operacional: full-auto com registro de premissas

## Visao de 30 segundos

```text
Usuario
  -> CoS
      -> cria/atualiza task
      -> escolhe trilha
      -> escolhe perfil de modelo
      -> monta context pack minimo
      -> aciona especialista
          -> produz output
          -> roda gate
          -> escreve handoff curto
      -> CoS atualiza ledger
```

## Camadas

| Camada | Pasta | Funcao |
|---|---|---|
| L0 | `00_OS/` | Governanca, CoS, router, budgets, gates |
| L1 | `01_PIPELINE/` | Sequencia de fases e dependencias |
| L2 | `02_AGENTS/` | Especialistas reduzidos |
| L3 | `03_TASKS/` | Contratos atomicos de execucao |
| L4 | `04_DIRETRIZES/` | Conhecimento carregado sob demanda |
| L5 | `05_WORKSPACE/` | Estado vivo de projetos |
| L6 | `07_LOGS/` | Memoria curta, decisoes e ledger |
| Templates | `10_TEMPLATES_OPERACIONAIS/` | Contexto, estado e handoff |
| Trafego | `11_TRAFFIC_STACK/` | 8 agentes operacionais sobre Meta Ads CLI |
| WhatsApp | `12_WHATSAPP_STACK/` | Bots de prospeccao, SDR, sucesso, follow-up e docs Cowork |
| Squads | `13_ADAPTIVE_SQUADS/` | Squads adaptativos por cliente, fase, canal e gargalo |
| Release | `15_PRODUCT_RELEASE/` | Camada publica simples para o aluno final |
| Automacoes | `18_AUTOMATION_STACK/` | Processos, SOPs, blueprints, ferramentas e ativacao segura |
| MCPs | `20_MCP_SETUP/` | Conectores prontos: Drive, WhatsApp, Slack, Meta, Composio |
| Builder | `21_BUILDER_KIT/` | Forge agent + scaffolds para criar agentes, skills, tasks, diretrizes |
| Desktop | `22_CLAUDE_DESKTOP/` | Adaptacao do kit pro Claude Desktop (app) — Projects, system prompt, MCPs, palavras-chave |

## Rotas principais

| Pedido | Rota | Modelo padrao |
|---|---|---|
| "organiza isso", "o que fazer agora" | CoS + task manager | router-cheap |
| Pesquisa, mercado, VOC | Researcher | research-balanced |
| Posicionamento, oferta, mecanismo | Strategist | strategy-frontier |
| Copy, LP, ads, email, VSL | Copy Director | copy-balanced -> copy-frontier se gate falhar |
| WhatsApp, SDR, chatbot, follow-up, Cowork | WhatsApp Orchestrator | conversation-balanced |
| Automacao, processo, SOP, n8n, Make, Zapier, Cowork generico | Automation Architect | automation-balanced |
| Pagina, criativo, video, pacote visual | Production Lead | production-balanced |
| Campanha, metricas, diagnostico | Traffic Analyst | analytics-balanced |
| Produto robusto, LP vs entrega, promessa | Product Auditor | reviewer-frontier |
| Squads, comandos por cliente, adaptacao | CoS + Adaptive Squads | router-cheap |
| "criar agente", "nova skill", "nova diretriz", "construir camada" | Forge (Builder) | strategy-frontier |
| Conectar Drive/WhatsApp/Slack/Meta/CRM | CoS + MCP Setup | router-cheap |
| Revisao, stress test, qualidade | QA Editor | reviewer-frontier quando bloqueante |

## Arquivos-chave

- `00_OS/cos.md` - comportamento do Chief of Staff.
- `00_OS/model-router.yaml` - slots de modelo por etapa.
- `00_OS/context-economy.md` - regras de economia de tokens.
- `00_OS/task-manager.md` - ciclo de vida de tasks.
- `00_OS/gates.md` - gates bloqueantes.
- `00_OS/gate-matrix.md` - severidade, verdict e escalada.
- `00_OS/cache-policy.md` - TTL e compactacao de contexto.
- `00_OS/access-preflight.md` - acessos, pastas, ferramentas e limites logo no inicio.
- `00_OS/proactivity-policy.md` - quando agir full-auto e quando bloquear.
- `00_OS/bootstrap.md` - sequencia de inicializacao.
- `01_PIPELINE/kpa-v30-pipeline.yaml` - pipeline mestre.
- `04_DIRETRIZES/copy-goat-lite.md` - creme de copy, sem templates.
- `10_TEMPLATES_OPERACIONAIS/` - templates de projeto, cliente, task e entrega.
- `11_TRAFFIC_STACK/PLAYBOOK.html` - manual operacional da stack de trafego.
- `12_WHATSAPP_STACK/README.md` - arquitetura WhatsApp, SDR, CS, follow-up e Cowork.
- `13_ADAPTIVE_SQUADS/README.md` - squads adaptativos e manifest por cliente.
- `15_PRODUCT_RELEASE/COMECE_AQUI.md` - entrada publica para usuario leigo.
- `18_AUTOMATION_STACK/README.md` - agente de automacoes e blueprints de processo.
- `20_MCP_SETUP/README.md` - conectores MCP recomendados e como instalar.
- `21_BUILDER_KIT/README.md` - Forge agent (cria agentes, skills, tasks, diretrizes).
- `22_CLAUDE_DESKTOP/README.md` - adaptacao pro Claude Desktop (app), Projects, MCPs, palavras-chave.
- `22_CLAUDE_DESKTOP/setup-project.md` - passo a passo de configurar Project no Desktop.
- `22_CLAUDE_DESKTOP/cos-desktop-system-prompt.md` - system prompt completo pro CoS rodar no Desktop.
- `00_OS/commands/atualizar-apartamentos-na-planta.md` - comando operacional para atualizar apartamentos na planta da Impar no Imobibrasil com fonte oficial, descricao, valor m2 e validacao publica.
- `15_PRODUCT_RELEASE/curso/README.md` - trilha publica do curso para usuario final.
- `07_LOGS/task-ledger.md` - quadro vivo de tarefas.

## Setup inicial (mentorados) — 1 COMANDO

```text
instalar kpa30
```

OU no Claude Code:

```text
/instalar-kpa30
```

Wizard guiado que cobre todas as etapas (~15-20 min):

1. Confere dependencias.
2. Configura `.env`.
3. Ativa MCPs essenciais (Composio Rube, WhatsApp, Filesystem, Playwright).
4. Configura Meta Ads CLI (opcional, so se rodar trafego pago).
5. Cria Projects do Claude Desktop (se for app).
6. Onboarding do negocio (empresa, nicho, produto, publico, canal, gargalo).
7. Gera primeira tarefa util adaptada.

Detalhes em `00_OS/commands/instalar-kpa30.md`.

## Setup avancado (manual)

Caso queira rodar etapas separadas:

```text
/meta-cli-install    # so Meta Ads CLI
/mcp-setup           # so MCPs
/preflight-acessos   # so preflight
```

**REGRA DE OURO ANTI-LEAK:** `.env` esta no `.gitignore`. Tokens NUNCA vao pro Git. Quem clonar/forkar o kit recebe `.env.example` (template), nunca `.env` (real).

Antes de operar qualquer cliente real, rode:

```text
/preflight-acessos
```

O preflight concentra acessos a pastas, LP, Cowork, WhatsApp, CRM, Meta, checkout e analytics, e separa o que pode rodar full-auto do que exige confirmacao humana.

## Conectar ferramentas externas (MCPs)

Drive, WhatsApp, Slack, Facebook/Instagram, Gmail, Notion: ver `20_MCP_SETUP/README.md` e rode `/mcp-setup` dentro do Claude Code.

## Criar novos agentes, skills, tasks, diretrizes

Use o **Forge** (Builder): `/forge` dentro do Claude Code. Ele cria agente, skill, task ou diretriz seguindo o padrao V30 e atualiza indices/routing automaticamente. Detalhes em `21_BUILDER_KIT/README.md`.

## Usar no Claude Desktop (app)

90% dos mentorados vao usar o Claude Desktop (app), nao o Claude Code (CLI).

Pra setup, seguir `22_CLAUDE_DESKTOP/README.md`:

1. Criar Project no Claude Desktop (3 recomendados: CoS V30 + Trafego + WhatsApp).
2. Colar system prompt de `22_CLAUDE_DESKTOP/cos-desktop-system-prompt.md`.
3. Upload knowledge files conforme `22_CLAUDE_DESKTOP/knowledge-files.md`.
4. Configurar MCPs com template `22_CLAUDE_DESKTOP/claude-desktop-config.json`.
5. Comandos no Desktop sao palavras-chave (sem `/`) — ver `22_CLAUDE_DESKTOP/commands-keywords.md`.
