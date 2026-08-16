# Setup do Project no Claude Desktop

> Passo a passo pro mentorado configurar o Project "Kit Piloto Automatico V30 - CoS" no Claude Desktop.

## Pre-requisito

- Claude Desktop instalado (https://claude.ai/download)
- Conta Anthropic com plano Pro ou Team (Free nao tem Projects)
- Pasta do kit extraida em local conhecido (Desktop ou Documentos)

## Passo 1 — Criar Project

1. Abra Claude Desktop.
2. Na sidebar esquerda, clique em **"+ New Project"** (ou icone de pasta com `+`).
3. Nome: `Kit Piloto Automatico V30 - CoS`
4. Descricao (opcional): `Operacao geral do kit. Setup de nicho, primeira tarefa, roteamento.`
5. Clique em **Create**.

## Passo 2 — Adicionar System Prompt

1. Dentro do Project, abra **Project Knowledge** (ou aba "Knowledge" / "Instructions").
2. Cole o conteudo de `cos-desktop-system-prompt.md` no campo "Custom instructions for this project".
3. Salve.

## Passo 3 — Upload de Knowledge Files

1. Ainda em **Project Knowledge**, clique em **"+ Add files"** ou arraste arquivos.
2. Faca upload da lista em `knowledge-files.md` (essencial pro Project funcionar).
3. Espere processar (Claude indexa).

**Limite atual:** 20 arquivos OU 30MB total. Use a lista priorizada.

## Passo 4 — Configurar MCPs (opcional mas recomendado)

Edite o arquivo de config do Claude Desktop:

### macOS

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows

```
%APPDATA%\Claude\claude_desktop_config.json
```

### Linux

```
~/.config/Claude/claude_desktop_config.json
```

Cole o template de `claude-desktop-config.json` adaptando ao seu setup. Reinicie o app.

## Passo 5 — Testar o Project

Dentro do Project, mande:

```text
Oi, sou novo aqui. Como funciona o kit V30?
```

Espera: CoS responde resumindo o caminho `preflight acessos` -> `setup de nicho` -> `primeira tarefa`.

Depois manda:

```text
preflight acessos
```

Espera: CoS conduz o preflight com perguntas guiadas.

## Passo 6 — Criar 2 Projects adicionais

Repita Passos 1-3 pra:

### Project 2: `Kit V30 - Trafego DR`

- System prompt: `cos-desktop-system-prompt.md` + diretrizes `11_TRAFFIC_STACK/` (PLAYBOOK + skill direct-response-br)
- Knowledge: arquivos da Traffic Stack

### Project 3: `Kit V30 - WhatsApp + Cowork`

- System prompt: `cos-desktop-system-prompt.md` + diretrizes `12_WHATSAPP_STACK/` + `04_DIRETRIZES/whatsapp-diretrizes.md`
- Knowledge: arquivos da WhatsApp Stack

Detalhes em `projects-recommended.md`.

## Manutencao

### Quando atualizar Project

- Kit V30 recebe update (forge cria agente novo, diretriz nova).
- Mentorado adicionou cliente novo que vale virar context.
- Mentorado mudou foco operacional.

### Como atualizar

1. Volte em **Project Knowledge**.
2. **Remova** arquivos antigos modificados.
3. **Re-upload** versoes novas.
4. Atualize system prompt se mudou.

## Troubleshooting

| Problema | Solucao |
|---|---|
| Claude nao acessa knowledge | Aguardar processamento (1-2 min) |
| Knowledge muito grande | Priorizar essencial (ver `knowledge-files.md`) |
| MCPs nao funcionam | Reiniciar app Desktop apos editar config |
| Project responde generico | System prompt nao foi salvo OU knowledge nao processou |
| Comandos `/forge` nao funcionam | Use palavra-chave: "forge: criar agente novo" |
