# Cache Policy V30

## Objetivo

Manter memoria util sem carregar historico demais.

## Tipos de memoria

| Tipo | Arquivo | TTL | Uso |
|---|---|---|---|
| Contexto ativo | `05_WORKSPACE/current-context.md` | ate mudar projeto | Sempre no boot |
| Ledger | `07_LOGS/task-ledger.md` | permanente | Controle de tasks |
| Decisoes | `07_LOGS/decisions.md` | permanente | Premissas importantes |
| Cache operacional | `07_LOGS/context-cache.md` | 7 a 30 dias | Resumos reutilizaveis |
| Output final | `06_OUTPUTS/` | permanente | Entrega, nao contexto ativo |

## Regras de TTL

| Conteudo | TTL sugerido |
|---|---:|
| Proxima task | ate concluir |
| Dados de campanha em leitura | 7 dias |
| VOC ouro | 30 dias ou ate mudar publico |
| Promessa/mecanismo | ate mudar oferta |
| Preferencia visual | 30 dias |
| Rascunho rejeitado | 48 horas |
| Log de tentativa sem aprendizado | descartar |

## Compactacao

Quando um arquivo de contexto passar de 120 linhas:

1. Criar resumo de ate 40 linhas.
2. Preservar decisoes, provas, gaps e proxima task.
3. Mover detalhe para cache ou projeto.
4. Atualizar `current-context.md`.

## Regra de ouro

Historico so entra no prompt se ajudar a proxima decisao.
