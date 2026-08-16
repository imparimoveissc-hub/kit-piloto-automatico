# Task — Create Skill

```yaml
owner: forge
model_profile: research-balanced
objective: Criar skill nova seguindo padrao V30.
inputs:
  required:
    - nome
    - triggers (palavras-chave)
    - inputs minimos
    - workflow em 3-7 passos
  optional:
    - priority
    - pathPatterns
output_contract:
  - arquivo `XX_STACK/skills/<nome>/SKILL.md`
  - linha em `XX_STACK/README.md`
  - linha em `00_INDEX.md` (se relevante)
  - linha em `22_CLAUDE_DESKTOP/knowledge-files.md`
acceptance_gate: GATE-INTAKE
budget: baixo-medio
```

## Action items

1. Pre-flight: skill similar existe?
2. Coletar inputs.
3. Aplicar `skill-scaffold.md`.
4. Criar arquivo.
5. Atualizar indices.
