---
tipo: brain
modulo: Contratos
status: ativo
criticidade: alta
atualizado: 2026-07-26
---

# 📄 Contratos — Locação

> [!info] Plugin ativo: imobiliario-juridico
> Gera, revisa e acompanha contratos conforme a Lei 8.245/91 (Lei do Inquilinato).

## O que o sistema faz

- **Gera** contratos de locação com todos os dados corretos
- **Revisa** contratos recebidos (identifica cláusulas problemáticas)
- **Acompanha** datas de reajuste e vencimento de vigência
- **Alerta** antes dos prazos fecharem

## Reajuste anual

> [!warning] Atenção ao calendário
> O Claude monitora os contratos e avisa antes das datas de reajuste chegarem. Se o alerta parou de chegar, a task `vigia-reajustes-semanal` pode estar desativada — diga "reativar vigia de reajustes".

## Como acionar

| O que você quer | O que dizer |
|-----------------|-------------|
| Gerar contrato novo | "gerar contrato de locação" |
| Revisar contrato recebido | "revisar contrato" + cole o texto |
| Ver o que reajusta em breve | "quais contratos reajustam agora" |
| Ver o que vence em breve | "o que vence esse mês" |
| Adicionar contrato ao acompanhamento | "adicionar contrato ao acompanhamento" |

## Fluxo de geração

```
Você informa: locatário, imóvel, valor, prazo, índice
       ↓
Claude gera o contrato completo
       ↓
Claude revisa e valida cláusulas
       ↓
Documento salvo em 06_OUTPUTS/
       ↓
Contrato entra no acompanhamento automático de reajuste
```

## Índice de reajuste

O sistema usa o índice definido em cada contrato (IGPM, IPCA, etc.).
O reajuste é calculado e alertado automaticamente pela vigia semanal.

## Ver também

- [[Jurídico Imobiliário (plugin)]] — spec completa do plugin
- [[gerar-contrato-locacao]] — skill de geração
- [[00 - Índice Brain]] — voltar ao índice
