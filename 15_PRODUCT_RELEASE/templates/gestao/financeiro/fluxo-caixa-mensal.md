# Fluxo de Caixa Mensal

> Mapa de entradas, saidas e saldo previsto. Diferente do DRE (regime de competencia), aqui e **regime de caixa**: so entra quando o dinheiro entra na conta, so sai quando sai.
> Use pra responder: "Eu vou ter dinheiro pra pagar o que ja prometi?"

---

## Cabecalho

```yaml
empresa: "{{NOME_EMPRESA}}"
periodo_referencia: "[AAAA-MM]"
moeda: "BRL"
ultima_atualizacao: "[AAAA-MM-DD HH:MM]"
responsavel: "[Nome do socio/financeiro]"
```

---

## Saldo inicial

| Conta | Banco | Saldo dia 1 do mes | Reservado (compromissos) | Disponivel real |
|---|---|---|---|---|
| Conta corrente principal | [A PREENCHER] | R$ [valor] | R$ [valor] | R$ [valor] |
| Conta corrente secundaria | [A PREENCHER] | R$ [valor] | R$ [valor] | R$ [valor] |
| Poupanca / Reserva | [A PREENCHER] | R$ [valor] | R$ [valor] | R$ [valor] |
| **TOTAL** | | **R$ [soma]** | **R$ [soma]** | **R$ [soma]** |

> "Reservado" = dinheiro que ja tem destino (tributo a recolher, parcela ja contratada, etc).

---

## Entradas previstas no mes

| Data prev | Cliente / Origem | Descricao | Valor | Status | Conta destino |
|---|---|---|---|---|---|
| [DD/MM] | [Nome] | [Mensalidade X / Projeto Y / Boleto N] | R$ [valor] | [previsto / confirmado / atrasado / recebido] | [conta] |
| [DD/MM] | [Nome] | [descricao] | R$ [valor] | [status] | [conta] |
| | | **TOTAL ENTRADAS PREVISTAS** | **R$ [soma]** | | |

### Indicadores entradas

- Total previsto no mes: R$ [valor]
- Ja confirmado/recebido: R$ [valor] ([%])
- Ainda pendente: R$ [valor] ([%])
- Atrasado: R$ [valor]
- Ticket medio previsto: R$ [valor]

---

## Saidas previstas no mes

### Custos fixos (recorrentes, mesmo valor todo mes)

| Data prev | Descricao | Categoria | Valor | Status | Forma pagto |
|---|---|---|---|---|---|
| [DD] | Aluguel | Operacional | R$ [valor] | [pago / previsto] | [boleto / debito] |
| [DD] | Folha de pagamento | Pessoal | R$ [valor] | [status] | [forma] |
| [DD] | Pro-labore | Pessoal | R$ [valor] | [status] | [forma] |
| [DD] | Contador | Servicos | R$ [valor] | [status] | [forma] |
| [DD] | Softwares (lista no anexo) | Operacional | R$ [valor] | [status] | [forma] |
| [DD] | Internet / Telefone | Operacional | R$ [valor] | [status] | [forma] |
| [DD] | Energia / Agua | Operacional | R$ [valor] | [status] | [forma] |
| | **SUBTOTAL FIXO** | | **R$ [soma]** | | |

### Custos variaveis (dependem de receita ou eventos)

| Data prev | Descricao | Categoria | Valor | Status | Forma pagto |
|---|---|---|---|---|---|
| [DD] | Trafego pago (Meta/Google) | Marketing | R$ [valor] | [status] | [forma] |
| [DD] | Comissao de vendas | Comercial | R$ [valor] | [status] | [forma] |
| [DD] | Insumos / Estoque | Operacional | R$ [valor] | [status] | [forma] |
| [DD] | Frete | Operacional | R$ [valor] | [status] | [forma] |
| | **SUBTOTAL VARIAVEL** | | **R$ [soma]** | | |

### Tributos e obrigacoes

