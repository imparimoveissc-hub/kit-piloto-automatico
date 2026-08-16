# Instalacao

## Requisitos

- Computador Windows 10+, macOS 12+ ou Linux.
- Conta Anthropic com plano Pro/Team ativo.
- Claude Desktop (app) OU Claude Code (terminal).

## Passo 1 — Extrair a pasta

Coloque a pasta `Kit-Piloto-Automatico-V30/` em local facil (Desktop ou Documents). Evita usar Downloads ou pasta temporaria.

## Passo 2 — Abrir o Claude

### Se vai usar Claude Desktop (recomendado pra leigo)

1. Abra o app.
2. Sidebar esquerda: clique em **+ New Project**.
3. Nome: `KPA Hub`
4. Em **Project Knowledge**:
   - Cole conteudo de `22_CLAUDE_DESKTOP/cos-desktop-system-prompt.md` em "Custom instructions"
   - Faca upload dos arquivos listados em `22_CLAUDE_DESKTOP/knowledge-files.md` (Project 1, Tier 1 — 10 arquivos)
5. Salve.

### Se vai usar Claude Code (terminal)

```bash
# Mac/Linux:
cd ~/Desktop/Kit-Piloto-Automatico-V30
claude

# Windows (PowerShell):
cd $env:USERPROFILE\Desktop\Kit-Piloto-Automatico-V30
claude
```

## Passo 3 — Comando unico

Dentro do Claude:

```text
instalar kpa30
```

O wizard cuida do resto:
- Confere dependencias do seu computador.
- Configura `.env` local.
- Ativa MCPs essenciais.
- Configura Meta Ads CLI se voce usar.
- Te conhece (6 perguntas).
- Gera sua primeira tarefa.

Tempo: ~15-20 minutos.

## Observacao

Instalacoes especificas (Meta CLI, MCPs avancados, automacao WhatsApp) entram conforme a tarefa exigir. O wizard so ativa o que voce precisa.

## Apos a instalacao

Use o comando do dia a dia conforme `COMECE_AQUI.md`.

## Reinstalacao

Se precisar refazer (ex: novo computador), basta rodar `instalar kpa30` de novo. O wizard detecta o que ja existe e pula etapas.
