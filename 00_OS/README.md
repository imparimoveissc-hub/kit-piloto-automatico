# OS V30

O OS V30 existe para reduzir custo de contexto e aumentar confiabilidade.

## Componentes

- `cos.md` - entry point e gestor de tasks.
- `bootstrap.md` - sequencia de inicializacao.
- `router.md` - tabela de roteamento por intencao.
- `model-router.yaml` - slots de modelos por etapa e politica de upgrade/downgrade.
- `context-economy.md` - budgets de tokens e regras de lazy loading.
- `cache-policy.md` - TTL e compactacao de contexto.
- `access-preflight.md` - validacao inicial de pastas, acessos, ferramentas e limites.
- `proactivity-policy.md` - politica de full-auto prudente.
- `clients-map.yaml` - mapa global sem segredos para clientes/contas.
- `knowledge-loader.md` - quando carregar cada diretriz.
- `task-manager.md` - lifecycle de tarefas, fila e ledger.
- `gates.md` - validacoes bloqueantes.
- `gate-matrix.md` - severidade e decisao de rework.
- `handoffs.md` - contratos entre especialistas.
- `commands/` - comandos operacionais.

## Filosofia do V30

V30 troca "muitos agentes e muitos arquivos" por "poucos agentes, contracts pequenos e escalada sob demanda". Cada task tem contrato de entrada/saida, budget de contexto e gate de qualidade.

Para operacao com usuario final, o preflight deve concentrar acessos no inicio. O sistema deve agir mais, perguntar menos e bloquear apenas quando houver risco real: credencial, gasto, publicacao, disparo ou acao irreversivel.

Para conectar ferramentas externas (Drive, WhatsApp, Slack, Meta, Composio, etc.), use `20_MCP_SETUP/`.

Para criar agentes, skills, tasks ou diretrizes novas, use `21_BUILDER_KIT/` (Forge agent).

## Regra de ouro

O CoS deve ser barato. Se o CoS esta lendo framework, escrevendo copy ou debatendo estrategia em profundidade, ele saiu da funcao dele.