| Data prev | Tributo | Competencia | Valor | Status | Codigo barras |
|---|---|---|---|---|---|
| [DD] | DAS Simples Nacional / DARF | [mes/ano] | R$ [valor] | [status] | [se tem] |
| [DD] | INSS patronal | [mes/ano] | R$ [valor] | [status] | |
| [DD] | FGTS | [mes/ano] | R$ [valor] | [status] | |
| [DD] | IRPJ / CSLL trimestral (se aplicavel) | [trimestre] | R$ [valor] | [status] | |
| [DD] | ISS / ICMS | [mes/ano] | R$ [valor] | [status] | |
| | **SUBTOTAL TRIBUTOS** | | **R$ [soma]** | | |

### Investimentos / nao recorrentes

| Data prev | Descricao | Valor | Status | Justificativa |
|---|---|---|---|---|
| [DD] | [Compra / aporte / curso / equipamento] | R$ [valor] | [status] | [por que vale] |

### Resumo saidas

| Categoria | Valor | % do total |
|---|---|---|
| Custos fixos | R$ [soma] | [%] |
| Custos variaveis | R$ [soma] | [%] |
| Tributos | R$ [soma] | [%] |
| Investimentos | R$ [soma] | [%] |
| **TOTAL SAIDAS PREVISTAS** | **R$ [soma]** | **100%** |

---

## Saldo final previsto

```
Saldo inicial:             R$ [valor]
(+) Entradas previstas:    R$ [valor]
(-) Saidas previstas:      R$ [valor]
= Saldo final previsto:    R$ [valor]
```

### Status do mes

- [ ] Saldo final previsto > zero
- [ ] Saldo final previsto > 1 mes de custo fixo (reserva minima)
- [ ] Saldo final previsto > 3 meses de custo fixo (reserva ideal)

**Alerta vermelho**: saldo final previsto negativo OU abaixo de 1 mes de custo fixo.

---

## Projecao 90 dias (proximos 3 meses)

| Mes | Entradas previstas | Saidas previstas | Saldo do mes | Saldo acumulado |
|---|---|---|---|---|
| [Mes 1] | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |
| [Mes 2] | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |
| [Mes 3] | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |

### Alertas pra 90 dias

- [ ] Algum mes da projecao fica negativo?
- [ ] Algum tributo grande caindo (IRPJ trimestral, 13o salario, ferias)?
- [ ] Algum cliente grande com contrato terminando?
- [ ] Algum investimento planejado nao previsto?

---

## Indicadores chave do mes

| Indicador | Valor | Status |
|---|---|---|
| Margem de caixa = (Saldo final / Receita) | [%] | [verde/amarelo/vermelho] |
| Burn rate mensal = (Saidas / Saldo disponivel) | [meses] | [verde/amarelo/vermelho] |
| Cobertura de custo fixo = Saldo / Custo fixo | [meses] | [verde/amarelo/vermelho] |
| % de receita comprometida em tributo | [%] | [verde/amarelo/vermelho] |
| Atraso medio de recebimento | [dias] | [verde/amarelo/vermelho] |

Benchmarks de referencia:
- Margem de caixa: > 15% saudavel
- Cobertura de custo fixo: minimo 1 mes, ideal 3 meses
- Carga tributaria: depende do regime (Simples ~6-15%, LP ~13-19%, LR variavel)

---

## Acoes do mes (escrito apos analise)

| Prioridade | Acao | Prazo | Responsavel |
|---|---|---|---|
| Alta | [acao concreta com verbo + objeto] | [DD/MM] | [nome] |
| Media | [acao] | [DD/MM] | [nome] |
| Baixa | [acao] | [DD/MM] | [nome] |

Exemplos de boas acoes:
- "Renegociar prazo de pagamento com fornecedor X (atual 30 dias, pedir 45)"
- "Cobrar cliente Y que esta com R$ 8.500 atrasado ha 22 dias"
- "Cancelar 2 softwares ociosos identificados (Z e W, R$ 480/mes)"
- "Antecipar 30% do recebivel de cartao do mes (custa 2%, libera R$ 12k)"

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Mes inicial |
