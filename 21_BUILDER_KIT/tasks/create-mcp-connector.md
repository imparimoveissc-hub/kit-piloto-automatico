# Task — Create MCP Connector

```yaml
owner: forge
model_profile: router-cheap
objective: Documentar conector MCP novo seguindo padrao V30 + atualizar setup.
inputs:
  required:
    - nome do MCP
    - comando de install
    - tools principais (3+)
    - casos de uso (3+)
    - token policy
  optional:
    - alternativa via Composio Rube
output_contract:
  - arquivo `20_MCP_SETUP/connectors/<nome>.md`
  - linha em `20_MCP_SETUP/README.md` (tabela de tiers)
  - linha em `20_MCP_SETUP/recommended-stack.md`
  - linha em `20_MCP_SETUP/commands/mcp-setup.md` (se for Tier 1)
  - linha em `22_CLAUDE_DESKTOP/claude-desktop-config.json` (template MCP)
acceptance_gate: GATE-INTAKE
budget: baixo-medio
```

## Action items

1. Pre-flight: ja existe via Rube? Vale criar nativo?
2. Coletar inputs.
3. Aplicar `mcp-connector-scaffold.md`.
4. Criar arquivo.
5. Atualizar todos indices listados.
6. Adicionar template no claude_desktop_config.json.
