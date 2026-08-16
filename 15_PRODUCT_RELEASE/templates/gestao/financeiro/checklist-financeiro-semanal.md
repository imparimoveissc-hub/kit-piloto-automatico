# Checklist Financeiro Semanal

> 30 minutos toda segunda-feira pra entrar na semana com visibilidade total.
> Se voce nao ve, voce nao gerencia. Tres minutos por dia evitam tres dias arrumando depois.

---

## Cabecalho

```yaml
empresa: "{{NOME_EMPRESA}}"
semana_referencia: "[AAAA-MM-DD a AAAA-MM-DD]"
responsavel: "[Nome]"
duracao_revisao: "[minutos gastos]"
```

---

## 1. Conferencia bancaria (10 min)

- [ ] Conciliar extrato de TODAS as contas (cartao + corrente + poupanca)
- [ ] Cada lancamento dos ultimos 7 dias tem categoria atribuida
- [ ] Nenhum lancamento "desconhecido" pendente
- [ ] Saldo do sistema bate com saldo do banco
- [ ] Nenhum cheque/boleto a compensar perdido

**Bloqueador**: divergencia > R$ 100 sem identificar -> resolver antes de seguir.

---

## 2. Contas a receber (5 min)

- [ ] Atualizar status de boletos/PIX da semana passada (recebido / nao recebido)
- [ ] Identificar atrasos novos (D+1 a D+7)
- [ ] Disparar cobranca automatica D+3 (WhatsApp amigavel)
- [ ] Listar clientes que precisam ligacao pessoal (D+15+)
- [ ] Atualizar previsao de recebimento da semana

**Acao da semana** (cobranca): [escrever lista de quem cobrar]

---

## 3. Contas a pagar (5 min)

- [ ] Listar TUDO que vence nos proximos 7 dias
- [ ] Conferir tributos da semana (DAS, INSS, FGTS, ISS, ICMS)
- [ ] Agendar pagamentos no banco (ou DDA, ou autopagamento)
- [ ] Nenhum tributo correndo risco de atraso
- [ ] Folha de pagamento programada se for semana de pagamento

**Bloqueador critico**: tributo a vencer sem dinheiro em caixa -> resolver hoje (negociar com fornecedor / antecipar recebivel).

---

## 4. Caixa (5 min)

- [ ] Atualizar saldo de cada conta no fluxo de caixa
- [ ] Recalcular saldo final previsto do mes
- [ ] Saldo final previsto > zero ate fim do mes?
- [ ] Saldo final previsto > 1 mes de custo fixo?
- [ ] Projecao 90 dias atualizada

**Alerta**: se projecao mostra mes negativo nos proximos 3 meses, definir acao agora.

---

## 5. Indicadores rapidos (3 min)

Anotar 4 numeros:

```
Saldo total em caixa hoje:           R$ [valor]
Receita confirmada essa semana:      R$ [valor]
Saidas previstas essa semana:        R$ [valor]
Posicao liquida (recebivel - pagar): R$ [valor]
```

Comparar com semana passada:
- Caixa cresceu ou caiu?
- Receita ta no ritmo da meta do mes?
- Posicao liquida ta melhorando?

---

## 6. Acoes da semana (2 min)

Definir maximo 3 acoes financeiras pra semana:

| Acao | Responsavel | Prazo |
|---|---|---|
| [verbo + objeto + valor] | [nome] | [DD/MM] |
| | | |
| | | |

Exemplos:
- "Cobrar pessoalmente cliente X (R$ 8.500 atrasado)"
- "Cancelar 2 softwares ociosos (R$ 480/mes)"
- "Renegociar prazo com fornecedor Y de 30 pra 45 dias"

---

## 7. Alertas pra atencao especial

- [ ] Algum cliente grande com contrato terminando esse mes
- [ ] Algum mes da projecao 90d com saldo negativo
- [ ] Algum tributo trimestral chegando (IRPJ/CSLL Lucro Presumido)
- [ ] Decimo terceiro / ferias caindo nos proximos 60 dias
- [ ] Algum investimento planejado sem reserva

---

## 8. Encerramento (1 min)

- [ ] Salvar arquivos atualizados (fluxo de caixa, contas pagar/receber)
- [ ] Backup automatico funcionou (se aplicavel)
- [ ] Proxima revisao agendada (proxima segunda)
- [ ] Resumo pra socio enviado (se aplicavel): 4 numeros + 3 acoes

### Template do resumo pro socio (WhatsApp ou email)

```
*Relatorio financeiro semana [AAAA-MM-DD a AAAA-MM-DD]*

Caixa hoje: R$ [valor] ({{COMPORTAMENTO_SEMANAL}} vs semana passada)
Recebido na semana: R$ [valor]
A pagar nessa semana: R$ [valor]

3 pontos de atencao:
1. [item]
2. [item]
3. [item]

3 acoes que vou tomar:
1. [acao]
2. [acao]
3. [acao]
```

---

## Sinais de alerta vermelho (chamar contador / financeiro)

Qualquer um abaixo = ligar AGORA:

- Conta corrente negativa
- Tributo atrasado mais de 7 dias
- Folha em risco de nao pagar no dia
- Inadimplencia > 15% do total a receber
- Projecao 90d mostra saldo negativo
- Identificou fraude ou divergencia inexplicavel

---

## Frequencia

- **Diario** (2-3 min): conferir extrato bancario, marcar recebimentos confirmados
- **Semanal** (este checklist, 30 min): segunda-feira de manha
- **Mensal**: fechar DRE (ver `../dre/`) + apurar pro-labore (`pro-labore-distribuicao.md`)
- **Trimestral**: revisar custo fixo, renegociar contratos vencendo, planejar tributo trimestral
- **Anual**: revisar pro-labore, definir reserva de caixa, planejar investimento

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Checklist inicial - 8 secoes |
