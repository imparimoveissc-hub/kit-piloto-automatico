# 11_TRAFFIC_STACK — Traffic Stack do Kit Piloto Automático V30

> Stack expandida de agentes especializados em tráfego pago Direct Response, análise de campanhas, criativos, funil, atribuição, escala e inteligência competitiva. Opera sobre o CLI nativo `meta` (WSL no Windows / nativo no macOS-Linux) e complementa os agents do V30.

## Por que esta camada existe

O resto do V30 (CoS + agents de copy + pipeline) é orientado a **planejamento e criação** de campanhas (briefing → estrutura → copy → criativos → subir). A Traffic Stack é orientada a **operação contínua** sobre campanhas vivas:

- Diagnóstico de queda de performance
- Análise de criativos (hook rate, retention, padrões vencedores)
- Auditoria de tracking (Pixel + CAPI saúde)
- Escala de vencedores (ABO/CBO/lateralização)
- Inteligência competitiva (Meta Ad Library, swipe, benchmark)
- Análise de funil end-to-end (ads → LP → VSL → quiz → checkout)

E faz isso conectada ao CLI `meta` oficial, permitindo puxar dados reais e gerar relatórios de campanhas vivas — não só planejar campanhas novas. Pra instalar o CLI do zero, rode `/meta-cli-install` dentro do Claude Code (cobre Windows via WSL Ubuntu e macOS/Linux nativo).

## Arquitetura

```
┌────────────────────────────────────────────────────────────────┐
│  L0 — Orquestração                                              │
│  @traffic-orchestrator (chief da stack)                         │
└──────────────┬──────────────────────────────────────────────────┘
               │
   ┌───────────┴───────────┬─────────────┬────────────┬──────────┐
   ▼                       ▼             ▼            ▼          ▼
┌──────────────┐  ┌─────────────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐
│ Execução     │  │ Análise         │  │ Tracking │  │ Otimização   │  │ Intel        │
├──────────────┤  ├─────────────────┤  ├──────────┤  ├──────────────┤  ├──────────────┤
│ @meta-dr-    │  │ @creative-      │  │ @attrib- │  │ @traffic-    │  │ @competitor- │
│ specialist   │  │ analyst         │  │ ution-   │  │ diagnostician│  │ spy          │
│              │  │                 │  │ auditor  │  │              │  │              │
│              │  │ @funnel-analyst │  │          │  │ @scaling-    │  │              │
│              │  │                 │  │          │  │ strategist   │  │              │
└──────────────┘  └─────────────────┘  └──────────┘  └──────────────┘  └──────────────┘
                          │
                          ▼
                  Reaproveita @traffic-analyst (V30)
                  para relatórios consolidados
```

### Os 8 agentes

| # | Agente | Responsabilidade |
|---|---|---|
| 1 | `@traffic-orchestrator` | Recebe pedido, detecta cliente, lê context, roteia |
| 2 | `@meta-dr-specialist` | Direct Response Meta — broad targeting, criativo-first, kill criteria, lateralização Oxigênio |
| 3 | `@creative-analyst` | Hook rate, retention curve, padrões vencedores, gera lateralizações |
| 4 | `@funnel-analyst` | Funil completo: ads → LP → VSL → quiz → checkout. Identifica drop-off |
| 5 | `@attribution-auditor` | Pixel + CAPI saúde, match quality, deduplicação, atribuição |
| 6 | `@traffic-diagnostician` | Investigação forensic de queda — root cause analysis |
| 7 | `@scaling-strategist` | Quando escalar, quanto, qual método (ABO/CBO/Oxigênio/horizontal) |
| 8 | `@competitor-spy` | Meta Ad Library, BigSpy, swipe, engenharia reversa de funis |

## Estrutura de pastas

