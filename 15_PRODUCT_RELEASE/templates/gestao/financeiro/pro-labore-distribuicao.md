# Pro-Labore e Distribuicao de Lucros

> Decisao mensal sobre quanto cada socio retira da empresa: pro-labore (salario do socio, tem INSS+IR) + distribuicao de lucros (isento de IR pessoa fisica, mas exige lucro real no DRE).
> Rodar APOS fechar DRE do mes ({{NOME_ESCRITORIO}} responsavel ou contador interno).

---

## Cabecalho

```yaml
empresa: "{{NOME_EMPRESA}}"
periodo_referencia: "[AAAA-MM]"
data_fechamento_dre: "[AAAA-MM-DD]"
data_decisao: "[AAAA-MM-DD]"
regime_tributario: "[Simples | Lucro Presumido | Lucro Real]"
```

---

## Pre-requisitos pra distribuir lucro

> Antes de distribuir, validar:

- [ ] DRE do mes fechado e revisado
- [ ] Tributos do mes pagos OU provisionados
- [ ] Folha de pagamento paga
- [ ] Reserva de caixa minima preservada (recomendado: 3 meses de custo fixo)
- [ ] Sem inadimplencia critica > R$ [valor] no recebivel

**Bloqueador**: se qualquer item nao for sim, NAO distribuir lucro nesse mes. Reter caixa.

---

## Quadro de socios

| Socio | % participacao | Pro-labore mensal fixo | Conta destino |
|---|---|---|---|
| [Nome 1] | [%] | R$ [valor] | [banco / conta] |
| [Nome 2] | [%] | R$ [valor] | [banco / conta] |
| [Nome 3] | [%] | R$ [valor] | [banco / conta] |
| **TOTAL** | 100% | R$ [soma] | |

---

## Pro-labore do mes

> Pro-labore tem INSS (11% socio + 20% empresa) e IRRF (tabela progressiva). Funciona como salario.

| Socio | Pro-labore bruto | (-) INSS socio (11%) | (-) IRRF | Liquido a receber | Data prevista |
|---|---|---|---|---|---|
| [Nome 1] | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] | [DD/MM] |
| [Nome 2] | R$ [valor] | R$ [valor] | R$ [valor] | R$ [valor] | [DD/MM] |
| **TOTAL** | R$ [soma] | R$ [soma] | R$ [soma] | R$ [soma] | |

### INSS patronal (empresa paga, 20% sobre pro-labore)

| Item | Valor |
|---|---|
| Base de calculo (total pro-labore bruto) | R$ [valor] |
| INSS patronal (20%) | R$ [valor] |
| Vencimento | dia 20 do mes seguinte |

---

## Apuracao de lucro disponivel pra distribuicao

> Calculo: Lucro Liquido contabil (do DRE) - reserva de caixa - reserva pra investimento

```
Lucro Liquido do mes (DRE linha 15):       R$ [valor]
(-) Reserva de caixa pra preservar:         R$ [valor]
(-) Reserva pra investimento planejado:     R$ [valor]
(-) Reserva pra tributo nao provisionado:   R$ [valor]
= Lucro disponivel pra distribuir:           R$ [valor]
```

### Justificativa de reservas

- **Reserva de caixa**: por que [N] meses de custo fixo? Porque [razao]
- **Reserva pra investimento**: o que ta sendo guardado pra [projeto X]
- **Reserva tributaria**: IRPJ/CSLL trimestral nao provisionado, 13o, ferias

---

## Distribuicao de lucros do mes

> Lucro distribuido proporcionalmente a % de participacao no contrato social.

| Socio | % participacao | Lucro a receber | Conta destino | Data prevista |
|---|---|---|---|---|
| [Nome 1] | [%] | R$ [valor] | [banco] | [DD/MM] |
| [Nome 2] | [%] | R$ [valor] | [banco] | [DD/MM] |
| **TOTAL** | 100% | R$ [valor] | | |

> Distribuicao de lucros e isenta de IRPF (pessoa fisica) DESDE QUE o lucro esteja apurado contabilmente (DRE assinado pelo contador). Sem isso, vira pro-labore disfarcado e tem multa.

---

## Total liquido por socio (pro-labore + lucros)

| Socio | Pro-labore liquido | Distribuicao lucro | TOTAL recebido no mes |
|---|---|---|---|
| [Nome 1] | R$ [valor] | R$ [valor] | R$ [valor] |
| [Nome 2] | R$ [valor] | R$ [valor] | R$ [valor] |
| **TOTAL EMPRESA** | R$ [soma] | R$ [soma] | R$ [soma] |

---

## Impacto no caixa

```
Saldo da empresa antes:           R$ [valor]
(-) Pro-labore bruto total:        R$ [valor]
(-) INSS patronal:                 R$ [valor]
(-) Distribuicao de lucros:        R$ [valor]
= Saldo apos retiradas:             R$ [valor]
```

- [ ] Saldo apos retiradas >= reserva de caixa minima

---

## Comparativo historico (ultimos 6 meses)

| Mes | Lucro liquido | Pro-labore total | Lucro distribuido | % distribuido do lucro |
|---|---|---|---|---|
| [M-5] | R$ [valor] | R$ [valor] | R$ [valor] | [%] |
| [M-4] | R$ [valor] | R$ [valor] | R$ [valor] | [%] |
| [M-3] | R$ [valor] | R$ [valor] | R$ [valor] | [%] |
| [M-2] | R$ [valor] | R$ [valor] | R$ [valor] | [%] |
| [M-1] | R$ [valor] | R$ [valor] | R$ [valor] | [%] |
| [Atual] | R$ [valor] | R$ [valor] | R$ [valor] | [%] |

---

## Regras internas combinadas entre socios

- Pro-labore valor base: R$ [valor] (revisado anualmente)
- % do lucro distribuido por padrao: [%] (resto vira reserva)
- Frequencia de revisao: [mensal / trimestral / anual]
- Quem aprova ajuste de pro-labore: [todos socios / socio majoritario / unanime]
- Em caso de prejuizo no mes: [decisao previa, ex: nao retirar lucro, manter pro-labore X]

---

## Aprovacao

| Quem | Aprovou? | Data | Observacao |
|---|---|---|---|
| Socio 1 | [SIM/NAO] | [DD/MM] | |
| Socio 2 | [SIM/NAO] | [DD/MM] | |
| Contador | [revisou DRE] | [DD/MM] | |

---

## Acoes para o proximo mes

- [ ] Revisar pro-labore se atualizar (anualmente)
- [ ] Provisionar IRPJ/CSLL trimestral (se Lucro Presumido)
- [ ] Ajustar reserva de caixa conforme variacao do custo fixo
- [ ] Conferir DCTFWeb / eSocial / DARF INSS pago

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Mes inicial |
