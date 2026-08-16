# 15_PRODUCT_RELEASE

Camada publica do V30. Esta pasta e o formato que o aluno final deve entender.

O motor interno continua em `00_OS/`, `11_TRAFFIC_STACK/`, `12_WHATSAPP_STACK/` e `13_ADAPTIVE_SQUADS/`. A release publica deve esconder essa complexidade e expor apenas:

- onde comecar;
- como instalar;
- qual comando rodar;
- quais prompts/templates existem;
- como adaptar para o segmento do usuario;
- como operar WhatsApp com seguranca;
- como seguir o curso sem se perder;
- como validar que tudo funcionou.

## Contrato da release

Antes de publicar/zipar, esta pasta precisa conter:

- [ ] `COMECE_AQUI.md` validado para usuario leigo.
- [ ] `INSTALACAO.md` com Windows e Mac.
- [ ] `PRIMEIRA_TAREFA.md` com teste em menos de 15 minutos.
- [x] `.claude/agents/` com agentes publicos ou wrappers simples.
- [x] `.claude/commands/` com comandos principais.
- [x] `.claude/skills/` com 10 skills publicas legadas.
- [x] `prompts/` com 50 prompts oficiais.
- [x] `templates/` com 17 templates por segmento.
- [x] `nichos/` com advocacia, B2B e clinicas no minimo.
- [x] `whatsapp/` com fluxos operacionais.
- [x] `cowork/` com documentos importaveis/rodaveis em modo draft.
- [x] `automacoes/` com entrada publica para automatizar processos.
- [x] `curso/` com trilha oficial, mapa de aulas, tarefas praticas e checklist do aluno.
- [x] `docs/` com FAQ, glossario, troubleshooting e referencia rapida.
- [x] `exemplos/` com outputs preenchidos e familias operacionais.

## Fluxo recomendado

Interface visual:

```text
index.html
```

Para quem esta seguindo as aulas:

```text
curso/README.md
-> curso/trilha-oficial.md
-> curso/tarefas/
```

Para quem quer operar direto:

```text
/preflight-acessos
-> /setup-nicho
-> /primeira-tarefa
-> /whatsapp-system ou /automatizar-processo, conforme necessidade
```

## Estado atual

Smoke test de arquivos: passou com concerns em `17_RELEASE_QA/smoke-test-results.md`.

Pendente antes de empacotar para venda: teste conversacional no Claude Code real.

## Principio

O aluno nao compra arquitetura. Ele compra resultado. A release publica deve parecer pequena, guiada e copiavel, mesmo quando o motor interno for sofisticado.
