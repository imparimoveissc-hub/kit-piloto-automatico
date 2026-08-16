# Relatorio Executivo Mensal - [MES/AAAA]

> Documento mensal pra socios, investidores, conselho ou equipe.
> Gerado todo dia 10, apos fechar DRE.
> Maximo 3 paginas. Comeca com conclusao, detalhe so depois.

---

## Cabecalho

```yaml
empresa: "{{NOME_EMPRESA}}"
periodo: "[MES/AAAA]"
data_emissao: "[AAAA-MM-DD]"
autor: "[Nome do CEO / socio responsavel]"
audiencia: "[Socios / Conselho / Equipe / Investidores]"
```

---

## TL;DR (1 paragrafo, comeca pelo numero)

> Regra: escreva isto POR ULTIMO, depois de analisar tudo. Maximo 5 linhas.

[MES] fechou com faturamento de R$ [valor] ([+/-%] vs mes anterior, [+/-%] vs mesmo mes ano passado). Lucro liquido de R$ [valor] e margem liquida de [%]. [1 frase do que aconteceu de mais importante]. [1 frase do que vamos fazer no proximo mes]. Saldo de caixa fechou em R$ [valor], cobrindo [N] meses de custo fixo.

---

## 1. NUMEROS CHAVE DO MES

| Metrica | Mes atual | Mes anterior | MoM | Mesmo mes ano passado | YoY |
|---|---|---|---|---|---|
| Faturamento bruto | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |
| Faturamento liquido | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |
| Lucro bruto | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |
| EBITDA | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |
| Lucro liquido | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |
| Margem liquida | [%] | [%] | [+/-pp] | [%] | [+/-pp] |
| Numero de vendas | [N] | [N] | [+/-%] | [N] | [+/-%] |
| Ticket medio | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |
| Novos clientes | [N] | [N] | [+/-%] | [N] | [+/-%] |
| Saldo de caixa | R$ [valor] | R$ [valor] | [+/-%] | R$ [valor] | [+/-%] |

> Para detalhe completo do DRE, ver `../dre/[AAAA-MM]-dre.md`.

---

## 2. VENDAS

### Performance vs meta

| Item | Meta do mes | Realizado | % atingido |
|---|---|---|---|
| Faturamento | R$ [valor] | R$ [valor] | [%] |
| Numero de vendas | [N] | [N] | [%] |
| Novos clientes | [N] | [N] | [%] |
| Recompra (% base) | [%] | [%] | [%] |

### Mix por canal

| Canal | Faturamento | % | Variacao vs mes ant |
|---|---|---|---|
| Direto / Site | R$ [valor] | [%] | [+/-%] |
| Indicacao | R$ [valor] | [%] | [+/-%] |
| Trafego pago | R$ [valor] | [%] | [+/-%] |
| Outbound | R$ [valor] | [%] | [+/-%] |
| Marketplace | R$ [valor] | [%] | [+/-%] |

### Top 3 destaques de vendas

1. [Cliente / produto / canal] - R$ [valor] - [contexto]
2. [Cliente / produto / canal] - R$ [valor] - [contexto]
3. [Cliente / produto / canal] - R$ [valor] - [contexto]

### Pipeline futuro

| Fase | Quantidade | Valor potencial |
|---|---|---|
| Em negociacao | [N] | R$ [valor] |
| Proposta enviada | [N] | R$ [valor] |
| Lead qualificado | [N] | R$ [valor] |

---

## 3. MARKETING

### Investimento e retorno

| Canal | Investido | Resultado | CAC | ROAS |
|---|---|---|---|---|
| Meta Ads | R$ [valor] | [N leads / N vendas / R$ X] | R$ [valor] | [N]x |
| Google Ads | R$ [valor] | [N leads / N vendas / R$ X] | R$ [valor] | [N]x |
| Organico (IG / YT / blog) | R$ [valor estimado] | [N leads atribuidos] | R$ [valor] | - |
| Email / WhatsApp | R$ [valor ferramentas] | [N vendas atribuidas] | R$ [valor] | [N]x |
| **TOTAL** | R$ [soma] | - | R$ [media] | [media]x |

### CAC global

```
Investimento total marketing+vendas:  R$ [valor]
Novos clientes no mes:                  [N]
CAC global:                              R$ [calc]
LTV medio:                                R$ [valor]
LTV / CAC:                                [N]x  (saudavel > 3x)
```

---

## 4. FINANCEIRO

### Caixa

