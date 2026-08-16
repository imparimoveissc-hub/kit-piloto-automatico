---
name: relatorio
description: Monta relatorio de performance com dados e analise
---

# /relatorio — Relatorio de Performance

## Processo

### 1. Ler contexto
Leia `.claude/config.md` pra adaptar metricas ao segmento.

### 2. Coletar informacoes
Pergunte:
- "Pra qual cliente?"
- "Qual o periodo? (semanal, mensal, campanha especifica)"
- "Cole os dados ou descreva os numeros."

### 3. Metricas por segmento

**Trafego pago:**
- Investimento, impressoes, cliques, CTR, CPC, leads, CPL, vendas, CPA, ROAS, frequencia

**Social media:**
- Seguidores (crescimento), alcance, impressoes, engajamento, saves, shares, cliques no link, DMs

**Designer:**
- Pecas entregues, pecas aprovadas de primeira, tempo medio por peca, revisoes

**Videomaker:**
- Videos entregues, views, retencao media, engajamento, tempo de producao

**Advocacia:**
- Processos ativos, movimentacoes, prazos cumpridos, audiencias, acordos

**B2B:**
- Leads gerados, SQLs, reunioes, propostas, fechamentos, ticket medio, ciclo de venda, pipeline

**Clinica:**
- Agendamentos, consultas realizadas, no-shows, procedimentos, faturamento, origem dos pacientes

### 4. Gerar relatorio

```markdown
# Relatorio [Periodo] — [Cliente]
Data: [data]
Elaborado por: [empresa do config.md]

## Resumo Executivo
[3-4 linhas com os destaques do periodo]

## Metricas Principais

| Metrica | Periodo atual | Periodo anterior | Variacao |
|---------|--------------|-----------------|----------|
| [metrica 1] | [valor] | [valor] | [+/- %] |
| [metrica 2] | [valor] | [valor] | [+/- %] |

## Analise

### O que funcionou
- [ponto positivo 1]
- [ponto positivo 2]

### O que precisa melhorar
- [ponto de atencao 1]
- [ponto de atencao 2]

## Recomendacoes

| Acao | Prioridade | Impacto esperado |
|------|-----------|-----------------|
| [acao 1] | Alta | [resultado] |
| [acao 2] | Media | [resultado] |

## Plano pro Proximo Periodo
1. [acao 1]
2. [acao 2]
3. [acao 3]
```

### 5. Salvar
```bash
mkdir -p clientes/[nome-cliente]/relatorios
```
Salve em `clientes/[nome]/relatorios/[periodo].md`

### 6. Proximo passo
Pergunte: "Relatorio pronto. Quer formatar pra entrega? (/entregar)"
