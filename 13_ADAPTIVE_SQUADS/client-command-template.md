# Client Command Template

Use para criar comandos especificos de cliente dentro de `squad-manifest.yaml`.

```yaml
- command: "*[atalho]"
  owner: "[agente]"
  objective: "[uma frase]"
  inputs:
    required: []
    optional: []
  output_contract: []
  gate: "[GATE]"
  safe_to_run_full_auto: true
  requires_confirmation_when: []
```

## Criterios

- Comando precisa reduzir friccao real.
- Comando nao pode esconder risco.
- Comando deve produzir output verificavel.
- Comando deve ser removido se parar de ser usado.

