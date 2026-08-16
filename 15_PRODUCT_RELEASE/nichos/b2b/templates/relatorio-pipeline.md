# Template: Relatorio de Pipeline / Funil de Vendas

## Quando usar
Reuniao semanal de vendas, report para diretoria, ou analise individual de performance do time comercial. Frequencia recomendada: semanal (operacional) e mensal (estrategico).

---

## Cabecalho

```
RELATORIO DE PIPELINE
[NOME_EMPRESA]

Periodo: [DATA_INICIO] a [DATA_FIM]
Responsavel: [NOME_GESTOR]
Time: [NOMES_DO_TIME]
```

---

## 1. Resumo Executivo

| Metrica | Semana Anterior | Semana Atual | Variacao |
|---------|-----------------|--------------|----------|
| Leads gerados | [N] | [N] | [+/-]% |
| MQLs | [N] | [N] | [+/-]% |
| SQLs | [N] | [N] | [+/-]% |
| Reunioes agendadas | [N] | [N] | [+/-]% |
| Propostas enviadas | [N] | [N] | [+/-]% |
| Deals fechados | [N] | [N] | [+/-]% |
| Receita fechada | R$ [N] | R$ [N] | [+/-]% |

**Destaque da semana:** [1 frase sobre o principal resultado positivo ou negativo]

---

## 2. Funil por Etapa

| Etapa | Quantidade | Valor Total | Taxa de Conversao | Meta |
|-------|------------|-------------|-------------------|------|
| Prospeccao | [N] | R$ [N] | -- | [N] |
| Qualificacao | [N] | R$ [N] | [N]% | [N] |
| Discovery | [N] | R$ [N] | [N]% | [N] |
| Proposta | [N] | R$ [N] | [N]% | [N] |
| Negociacao | [N] | R$ [N] | [N]% | [N] |
| Fechamento | [N] | R$ [N] | [N]% | [N] |

**Pipeline total:** R$ [VALOR_TOTAL]
**Previsao ponderada:** R$ [VALOR_PONDERADO] (considerando probabilidade por etapa)

---

## 3. Performance Individual

| SDR/Closer | Atividades | Reunioes | Propostas | Deals | Receita | % Meta |
|------------|------------|----------|-----------|-------|---------|--------|
| [NOME_1] | [N] | [N] | [N] | [N] | R$ [N] | [N]% |
| [NOME_2] | [N] | [N] | [N] | [N] | R$ [N] | [N]% |
| [NOME_3] | [N] | [N] | [N] | [N] | R$ [N] | [N]% |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **R$ [N]** | **[N]%** |

---

## 4. Deals em Risco

| Deal | Empresa | Valor | Etapa | Dias parado | Risco | Acao necessaria |
|------|---------|-------|-------|-------------|-------|-----------------|
| [DEAL_1] | [EMP_1] | R$ [N] | [ETAPA] | [N] dias | Alto | [ACAO] |
| [DEAL_2] | [EMP_2] | R$ [N] | [ETAPA] | [N] dias | Medio | [ACAO] |
| [DEAL_3] | [EMP_3] | R$ [N] | [ETAPA] | [N] dias | Alto | [ACAO] |

> **Regra:** Deal parado por mais de [N] dias na mesma etapa entra na lista de risco.

---

## 5. Deals com Previsao de Fechamento (Proximos 30 dias)

| Deal | Empresa | Valor | Probabilidade | Data prevista | Proximo passo |
|------|---------|-------|---------------|---------------|---------------|
| [DEAL_1] | [EMP_1] | R$ [N] | [N]% | [DATA] | [ACAO] |
| [DEAL_2] | [EMP_2] | R$ [N] | [N]% | [DATA] | [ACAO] |
| [DEAL_3] | [EMP_3] | R$ [N] | [N]% | [DATA] | [ACAO] |

**Total previsto (30 dias):** R$ [TOTAL_PREVISTO]

---

## 6. Metricas de Eficiencia

| Metrica | Atual | Meta | Status |
|---------|-------|------|--------|
| Ciclo medio de venda | [N] dias | [N] dias | [OK/ATENCAO/CRITICO] |
| Ticket medio | R$ [N] | R$ [N] | [OK/ATENCAO/CRITICO] |
| Win rate | [N]% | [N]% | [OK/ATENCAO/CRITICO] |
| CAC | R$ [N] | R$ [N] | [OK/ATENCAO/CRITICO] |
| LTV/CAC | [N]x | [N]x | [OK/ATENCAO/CRITICO] |
| Taxa de no-show | [N]% | <[N]% | [OK/ATENCAO/CRITICO] |

---

## 7. Motivos de Perda (Deals Perdidos no Periodo)

| Motivo | Quantidade | % do total | Valor perdido |
|--------|------------|------------|---------------|
| Preco/orcamento | [N] | [N]% | R$ [N] |
| Timing (nao e prioridade agora) | [N] | [N]% | R$ [N] |
| Escolheu concorrente | [N] | [N]% | R$ [N] |
| Sem resposta / ghosting | [N] | [N]% | R$ [N] |
| Nao era fit (ICP errado) | [N] | [N]% | R$ [N] |
| **Total** | **[N]** | **100%** | **R$ [N]** |

---

## 8. Acoes da Semana

### O que funcionou
- [ACAO_POSITIVA_1]
- [ACAO_POSITIVA_2]

### O que precisa melhorar
- [PONTO_MELHORIA_1] → Acao: [ACAO_CORRETIVA_1]
- [PONTO_MELHORIA_2] → Acao: [ACAO_CORRETIVA_2]

### Prioridades proxima semana
1. [PRIORIDADE_1]
2. [PRIORIDADE_2]
3. [PRIORIDADE_3]

---

## Checklist do Relatorio

- [ ] Dados do CRM atualizados antes de gerar o report
- [ ] Todos os deals com etapa e valor corretos
- [ ] Deals parados identificados com acao definida
- [ ] Performance individual revisada com cada membro
- [ ] Previsao de fechamento realista (nao otimista)
- [ ] Motivos de perda categorizados corretamente
