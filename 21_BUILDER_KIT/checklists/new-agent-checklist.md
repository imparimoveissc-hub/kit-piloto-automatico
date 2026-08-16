# New Agent Checklist

> Aplica antes de declarar agente novo pronto.

## Identidade

- [ ] Nome em kebab-case unico no kit
- [ ] Papel descrito em 2-3 frases
- [ ] Quando usar listado com palavras-chave reais
- [ ] Tier definido (0/1/2/3) ou justificado ausencia

## Inputs/Outputs

- [ ] Inputs obrigatorios listados
- [ ] Inputs opcionais marcados
- [ ] Output contract verificavel (nao adjetivo)
- [ ] Workflow em passos numerados

## Carregamento

- [ ] Lista maximo 2 diretrizes (carga sob demanda)
- [ ] Nao referencia clientes reais
- [ ] Nao tem token/credencial

## Gate

- [ ] Gate definido (existente ou novo em `00_OS/gates.md`)
- [ ] Criterios de pass/fail claros

## Handoff

- [ ] Para qual agente envia o output
- [ ] O que o proximo agente precisa receber

## Regras / Anti-patterns

- [ ] 3+ regras explicitas
- [ ] 3+ anti-patterns

## Wrapper

- [ ] `.claude/agents/<nome>.md` criado
- [ ] Aponta pra arquivo correto

## Indices

- [ ] `00_INDEX.md` (camadas + rotas + arquivos-chave)
- [ ] `00_OS/router.md` (tabela)
- [ ] `00_OS/cos.md` (classificacao)
- [ ] `02_AGENTS/README.md` (tabela de agentes)

## Claude Desktop

- [ ] `22_CLAUDE_DESKTOP/knowledge-files.md` atualizado
- [ ] `22_CLAUDE_DESKTOP/commands-keywords.md` atualizado
- [ ] Se for crítico, considerar criar Project dedicado

## Teste

- [ ] Roda comando simulado e funciona
- [ ] Output esperado se materializa
- [ ] Gate se aplica corretamente

## Documentado

- [ ] Resumo do agente em `_DONO_PRODUTO/07_LOGS/decisions.md` (se for do dono)
