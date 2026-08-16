# Command - preflight-acessos

## Objetivo

Validar ambiente, pastas, acessos e limites de automacao antes de iniciar trabalho real.

## Passos

1. Ler `00_OS/access-preflight.md`.
2. Identificar cliente/projeto alvo.
3. Verificar se existe context pack do cliente.
4. Listar acessos obrigatorios para a rota atual.
5. Separar leitura, escrita, install, login, publicacao e acao destrutiva.
6. Criar checklist do que esta pronto e do que bloqueia.
7. Registrar premissas relevantes em `07_LOGS/decisions.md`.

## Saida

```yaml
preflight_status:
ready_now:
missing:
needs_user_action:
blocked_by:
next_task:
```

