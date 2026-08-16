# Nicho B2B -- Kit Piloto Automatico com IA

## O que e isso

Pacote completo de templates e prompts para empresas que vendem para outras empresas (B2B). Cobre todo o ciclo comercial: da prospeccao ao onboarding do cliente.

## Para quem

- Empresarios B2B que querem escalar o processo comercial com IA
- SDRs que precisam de cadencias e mensagens de prospeccao
- Closers que precisam de propostas e scripts de reuniao
- Gestores comerciais que precisam de relatorios de pipeline
- CS que precisa de templates de onboarding e gestao de contas

## Estrutura

```
b2b/
├── CLAUDE.md                          Instrucoes do agente para contexto B2B
├── templates/
│   ├── prospeccao-outbound.md         Mensagens de prospeccao fria + cadencia
│   ├── proposta-comercial-b2b.md      Proposta comercial completa com ROI
│   ├── relatorio-pipeline.md          Relatorio semanal de pipeline/funil
│   ├── script-reuniao-vendas.md       Script completo de discovery + vendas
│   └── onboarding-cliente-b2b.md      Onboarding em 4 fases (0 a 90 dias)
├── prompts/
│   ├── prospeccao.md                  5 prompts de prospeccao e qualificacao
│   ├── vendas.md                      5 prompts de processo de vendas
│   └── account-management.md          5 prompts de gestao de contas
└── README.md                          Este arquivo
```

## Ciclo coberto

```
PROSPECCAO → QUALIFICACAO → DISCOVERY → PROPOSTA → CLOSE → ONBOARDING → CS
     |             |             |           |         |         |         |
  Template 1    Prompt 3     Template 4   Template 2  Prompt 5  Template 5  Prompt AM
  Prompt 1-2    Prompt 4     Prompt V1    Prompt V2   Prompt V3  Prompt AM  Prompt AM
```

## Templates (5)

| Template | Fase | Quem usa |
|----------|------|----------|
| prospeccao-outbound.md | Gerar demanda | SDR |
| proposta-comercial-b2b.md | Converter em cliente | Closer |
| relatorio-pipeline.md | Acompanhar resultados | Gestor |
| script-reuniao-vendas.md | Conduzir discovery | Closer |
| onboarding-cliente-b2b.md | Integrar novo cliente | CS |

## Prompts (15)

### Prospeccao (5)
1. Gerar lista de prospeccao por ICP
2. Criar sequencia de outbound multicanal
3. Qualificar lead com perguntas BANT
4. Pesquisar empresa antes da abordagem
5. Criar email de reengajamento para leads frios

### Vendas (5)
1. Preparar reuniao de discovery
2. Criar proposta comercial personalizada
3. Contornar objecoes especificas
4. Criar apresentacao de vendas (deck consultivo)
5. Criar email de follow-up pos-proposta

### Account Management (5)
1. Criar relatorio mensal de resultados
2. Identificar oportunidades de upsell/cross-sell
3. Criar plano de retencao para cliente em risco
4. Montar QBR (Quarterly Business Review)
5. Criar programa de indicacao B2B (referral)

## Como usar

1. Abra o template ou prompt relevante para sua necessidade
2. Substitua as variaveis entre colchetes [ASSIM] com seus dados
3. Cole na IA e ajuste conforme necessario
4. Use o CLAUDE.md como contexto se estiver usando dentro do Claude Code

## Vocabulario-chave

ICP, MQL, SQL, SDR, Closer, CS, Pipeline, Ticket medio, CAC, LTV, Churn, MRR, ARR, Outbound, Inbound, Discovery, QBR, Upsell, Cross-sell
