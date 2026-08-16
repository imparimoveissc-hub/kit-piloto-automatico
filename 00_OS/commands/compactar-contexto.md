# Command - compactar-contexto

## Objetivo

Reduzir custo de contexto sem perder estado operacional.

## Passos

1. Ler outputs recentes e ledger.
2. Extrair apenas decisoes, premissas, provas, gaps e proxima task.
3. Atualizar `05_WORKSPACE/current-context.md`.
4. Mover detalhes para `07_LOGS/context-cache.md` com TTL.
5. Remover do contexto ativo informacoes que nao afetam a proxima task.

## Saida

```yaml
current_context_updated: true
cache_entries_added:
discarded_context:
next_task:
```
