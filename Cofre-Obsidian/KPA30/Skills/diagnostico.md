---
name: diagnostico
description: Diagnostico rapido da operacao de um cliente ou prospect
---

# /diagnostico — Diagnostico de Operacao

## Processo

### 1. Ler contexto
Leia `.claude/config.md` pra adaptar as perguntas ao segmento.

### 2. Coletar informacoes
Pergunte: "Vou fazer um diagnostico rapido. E pra um prospect (ferramenta de vendas) ou cliente atual (melhoria)?"

### 3. Fazer 5 perguntas

**Pra qualquer segmento:**
1. "Qual o principal servico/produto que oferece?"
2. "Quantos clientes atende hoje e qual o ticket medio?"
3. "Como consegue clientes novos? (indicacao, trafego, organico, outbound)"
4. "Qual a maior dificuldade da operacao hoje? (entrega, vendas, gestao, tempo)"
5. "O que ja tentou pra resolver e nao funcionou?"

### 4. Gerar diagnostico

```markdown
# Diagnostico — [Nome]
Data: [data]
Elaborado por: [empresa do config.md]

## Situacao Atual

| Aspecto | Status |
|---------|--------|
| Servico principal | [resposta] |
| Clientes ativos | [numero] |
| Ticket medio | R$ [valor] |
| Faturamento estimado | R$ [calculo] |
| Canal de aquisicao | [resposta] |
| Principal gargalo | [resposta] |

## Diagnostico

### Pontos fortes
- [ponto forte 1, baseado nas respostas]
- [ponto forte 2]

### Gargalos identificados
1. **[gargalo 1]:** [explicacao + impacto no negocio]
2. **[gargalo 2]:** [explicacao + impacto]
3. **[gargalo 3]:** [explicacao + impacto]

### Oportunidades
1. **[oportunidade 1]:** [o que pode ser feito + resultado esperado]
2. **[oportunidade 2]:** [o que pode ser feito + resultado esperado]

## Recomendacao

### Prioridade 1 (resolver em 30 dias)
[acao principal que destrava o crescimento]

### Prioridade 2 (resolver em 60 dias)
[acao secundaria]

### Prioridade 3 (resolver em 90 dias)
[acao de escala]

## Projecao

| Cenario | Faturamento | Crescimento |
|---------|------------|-------------|
| Atual (sem mudanca) | R$ [valor] | 0% |
| Com prioridade 1 | R$ [valor] | +[X]% |
| Com todas as acoes | R$ [valor] | +[X]% |

---
*Este diagnostico e uma analise inicial. Resultados reais dependem de implementacao.*
```

### 5. Se for prospect
Adicione ao final:

```markdown
## Proximos Passos
Posso te ajudar a resolver esses gargalos. Quer que eu monte uma proposta?

[Empresa] oferece: [servicos do config.md]
```

### 6. Salvar
Salve em `clientes/[nome]/diagnostico.md`

### 7. Proximo passo
Se prospect: "Diagnostico pronto. Quer gerar a proposta? (/proposta)"
Se cliente: "Diagnostico pronto. Quer criar um plano de acao? (/criar)"
