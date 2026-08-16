# Adaptive Loop

## Objetivo

Fazer o sistema aprender a operar cada cliente sem carregar historico inteiro e sem virar prompt gigante.

## Gatilhos de revisao

Revisar `squad-manifest.yaml` quando:

- concluir uma entrega relevante;
- falhar duas vezes no mesmo gate;
- surgir novo canal, oferta, nicho ou promessa;
- usuario corrigir o mesmo comportamento do agente duas vezes;
- uma conversa revelar SLA, objeção, prova ou restricao nova;
- o CoS perceber que esta perguntando algo que poderia estar no contexto.

## O que atualizar

```yaml
client_learning:
  repeated_requests:
  preferred_outputs:
  banned_phrases:
  approved_claims:
  unresolved_gaps:
  active_commands:
  active_squad:
  next_review_trigger:
```

## Economia de contexto

- Manifest deve ter no maximo 120 linhas.
- Detalhe longo vai para `07_LOGS/context-cache.md` ou arquivo do cliente.
- CoS carrega manifest + current context, nao historico bruto.

## Politica de mudanca

Mudancas reversiveis entram direto e sao registradas. Mudancas que alteram publicacao, gasto, automacao real ou promessa publica exigem confirmacao.

## Output de revisao

```yaml
manifest_updated: true | false
reason:
added_commands:
removed_commands:
new_constraints:
next_task:
```

