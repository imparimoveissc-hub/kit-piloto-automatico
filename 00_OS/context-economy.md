# Economia de Contexto

## Regra central

Contexto e custo. So carregue o que muda a decisao ou melhora diretamente o output.

## Budgets por papel

| Papel | Budget alvo | Pode carregar |
|---|---:|---|
| CoS | 800 tokens | indice, ledger, task atual, context pack |
| Researcher | 4.000 tokens | task + fontes + diretriz de VOC |
| Strategist | 5.000 tokens | briefing curto + VOC ouro + diretriz de estrategia |
| Copy Director | 6.000 tokens | briefing + mecanismo + voz + copy-goat-lite |
| Production Lead | 4.000 tokens | copy aprovada + direcao visual + specs |
| Traffic Analyst | 4.000 tokens | oferta + assets + metricas |
| WhatsApp Stack | 5.000 tokens | contexto + oferta + restricoes + whatsapp-diretrizes |
| Adaptive Squads | 1.500 tokens | manifest + ledger + contexto ativo |
| Product Hardening | 5.000 tokens | LP + promessa + entrega + product-hardening |
| QA Editor | 3.000 tokens | output + gate + contexto minimo |

## Context Pack

Todo projeto ativo deve ter um resumo curto em `05_WORKSPACE/current-context.md`:

```yaml
projeto:
objetivo:
publico:
oferta:
mecanismo:
tom:
provas_confirmadas:
restricoes:
status:
proxima_task:
arquivos_relevantes:
squad_manifest:
```

Se esse arquivo existe, leia ele antes de qualquer historico. So abra arquivos antigos quando o context pack apontar gap.

Ver `00_OS/cache-policy.md` para TTL e compactacao.

## Loading em cascata

1. Ler task.
2. Ler context pack.
3. Ler gate.
4. Ler uma diretriz primaria.
5. Produzir.
6. Se falhar no gate, carregar diretriz secundaria ou subir modelo.

## Anti-patterns

- Carregar todos os agentes "para entender o sistema".
- Carregar toda a pasta de diretrizes antes de escrever.
- Reabrir historico completo em toda task.
- Usar modelo caro para triagem.
- Fazer output longo quando o handoff precisa ser curto.
- Usar compatibilidade V29 como desculpa para carregar a pasta antiga inteira.

## Handoff curto

Todo especialista termina com:

- output produzido;
- premissas usadas;
- gaps marcados;
- gate aplicado;
- proxima dependencia;
- arquivos gerados ou alterados.

Maximo 10 bullets.
