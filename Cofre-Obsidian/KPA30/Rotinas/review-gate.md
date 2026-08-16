# Command - review-gate

## Objetivo

Validar uma entrega contra o gate certo.

## Passos

1. Identificar tipo de entrega.
2. Escolher gate em `00_OS/gates.md`.
3. Se gate for bloqueante, usar `reviewer-frontier`.
4. Aplicar matriz em `00_OS/gate-matrix.md`.
5. Devolver verdict, score, issues e fixes.
6. Atualizar ledger para `done`, `concerns` ou `rework`.

## Saida

```yaml
verdict:
score:
blocked_next_step:
specific_issues:
concrete_fixes:
next_status:
```
