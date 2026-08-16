# Kit Piloto Automatico V30

Stack pra operar funis, campanhas e entregas de servico com menos contexto, mais controle de qualidade e roteamento inteligente por etapa.

O V30 herda o que funcionou em iteracoes anteriores: CoS como entry point, loading sob demanda, gates e pipeline por fases. O salto esta em reduzir agentes residentes, transformar tarefas em contratos pequenos e usar roteamento de modelos por criticidade.

## Principios

- CoS gerencia tarefas, contexto e rotas. Ele nao faz trabalho de especialista quando uma etapa exige profundidade.
- Cada task tem contrato de entrada, saida, budget e gate. Nada de prompts gigantes permanentes.
- Conhecimento entra por diretriz curta e sob demanda, nao por template.
- Copy segue principios do GOAT-copy em versao leve: VOC, DRE, MUP, MUS, awareness, prova especifica e voz humana.
- Modelos caros entram apenas em decisoes irreversiveis, estrategia, mecanismo, copy final e revisao critica.
- Full-auto por padrao: assumir o caminho mais seguro e registrar a premissa. Perguntar so quando a decisao for irreversivel ou faltar dado bloqueante.

## Mapa

```text
Kit-Piloto-Automatico-V30/
├── 00_INDEX.md
├── CLAUDE.md
├── 00_OS/                       # CoS, router, economia de contexto, modelos, gates
├── 01_PIPELINE/                 # Pipeline mestre e ciclo operacional
├── 02_AGENTS/                   # Time reduzido de especialistas
├── 03_TASKS/                    # Contratos pequenos de execucao
├── 04_DIRETRIZES/               # Conhecimento acionavel, sem templates de copy
├── 05_WORKSPACE/                # Estado de projetos/clientes
├── 06_OUTPUTS/                  # Entregaveis finais
├── 07_LOGS/                     # Ledger de tasks, decisoes e cache
├── 08_CHECKLISTS/               # Gates e listas de validacao
├── 10_TEMPLATES_OPERACIONAIS/   # Templates de estado, projeto e entrega
├── 11_TRAFFIC_STACK/            # Operacao Meta Ads com CLI e diagnosticos reais
├── 12_WHATSAPP_STACK/           # Bots WhatsApp, SDR, sucesso, follow-up e Cowork
├── 13_ADAPTIVE_SQUADS/          # Squads vivos por cliente, fase e gargalo
├── 15_PRODUCT_RELEASE/          # Camada publica simples para o aluno final
├── 18_AUTOMATION_STACK/         # Automacoes genericas de processos
├── 20_MCP_SETUP/                # Conectores MCP: Drive, WhatsApp, Slack, Meta, Composio, etc.
├── 21_BUILDER_KIT/              # Forge agent + scaffolds (criar agente/skill/task/diretriz)
└── 22_CLAUDE_DESKTOP/           # Adaptacao do kit pro Claude Desktop (Projects + MCPs + palavras-chave)
```

## Como usar

1. Comece por `00_OS/cos.md`.
2. O CoS classifica o pedido, cria ou atualiza a task no ledger e escolhe rota + perfil de modelo.
3. O especialista recebe apenas o pacote minimo: objetivo, insumos, restricoes, budget e gate.
4. Cada entrega volta com handoff curto, nao com historico completo.
5. Gates bloqueiam avancos caros quando a base esta fraca.

Para usuario pouco tecnico, rode primeiro `/preflight-acessos`. Isso concentra pastas, URLs, acessos, limites de automacao e pendencias no inicio, em vez de interromper cada etapa.

## Setup inicial (uma vez por maquina) — 1 comando

```text
instalar kpa30
```

OU no Claude Code:

```text
/instalar-kpa30
```

Wizard guiado que cobre tudo em ~15-20 min:

- Dependencias (Node, Git).
- `.env` local.
- MCPs essenciais (Composio Rube, WhatsApp, Filesystem, Playwright).
- Meta Ads CLI (opcional, so se rodar trafego pago).
- Projects do Claude Desktop (se for app).
- Onboarding do negocio (empresa, nicho, produto, publico, canal, gargalo).
- Primeira tarefa util adaptada.

Detalhes em `INICIO_RAPIDO.md` ou `00_OS/commands/instalar-kpa30.md`.

Para WhatsApp/Cowork, o kit gera documentos em modo `draft` antes de qualquer ativacao real. Disparo em massa, publicacao, budget e mudanca destrutiva continuam exigindo confirmacao humana.

## V30 Complete

O V30 tem duas camadas:

- **Motor interno**: `00_OS/`, pipeline, agents, gates, Traffic Stack, WhatsApp Stack e Adaptive Squads.
- **Release publica**: `15_PRODUCT_RELEASE/`, a pasta que o aluno final entende e usa.

Para processos recorrentes, use `18_AUTOMATION_STACK/`: o agente de automacoes transforma qualquer rotina do cliente em blueprint, SOP, teste e plano de ativacao em modo `draft`.

Para criar novos agentes, skills, tasks ou diretrizes, use o **Forge** em `21_BUILDER_KIT/` (`/forge` dentro do Claude Code). Ele cria seguindo o padrao V30 e atualiza indices automaticamente.

## Pro Claude Desktop (app)

**90% dos mentorados usam o Claude Desktop (app), nao o Claude Code (CLI).** Em `22_CLAUDE_DESKTOP/` tem tudo pra rodar o kit no app:

- Como criar Project (com system prompt + knowledge files + custom instructions).
- Template de `claude_desktop_config.json` pros MCPs.
- Mapping de comandos `/` -> palavras-chave (sem `/` no Desktop).
- Lista priorizada de arquivos pra upload no Project.
- 3-5 Projects recomendados (CoS / Trafego / WhatsApp / Auto / Forge).

## Anti-leak (CRITICO)

- `.env` esta no `.gitignore`. **Nunca** commitar `.env` real.
- `.env.example` e o template (sem segredos) — esse sim vai pro Git.
- Tokens, `act_id`, `pixel_id` e qualquer credencial real ficam SOMENTE no `.env` local OU em variavel de ambiente.
- Em caso de vazamento acidental: revogar o token no provider (Meta Business Manager, Composio, Slack, etc.) IMEDIATAMENTE.

## O que ficou fora de proposito

- Conteudo ultra-especifico de clientes do dono do kit.
- Templates longos de copy.
- Swipes copiados.
- Agentes demais carregados ao mesmo tempo.
- Conhecimento profundo carregado antes de existir uma task que precise dele.
- Kits completos por nicho antes do core estar validado em usuario piloto.
