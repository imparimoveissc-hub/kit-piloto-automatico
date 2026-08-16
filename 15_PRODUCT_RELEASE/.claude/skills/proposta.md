---
name: proposta
description: Gera proposta comercial profissional
---

# /proposta — Proposta Comercial

## Processo

### 1. Ler contexto
Leia `.claude/config.md` pra pegar servicos e tom de voz.

### 2. Coletar dados
Pergunte:
- "Pra quem e a proposta? (nome e empresa)"
- "Qual servico vai oferecer?"
- "Qual o escopo/entregaveis?"
- "Qual a faixa de investimento?"

### 3. Gerar proposta

```markdown
# Proposta Comercial

**Para:** [nome do prospect]
**De:** [empresa do config.md]
**Data:** [data atual]

---

## Sobre nos
[2-3 linhas sobre a empresa, baseado no config.md]

## Diagnostico
[Resumo do problema/oportunidade do prospect — baseado nas informacoes coletadas]

## Solucao proposta
[O que voce vai fazer pra resolver]

## Escopo e entregaveis

| # | Entregavel | Descricao |
|---|-----------|-----------|
| 1 | [entregavel] | [o que inclui] |
| 2 | [entregavel] | [o que inclui] |
| 3 | [entregavel] | [o que inclui] |

## Opcoes de investimento

### Opcao 1 — Essencial
- [escopo reduzido]
- **Investimento:** R$ [valor]/mes

### Opcao 2 — Profissional (Recomendada)
- [escopo completo]
- **Investimento:** R$ [valor]/mes

### Opcao 3 — Premium
- [escopo completo + extras]
- **Investimento:** R$ [valor]/mes

## Cronograma

| Fase | Atividade | Prazo |
|------|----------|-------|
| Semana 1 | Onboarding e setup | [data] |
| Semana 2-4 | Implementacao | [data] |
| Mensal | Gestao e otimizacao | Continuo |

## Condicoes
- Pagamento: [forma]
- Contrato minimo: [periodo]
- Prazo pra aceite: [X] dias

## Proximos passos
1. Aceite desta proposta
2. Assinatura de contrato
3. Kickoff em [prazo]

---
[empresa] | [contato]
```

### 4. Salvar
Salve em `clientes/[nome]/proposta.md`

### 5. Proximo passo
Pergunte: "Proposta pronta. Quer gerar o follow-up pra enviar junto? (/follow-up)"