```
11_TRAFFIC_STACK/
├── README.md                             # Este arquivo
├── agents/                               # 8 definições de agente
│   ├── traffic-orchestrator.md
│   ├── meta-dr-specialist.md
│   ├── creative-analyst.md
│   ├── funnel-analyst.md
│   ├── attribution-auditor.md
│   ├── traffic-diagnostician.md
│   ├── scaling-strategist.md
│   └── competitor-spy.md
├── tasks/                                # Tasks operacionais
│   ├── diagnosticar-campanha-meta-cli.md
│   ├── analisar-criativos.md
│   ├── investigar-queda.md
│   ├── escalar-vencedores.md
│   └── espionar-concorrente.md
├── skills/
│   └── direct-response-br/
│       └── SKILL.md                      # DR brasileiro: ABO, CBO, Oxigênio, kill criteria
├── playbooks/
│   ├── direct-response-flow.md
│   ├── quiz-funnel-flow.md
│   └── vsl-flow.md
└── templates/
    ├── relatorio-diagnostico-tmpl.html
    ├── relatorio-criativos-tmpl.html
    └── cliente-template/                 # Template pra novo cliente em 05_WORKSPACE/clientes/
        ├── CLAUDE.md
        ├── act-mapping.yaml
        ├── icp.md
        ├── funil.md
        └── baseline-kpis.md
```

## Integração com o resto do V30

- **Reusa `@traffic-analyst`** (V30) — relatórios consolidados, dashboards, projeções
- **Reusa diretrizes** em `04_DIRETRIZES/` carregadas sob demanda — conhecimento técnico Meta
- **Reusa `@cos`** (entry point V30) — `@cos` roteia tráfego pra `@traffic-orchestrator`
- **Lê `05_WORKSPACE/clientes/<cliente>/`** sempre — context obrigatório por cliente
- **Conecta com CLI nativo `meta`** — toda análise puxa dados reais

## Multi-conta — como funciona

A stack é multi-conta por design:

1. **`00_OS/clients-map.yaml`** — mapeia cada `act_id` Meta para um cliente do V30 (criar conforme necessário)
2. **`05_WORKSPACE/clientes/<cliente>/act-mapping.yaml`** — mapeia todas as contas de um cliente (alguns têm múltiplas)
3. **CLI** — `meta ads <recurso> <ação> --ad-account-id act_XXXXXXXXXXXXXXX` por comando
4. **Token** — System User Token (gerado no Business Manager) precisa ter acesso a TODAS as contas. NUNCA hardcoded — vive no `.env` (gitignored) ou no `~/.profile` do WSL

## Convenções

- Todos os agentes operam em **pt-BR** (greeting, output, prompts)
- Saída padrão: **HTML visual** (relatórios) ou **markdown estruturado** (briefings táticos)
- **Ações destrutivas** (pause, delete, budget mudança >20%): confirmação manual obrigatória, mesmo em auto mode
- **Dados reais sempre** — nenhum agente inventa número. Se CLI falhar, agente reporta erro e para
- **Frameworks Tier 1 padronizados** — todos seguem (1) DRE 5 níveis (2) Funil 4 estágios (3) Diagnóstico Onde Quebrou (4) Andrômeda Era (Meta v25)

## Roadmap

### Sprint 1 (atual — Maio 2026)
- [x] Estrutura `11_TRAFFIC_STACK/` criada
- [ ] 8 agentes definidos (em andamento)
- [ ] Task `diagnosticar-campanha-meta-cli.md`
- [ ] Skill `direct-response-br`
- [ ] Cliente piloto definido pelo operador

### Sprint 2 (próximo)
- [ ] Adicionar clientes em `05_WORKSPACE/clientes/`
- [ ] Templates HTML de relatório
- [ ] Playbooks de funil (DR, Quiz, VSL)

### Sprint 3 (futuro)
- [ ] Integração Google Ads CLI (quando setup estiver pronto)
- [ ] Skill `direct-response-tiktok`
- [ ] Auto-execução agendada (cron diário/semanal)

## Versão

- **v1.0.0** — 2026-05-04 — Criação inicial
