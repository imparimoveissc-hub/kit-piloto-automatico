# Prompts: Gestao de Contas (Account Management) B2B

## Como usar
Copie o prompt, substitua as variaveis entre colchetes e cole na IA. Esses prompts cobrem pos-venda: retencao, expansao, satisfacao e gestao ativa da carteira de clientes.

---

## Prompt 1: Criar Relatorio Mensal de Resultados para o Cliente

```
Atue como um Customer Success Manager que gera relatorios que
justificam o investimento do cliente.

DADOS DO CLIENTE:
- Empresa: [NOME_EMPRESA]
- Plano: [PLANO_CONTRATADO]
- Investimento mensal: R$ [VALOR]
- Cliente desde: [DATA_INICIO]
- Responsavel CS: [NOME_CS]

METRICAS DO MES:
[Cole aqui os dados do periodo -- pode ser texto, planilha, print do dashboard]

- [METRICA_1]: [VALOR]
- [METRICA_2]: [VALOR]
- [METRICA_3]: [VALOR]
- [METRICA_4]: [VALOR]

METAS ACORDADAS:
- [META_1]: [VALOR_META]
- [META_2]: [VALOR_META]
- [META_3]: [VALOR_META]

ACOES REALIZADAS NO MES:
- [ACAO_1]
- [ACAO_2]
- [ACAO_3]

Gere um relatorio mensal profissional com:
1. RESUMO EXECUTIVO (3-4 frases, foco em resultado)
2. DASHBOARD DE METRICAS (tabela comparando meta vs. realizado vs. mes anterior)
3. DESTAQUES POSITIVOS (o que funcionou e por que)
4. PONTOS DE ATENCAO (o que precisa melhorar, com acao proposta)
5. ACOES DO PROXIMO MES (3-5 prioridades)
6. ROI ACUMULADO (quanto o cliente ja recuperou do investimento)

Tom: profissional, orientado a dados, transparente.
Formato: pronto para enviar por email ao decisor.
```

---

## Prompt 2: Identificar Oportunidades de Upsell/Cross-sell

```
Atue como um Account Manager focado em expansao de receita.

CARTEIRA DE CLIENTES:
[Liste seus clientes ativos com as informacoes abaixo]

| Cliente | Plano atual | Valor/mes | Meses ativo | NPS | Uso da solucao |
|---------|-------------|-----------|-------------|-----|----------------|
| [CLIENTE_1] | [PLANO] | R$ [N] | [N] | [N] | [%] |
| [CLIENTE_2] | [PLANO] | R$ [N] | [N] | [N] | [%] |
| [CLIENTE_3] | [PLANO] | R$ [N] | [N] | [N] | [%] |
| [CLIENTE_4] | [PLANO] | R$ [N] | [N] | [N] | [%] |
| [CLIENTE_5] | [PLANO] | R$ [N] | [N] | [N] | [%] |

MEUS PRODUTOS/SERVICOS DISPONIVEIS PARA EXPANSAO:
- [PRODUTO_UPSELL_1]: R$ [VALOR] -- [DESCRICAO]
- [PRODUTO_UPSELL_2]: R$ [VALOR] -- [DESCRICAO]
- [PRODUTO_CROSSSELL_1]: R$ [VALOR] -- [DESCRICAO]
- [PRODUTO_CROSSSELL_2]: R$ [VALOR] -- [DESCRICAO]

Para cada cliente, me de:
1. SCORE DE PROPENSAO A EXPANSAO (1-10)
2. PRODUTO RECOMENDADO (upsell ou cross-sell)
3. GATILHO DE ABORDAGEM (o que justifica a conversa agora)
4. MENSAGEM DE ABORDAGEM (pronta para enviar, 3-4 frases)
5. VALOR POTENCIAL DE EXPANSAO (R$/mes)
6. TIMING IDEAL (quando abordar)

No final, calcule:
- Receita adicional potencial total
- Top 3 contas prioritarias para abordar esta semana
```

---

## Prompt 3: Criar Plano de Retencao para Cliente em Risco de Churn