```
Saldo inicio mes:                       R$ [valor]
(+) Entradas (recebimentos):            R$ [valor]
(-) Saidas (pagamentos):                R$ [valor]
= Saldo fim mes:                         R$ [valor]
Cobertura de custo fixo:                 [N] meses
```

### Variacao patrimonial vs mes anterior

| Item | Mes anterior | Mes atual | Variacao |
|---|---|---|---|
| Caixa + bancos | R$ [valor] | R$ [valor] | R$ [valor] |
| A receber | R$ [valor] | R$ [valor] | R$ [valor] |
| A pagar | R$ [valor] | R$ [valor] | R$ [valor] |
| Posicao liquida | R$ [valor] | R$ [valor] | R$ [valor] |

### Tributos

- [ ] Todos os tributos do mes pagos
- [ ] DAS / DARF: R$ [valor]
- [ ] INSS patronal: R$ [valor]
- [ ] FGTS: R$ [valor]
- [ ] IRPJ / CSLL (se trimestre): R$ [valor]
- [ ] Carga tributaria efetiva no mes: [%] do faturamento

---

## 5. OPERACAO

### Volume e SLA

| Metrica | Realizado | Meta | Status |
|---|---|---|---|
| Volume de pedidos / projetos | [N] | [N] | [status] |
| % entregue no prazo | [%] | > 95% | [status] |
| Retrabalho / refacao | [%] | < 5% | [status] |
| Tempo medio de entrega | [tempo] | [meta] | [status] |
| NPS | [N] | > 50 | [status] |
| Tickets de suporte | [N abertos / N resolvidos] | - | - |
| Cancelamentos / reembolsos | [N] / R$ [valor] | < [meta] | [status] |

---

## 6. TIME

| Item | Mes atual |
|---|---|
| Headcount total | [N] (CLT [N] + PJ [N] + Estagio [N]) |
| Contratacoes no mes | [N] |
| Saidas no mes | [N] |
| Vagas em aberto | [N] |
| Turnover acumulado 12m | [%] |
| Custo de pessoal / receita | [%] |

### Destaques de time

- [Pessoa / area com destaque positivo no mes]
- [Mudancas organizacionais relevantes]
- [Treinamentos / certificacoes / promocoes]

---

## 7. PROJETOS / INICIATIVAS ESTRATEGICAS

| Projeto | Owner | Fase | % concluido | Status |
|---|---|---|---|---|
| [Nome do projeto] | [nome] | [planning / execucao / homologacao / done] | [%] | [verde / amarelo / vermelho] |
| [Nome do projeto] | [nome] | [fase] | [%] | [status] |

---

## 8. O QUE FUNCIONOU (manter / amplificar)

1. [Iniciativa / decisao que deu resultado] - **Impacto:** [R$ ou %]
2. [Idem]
3. [Idem]

## 9. O QUE NAO FUNCIONOU (corrigir / cortar)

1. [Iniciativa / decisao que falhou] - **Aprendizado:** [o que ficou]
2. [Idem]
3. [Idem]

---

## 10. PLANO PRA PROXIMO MES

### Prioridades

| # | Iniciativa | Responsavel | Resultado esperado | Indicador de sucesso |
|---|---|---|---|---|
| 1 | [acao] | [nome] | [resultado] | [metrica] |
| 2 | [acao] | [nome] | [resultado] | [metrica] |
| 3 | [acao] | [nome] | [resultado] | [metrica] |

### Metas do proximo mes

| Metrica | Meta |
|---|---|
| Faturamento | R$ [valor] |
| Novos clientes | [N] |
| Margem liquida | [%] |
| CAC | R$ [valor] |

---

## 11. RISCOS E ATENCAO

| Risco | Probabilidade | Impacto | Mitigacao | Owner |
|---|---|---|---|---|
| [risco identificado] | [baixa / media / alta] | [R$ ou impacto] | [acao] | [nome] |

Exemplos:
- Cliente concentrado (top 3 = X% receita): diversificar carteira
- Dependencia de canal unico (Meta Ads = X% leads): testar Google + organico
- Mudanca regulatoria iminente: acompanhar e ajustar
- Concorrente novo com preco agressivo: revisar posicionamento

---

## 12. ANEXOS

- DRE completo: `[link ou anexo]`
- Fluxo de caixa: `[link]`
- Dashboard semanal (4 semanas): `[link]`
- Dashboard de marketing por campanha: `[link]`

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Emissao inicial |
