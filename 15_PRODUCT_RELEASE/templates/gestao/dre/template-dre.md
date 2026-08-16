# Template - DRE Mensal

> Versao Markdown estruturada. Serve de fonte unica pra geracao de XLSX, PDF e corpo de email.
> Preencher campos `[A PREENCHER]` por cliente/mes.

---

## Cabecalho

```yaml
cliente: "[A PREENCHER]"
cnpj: "[A PREENCHER]"
regime_tributario: "[Simples | Lucro Presumido | Lucro Real]"
periodo_referencia: "[AAAA-MM]"
data_emissao: "[AAAA-MM-DD]"
contador_responsavel: "[Nome] - CRC [num]"
revisor: "[Nome]"
escritorio: "{{NOME_ESCRITORIO}}"
moeda: "BRL"
```

---

## Demonstracao do Resultado (formato vertical)

| Linha | Conta | Valor (R$) | % Receita Liquida | MoM (%) | YoY (%) |
|---|---|---|---|---|---|
| 1 | **Receita Bruta** | [A PREENCHER] | - | - | - |
| 2 | (-) Deducoes (ICMS, ISS, PIS, COFINS, devolucoes) | [A PREENCHER] | - | - | - |
| 3 | **= Receita Liquida** | [A PREENCHER] | 100% | - | - |
| 4 | (-) CMV / CPV / CSP | [A PREENCHER] | - | - | - |
| 5 | **= Lucro Bruto** | [A PREENCHER] | - | - | - |
| 6 | (-) Despesas com Vendas | [A PREENCHER] | - | - | - |
| 7 | (-) Despesas Administrativas | [A PREENCHER] | - | - | - |
| 8 | (-) Outras Despesas Operacionais | [A PREENCHER] | - | - | - |
| 9 | **= EBITDA** | [A PREENCHER] | - | - | - |
| 10 | (-) Depreciacao e Amortizacao | [A PREENCHER] | - | - | - |
| 11 | **= EBIT (Lucro Operacional)** | [A PREENCHER] | - | - | - |
| 12 | (+/-) Resultado Financeiro | [A PREENCHER] | - | - | - |
| 13 | **= LAIR (Lucro Antes do IR/CSLL)** | [A PREENCHER] | - | - | - |
| 14 | (-) IRPJ e CSLL | [A PREENCHER] | - | - | - |
| 15 | **= Lucro Liquido do Periodo** | [A PREENCHER] | - | - | - |

---

## Indicadores chave

| Indicador | Formula | Valor | Benchmark setorial | Status |
|---|---|---|---|---|
| Margem Bruta | Lucro Bruto / Receita Liquida | [%] | [%] | [verde/amarelo/vermelho] |
| Margem Operacional (EBIT) | EBIT / Receita Liquida | [%] | [%] | [verde/amarelo/vermelho] |
| Margem EBITDA | EBITDA / Receita Liquida | [%] | [%] | [verde/amarelo/vermelho] |
| Margem Liquida | Lucro Liquido / Receita Liquida | [%] | [%] | [verde/amarelo/vermelho] |
| Ponto de Equilibrio | Custo Fixo / Margem Contribuicao | R$ [valor] | - | - |
| Carga Tributaria efetiva | (Deducoes + IRPJ + CSLL) / Receita Bruta | [%] | [%] | [verde/amarelo/vermelho] |

---

## Comparativo MoM (mes vs mes anterior)

```
Receita Bruta:    R$ [atual]  vs  R$ [anterior]  =  +/- [%]
Lucro Bruto:      R$ [atual]  vs  R$ [anterior]  =  +/- [%]
EBITDA:           R$ [atual]  vs  R$ [anterior]  =  +/- [%]
Lucro Liquido:    R$ [atual]  vs  R$ [anterior]  =  +/- [%]
```

## Comparativo YoY (mes vs mesmo mes ano passado)

```
Receita Bruta:    R$ [atual]  vs  R$ [yoy]  =  +/- [%]
Lucro Bruto:      R$ [atual]  vs  R$ [yoy]  =  +/- [%]
EBITDA:           R$ [atual]  vs  R$ [yoy]  =  +/- [%]
Lucro Liquido:    R$ [atual]  vs  R$ [yoy]  =  +/- [%]
```

---

## Top 3 variacoes do mes

### Positivas
1. **[Linha/conta]** - variacao de R$ [valor] (+[%]). Causa provavel: [explicacao em linguagem simples].
2. **[Linha/conta]** - variacao de R$ [valor] (+[%]). Causa provavel: [explicacao].
3. **[Linha/conta]** - variacao de R$ [valor] (+[%]). Causa provavel: [explicacao].

### Negativas
1. **[Linha/conta]** - variacao de R$ [valor] (-[%]). Causa provavel: [explicacao].
2. **[Linha/conta]** - variacao de R$ [valor] (-[%]). Causa provavel: [explicacao].
3. **[Linha/conta]** - variacao de R$ [valor] (-[%]). Causa provavel: [explicacao].

---

## Insights (linguagem do cliente, sem jargao)

> Regra: cada insight comeca pelo numero, explica o que significa no negocio e sugere acao concreta.

1. **[Insight 1]** - [contexto + significado + acao sugerida em 2-3 linhas]
2. **[Insight 2]** - [idem]
3. **[Insight 3]** - [idem]

Exemplos de bons insights:
- "Sua margem bruta caiu de 42% pra 36% esse mes. Significa que voce ta vendendo o mesmo, mas sobrando menos depois do custo direto. Provavel: aumento de fornecedor ou desconto agressivo. Acao: revisar lista de precos e renegociar com fornecedor X."
- "Voce gastou R$ 18 mil em despesa administrativa contra R$ 12 mil em abril. Crescimento de 50% sem aumento de receita proporcional. Vale olhar contrato a contrato pra identificar o que entrou nesse mes."

---

## Recomendacoes

| Prioridade | Recomendacao | Impacto estimado | Prazo sugerido |
|---|---|---|---|
| Alta | [acao] | [R$ ou %] | [data] |
| Media | [acao] | [R$ ou %] | [data] |
| Baixa | [acao] | [R$ ou %] | [data] |

---

## Alertas e atencao

- [ ] Algum tributo em atraso? [SIM/NAO + valor]
- [ ] Algum pagamento de folha em atraso? [SIM/NAO]
- [ ] Algum lancamento sem documento fiscal? [SIM/NAO + valor]
- [ ] Variacao acima de 30% em alguma linha sem justificativa? [SIM/NAO]
- [ ] Risco de descumprir limite do Simples Nacional? [SIM/NAO]

---

## Anexos enviados ao cliente

- [ ] DRE PDF formatado
- [ ] Balancete sintetico (opcional, por padrao NAO enviar)
- [ ] Razao analitico de contas com maior variacao (sob demanda)

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Emissao original |
| v2 | [AAAA-MM-DD] | [se houver retificacao, descrever] |
