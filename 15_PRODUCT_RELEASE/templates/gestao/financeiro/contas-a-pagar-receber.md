# Contas a Pagar e a Receber

> Controle granular de obrigacoes (a pagar) e creditos (a receber). Atualizar diariamente, fechar 1x por semana.
> Conecta com `fluxo-caixa-mensal.md` (este aqui e a fonte, fluxo de caixa e a visao consolidada).

---

## Cabecalho

```yaml
empresa: "{{NOME_EMPRESA}}"
data_referencia: "[AAAA-MM-DD]"
responsavel: "[Nome]"
ferramentas: "[Planilha Google / ERP Conta Azul / Asaas / proprio]"
```

---

## CONTAS A RECEBER

### Em aberto (a vencer)

| Vencimento | Cliente | Origem (NF / Contrato / Boleto) | Valor | Forma | Status | Acao |
|---|---|---|---|---|---|---|
| [DD/MM] | [Nome] | NF [num] / Contrato [ref] | R$ [valor] | [boleto / pix / cartao / transf] | [aguardando / negociando] | [proxima acao] |
| [DD/MM] | [Nome] | [origem] | R$ [valor] | [forma] | [status] | [acao] |

### Atrasadas

| Vencimento | Cliente | Origem | Valor original | Dias atraso | Juros/multa | Total atual | Acao |
|---|---|---|---|---|---|---|---|
| [DD/MM] | [Nome] | [origem] | R$ [valor] | [N dias] | R$ [calc] | R$ [total] | [1a cobranca / 2a / juridico] |

**Regra de cobranca:**
- D+3: WhatsApp amigavel automatico
- D+7: Email formal com boleto atualizado
- D+15: Telefonema pessoal
- D+30: Carta de cobranca + suspensao de servico (se aplicavel)
- D+60: Protesto / juridico

### Recebidas no periodo

| Data recebimento | Cliente | Origem | Valor | Conta destino |
|---|---|---|---|---|
| [DD/MM] | [Nome] | [origem] | R$ [valor] | [conta] |

### Resumo a receber

| Status | Quantidade | Valor total |
|---|---|---|
| A vencer | [N] | R$ [valor] |
| Atrasadas | [N] | R$ [valor] |
| Recebidas no mes | [N] | R$ [valor] |
| **TOTAL EM ABERTO** | **[N]** | **R$ [valor]** |

---

## CONTAS A PAGAR

### Em aberto (a vencer)

| Vencimento | Fornecedor / Origem | Categoria | Valor | Forma | Status | Codigo barras / PIX |
|---|---|---|---|---|---|---|
| [DD/MM] | [Nome] | [Fixo / Variavel / Tributo / Folha] | R$ [valor] | [boleto / debito / pix] | [previsto / agendado / pago] | [se tem] |

### Atrasadas

| Vencimento | Fornecedor | Categoria | Valor original | Dias atraso | Juros/multa | Total atual | Acao |
|---|---|---|---|---|---|---|---|
| [DD/MM] | [Nome] | [categoria] | R$ [valor] | [N dias] | R$ [calc] | R$ [total] | [renegociar / pagar / parcelar] |

**Bloqueador critico**: tributo em atraso > 30 dias OU folha em atraso = parar tudo e resolver.

### Pagas no periodo

| Data pagamento | Fornecedor | Categoria | Valor | Conta origem |
|---|---|---|---|---|
| [DD/MM] | [Nome] | [categoria] | R$ [valor] | [conta] |

### Resumo a pagar

| Categoria | A vencer | Atrasadas | Pagas no mes | Total comprometido |
|---|---|---|---|---|
| Fixo | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |
| Variavel | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |
| Tributo | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |
| Folha | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] |
| **TOTAL** | R$ [soma] | R$ [soma] | R$ [soma] | R$ [soma] |

---

## Posicao consolidada (a receber - a pagar)

```
A receber (em aberto + atrasadas):   R$ [valor]
A pagar (em aberto + atrasadas):     R$ [valor]
= Posicao liquida:                    R$ [valor]
```

### Status

- [ ] Posicao liquida positiva
- [ ] Atraso de cliente < 5% do total a receber
- [ ] Zero atraso em tributo
- [ ] Zero atraso em folha
- [ ] Nenhum fornecedor critico em atraso

---

## Aging (idade dos atrasos)

### Recebivel

| Faixa | Quantidade | Valor |
|---|---|---|
| Em dia | [N] | R$ [valor] |
| 1-7 dias atraso | [N] | R$ [valor] |
| 8-30 dias atraso | [N] | R$ [valor] |
| 31-60 dias atraso | [N] | R$ [valor] |
| 60+ dias atraso | [N] | R$ [valor] |

### Pagavel

| Faixa | Quantidade | Valor |
|---|---|---|
| Em dia | [N] | R$ [valor] |
| 1-7 dias atraso | [N] | R$ [valor] |
| 8-30 dias atraso | [N] | R$ [valor] |
| 30+ dias atraso (CRITICO) | [N] | R$ [valor] |

---

## Indicadores

| Indicador | Valor | Status |
|---|---|---|
| Inadimplencia (atrasado / total a receber) | [%] | [verde < 5%, amarelo 5-10%, vermelho > 10%] |
| Prazo medio de recebimento (DSO) | [dias] | [verde < 30, amarelo 30-45, vermelho > 45] |
| Prazo medio de pagamento (DPO) | [dias] | [maior = melhor pra caixa] |
| Ciclo financeiro = DSO - DPO | [dias] | [menor = melhor] |

---

## Acoes da semana

| Prioridade | Acao | Responsavel | Prazo |
|---|---|---|---|
| Alta | [acao] | [nome] | [DD/MM] |
| Media | [acao] | [nome] | [DD/MM] |

Exemplos:
- "Ligar pro cliente X (atraso 15 dias, R$ 4.500), oferecer parcelamento em 2x"
- "Renegociar boleto Y do fornecedor Z (vence 25/MM, antecipa pra 20/MM com 2% desconto)"
- "Agendar pagamento de DAS no banco antes do dia 20"

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Estado inicial |
