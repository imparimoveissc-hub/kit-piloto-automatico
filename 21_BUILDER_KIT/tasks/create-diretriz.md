# Task — Create Diretriz

```yaml
owner: forge
model_profile: research-balanced
objective: Criar diretriz nova (conhecimento sob demanda) seguindo padrao V30.
inputs:
  required:
    - topico
    - quando carregar
    - 3-7 principios
    - anti-patterns
  optional:
    - exemplos
output_contract:
  - arquivo `04_DIRETRIZES/<topico>.md`
  - linha em `04_DIRETRIZES/README.md`
  - linha em `00_OS/knowledge-loader.md`
  - linha em `22_CLAUDE_DESKTOP/knowledge-files.md`
acceptance_gate: GATE-INTAKE
budget: medio
```

## Action items

1. Pre-flight: diretriz parecida existe? Pode estender?
2. Coletar inputs.
3. Aplicar `diretriz-scaffold.md`.
4. Criar arquivo.
5. Atualizar indices + knowledge-loader.