```
Atue como um especialista em retencao de clientes B2B.

CLIENTE EM RISCO:
- Empresa: [NOME_EMPRESA]
- Contato principal: [NOME] -- [CARGO]
- Cliente desde: [DATA]
- Plano: [PLANO] -- R$ [VALOR]/mes
- Receita total gerada ate hoje: R$ [VALOR_TOTAL]

SINAIS DE RISCO:
[Marque os que se aplicam]
- [ ] Uso da plataforma caiu [N]% nos ultimos [N] meses
- [ ] Nao participa das reunioes de acompanhamento
- [ ] Reclamou de [PROBLEMA]
- [ ] Pediu reducao de plano ou pausa
- [ ] Mencionou concorrente
- [ ] Mudanca de lideranca na empresa
- [ ] Resultados abaixo do esperado
- [ ] Faturamento do cliente caiu
- [ ] Outro: [DESCREVA]

HISTORICO RECENTE:
- Ultima interacao: [DATA] -- [O QUE FOI DISCUTIDO]
- NPS mais recente: [NOTA]
- Feedback recebido: "[FEEDBACK_DO_CLIENTE]"

Crie um plano de retencao com:

1. DIAGNOSTICO
   - Classificacao do risco (baixo/medio/alto/critico)
   - Causa raiz provavel
   - Impacto financeiro se perder esse cliente

2. PLANO DE ACAO IMEDIATO (proximos 7 dias)
   - Acao 1: [O que fazer + quem faz + ate quando]
   - Acao 2: [O que fazer + quem faz + ate quando]
   - Acao 3: [O que fazer + quem faz + ate quando]

3. CONVERSA DE RETENCAO
   - Script de abertura (reconhecer o problema, nao minimizar)
   - Perguntas para entender a insatisfacao real
   - Ofertas de retencao (do menor ao maior custo):
     a) Sem custo (atencao, suporte prioritario)
     b) Baixo custo (feature, treinamento extra)
     c) Medio custo (desconto temporario, upgrade)
     d) Alto custo (reducao de preco -- ultima opcao)

4. PLANO DE RECUPERACAO (30-60 dias)
   - Quick wins para restaurar confianca
   - Metricas para acompanhar a recuperacao
   - Cadencia de check-ins
   - Criterio de sucesso (quando considerar "retido")

5. EMAIL DE REENGAJAMENTO
   - Texto pronto para enviar ao decisor
   - Tom: humilde, proativo, focado em solucao
```

---

## Prompt 4: Montar QBR (Quarterly Business Review)

```
Atue como um CS senior que conduz QBRs que renovam contratos.

DADOS PARA O QBR:

CLIENTE:
- Empresa: [NOME_EMPRESA]
- Decisor: [NOME] -- [CARGO]
- Operacional: [NOME_OP] -- [CARGO_OP]
- Plano: [PLANO] -- R$ [VALOR]/mes
- Contrato renova em: [DATA_RENOVACAO]

RESULTADOS DO TRIMESTRE:
| Metrica | Q anterior | Q atual | Meta | Status |
|---------|------------|---------|------|--------|
| [M1] | [N] | [N] | [N] | [+/-]% |
| [M2] | [N] | [N] | [N] | [+/-]% |
| [M3] | [N] | [N] | [N] | [+/-]% |
| [M4] | [N] | [N] | [N] | [+/-]% |

MARCOS ALCANCADOS:
- [MARCO_1]
- [MARCO_2]
- [MARCO_3]

DESAFIOS DO PERIODO:
- [DESAFIO_1] -- Como resolvemos: [RESOLUCAO_1]
- [DESAFIO_2] -- Status: [ABERTO/RESOLVIDO]

Monte o QBR completo:

1. AGENDA DA REUNIAO (60 min)
   - Tempo por bloco
   - Quem apresenta cada parte

2. SLIDE POR SLIDE
   - Retrospectiva de resultados (antes/depois com numeros)
   - ROI acumulado desde o inicio do contrato
   - Highlights do trimestre
   - Pontos de melhoria (transparencia)
   - Roadmap do proximo trimestre
   - Oportunidades de expansao (se aplicavel)
   - Alinhamento de expectativas para renovacao

3. PERGUNTAS ESTRATEGICAS
   - 5 perguntas para entender prioridades do proximo trimestre
   - 3 perguntas para mapear expansao

4. EMAIL PRE-QBR
   - Convite com agenda e expectativas

5. EMAIL POS-QBR
   - Resumo das decisoes e proximos passos
```

---

## Prompt 5: Criar Programa de Indicacao B2B (Referral)

```
Atue como um estrategista de growth B2B focado em indicacoes.

MINHA EMPRESA:
- Nome: [NOME_DA_SUA_EMPRESA]
- O que vendemos: [PRODUTO/SERVICO]
- Ticket medio: R$ [VALOR]/mes
- Segmento: [SEGMENTO]
- Numero de clientes ativos: [N]
- NPS medio: [NOTA]
- Clientes promotores (NPS 9-10): [N]

PERFIL DO CLIENTE IDEAL (ICP):
- [DESCRICAO_ICP]

Crie um programa de indicacao B2B completo:

1. ESTRUTURA DO PROGRAMA
   - Nome do programa (algo memoravel, nao "Programa de Indicacao")
   - Regras claras (quem pode indicar, o que conta como indicacao valida)
   - Recompensas por nivel:
     a) Indicacao que vira reuniao
     b) Indicacao que vira proposta
     c) Indicacao que fecha contrato
   - Exemplos de recompensa B2B (nao e cupom de desconto, e algo corporativo)

2. COMUNICACAO DE LANCAMENTO
   - Email para clientes promotores anunciando o programa
   - Mensagem para enviar via WhatsApp/LinkedIn
   - Post para redes sociais

3. MOMENTO IDEAL PARA PEDIR INDICACAO
   - 5 momentos do ciclo de vida do cliente onde a indicacao e natural
   - Script exato para cada momento

4. FOLLOW-UP COM INDICADOS
   - Email/mensagem para o lead indicado (mencionando quem indicou)
   - Cadencia de follow-up especifica para leads por indicacao

5. METRICAS DO PROGRAMA
   - KPIs para acompanhar
   - Meta de indicacoes por cliente por trimestre
   - CAC via indicacao vs. CAC geral (benchmark)

6. TEMPLATE DE AGRADECIMENTO
   - Email para o cliente que indicou (quando a indicacao fecha)
```
