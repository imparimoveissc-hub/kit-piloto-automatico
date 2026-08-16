# Templates Financeiro

Controle financeiro do PROPRIO negocio (uso interno). Diferente de DRE que e entregavel pra cliente final, aqui sao templates pra dono de empresa ou socio organizar a operacao financeira.

## O que tem aqui

| Arquivo | O que e | Frequencia |
|---|---|---|
| `fluxo-caixa-mensal.md` | Mapa entradas/saidas/saldo com previsao 90 dias | Atualizar 1x por semana, fechar 1x por mes |
| `contas-a-pagar-receber.md` | Controle das obrigacoes e creditos a vencer | Atualizar diariamente, fechar 1x por semana |
| `pro-labore-distribuicao.md` | Calculo e distribuicao de pro-labore + dividendos | 1x por mes (apos fechar DRE) |
| `checklist-financeiro-semanal.md` | Rotina de revisao financeira de 30 min | Toda segunda-feira pela manha |

## Pra quem e

- Dono de pequena/media empresa fazendo gestao financeira sem time financeiro
- Freelancer/profissional liberal organizando PJ
- Socio de agencia/consultoria/escritorio querendo visibilidade real do caixa
- Operador de e-commerce/infoproduto rodando sem CFO

## Antes de comecar

Fixar os dados basicos do negocio em um arquivo `meu-negocio.yaml`:

```yaml
empresa: "[Nome da empresa]"
cnpj: "[XX.XXX.XXX/XXXX-XX]"
regime_tributario: "[Simples | Lucro Presumido | Lucro Real]"
contas_bancarias:
  - banco: "[Nome]"
    tipo: "[CC | Poupanca | Investimento]"
    saldo_inicial: 0
custo_fixo_mensal_estimado: 0       # aluguel + folha + softwares fixos
meta_reserva_caixa_meses: 3         # quantos meses de custo fixo manter como reserva
data_corte_mensal: 25               # dia do mes em que fecha o periodo (padrao 25)
```

## Sequencia recomendada de uso

1. Abrir `checklist-financeiro-semanal.md` toda segunda
2. Atualizar `contas-a-pagar-receber.md` (entradas confirmadas + saidas previstas)
3. Atualizar `fluxo-caixa-mensal.md` (consolidar contas + projetar 90 dias)
4. No fechamento mensal, atualizar `pro-labore-distribuicao.md`
5. Cruzar com DRE do mes (ver `../dre/`) pra validar numeros

## Regra de ouro

**Numero antes de sentimento.** Se voce nao ta vendo o numero, voce nao ta gerenciando. Tres minutos atualizando todo dia evitam tres dias arrumando depois.
