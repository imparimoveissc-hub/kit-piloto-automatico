# Inicio Rapido — Kit Piloto Automatico V30

> 1 comando pra instalar tudo.

## Passo 1 — Baixar e descompactar

Voce ja fez isso. Esta pasta `Kit-Piloto-Automatico-V30/` na sua maquina.

**Recomendado:** mover pra `Desktop/` ou `Documents/` (nao deixa em Downloads ou pasta temporaria).

## Passo 2 — Abrir no Claude

Voce tem 2 opcoes:

### Opcao A — Claude Desktop (app)

1. Abre o app Claude Desktop.
2. Sidebar esquerda: clica em **+ New Project**.
3. Nome: `Kit Piloto Automatico V30`
4. Em **Project Knowledge**:
   - Cola o conteudo de `22_CLAUDE_DESKTOP/cos-desktop-system-prompt.md`
   - Faz upload dos arquivos listados em `22_CLAUDE_DESKTOP/knowledge-files.md` (Project 1, Tier 1)
5. Salva e abre o Project.

### Opcao B — Claude Code (terminal)

```bash
# Mac/Linux:
cd ~/Desktop/Kit-Piloto-Automatico-V30
claude

# Windows (PowerShell):
cd $env:USERPROFILE\Desktop\Kit-Piloto-Automatico-V30
claude
```

## Passo 3 — Comando unico

Dentro do Claude (Desktop ou Code), digite:

```text
instalar kpa30
```

OU

```text
/instalar-kpa30
```

(o `/` so funciona no Code; no Desktop a palavra-chave funciona).

## O que o instalador faz

Wizard guiado em 7 etapas (~15-20 min):

1. **Confere dependencias** do seu computador (Node, Git).
2. **Configura `.env`** (sem te pedir token).
3. **Ativa MCPs essenciais** (Composio Rube, WhatsApp, Filesystem, Playwright).
4. **Configura Meta Ads CLI** (so se voce roda trafego pago).
5. **Cria Projects do Desktop** (se voce usa o app).
6. **Te conhece** (6 perguntas: empresa, nicho, produto, publico, canal, gargalo).
7. **Gera sua primeira tarefa util** ja adaptada ao seu negocio.

No final voce tem:
- Kit configurado pro seu segmento.
- Primeira entrega pronta pra revisar.
- Proximos comandos sugeridos.

## Em caso de erro

Se algo travar:

1. Cola o erro no chat — eu te ajudo.
2. Se for grave, abre issue em <https://github.com/seu-repo> (se aplicavel).
3. Documentacao completa em `00_INDEX.md`.

## Apos instalar

Use os comandos do dia a dia:

| Comando | O que faz |
|---|---|
| `/primeira-tarefa` ou "primeira tarefa" | Gera entrega util |
| `/briefing` ou "fazer briefing" | Briefing de cliente novo |
| `/whatsapp-system` ou "whatsapp" | Monta fluxo WhatsApp (draft) |
| `/automatizar-processo` ou "automatizar" | Documenta automacao |
| `/forge` ou "forge" | Cria agente/skill novo |
| `/mcp-setup` ou "mcp setup" | Adiciona mais MCPs |

## Estrutura da pasta

- `15_PRODUCT_RELEASE/` — release publica simples (uso diario)
- `00_OS/` — motor (CoS, gates, router)
- `02_AGENTS/` — especialistas
- `04_DIRETRIZES/` — conhecimento sob demanda
- `20_MCP_SETUP/` — conectores externos
- `21_BUILDER_KIT/` — Forge (criar agentes novos)
- `22_CLAUDE_DESKTOP/` — adaptacao pro app

Detalhes em `00_INDEX.md` e `README.md`.

---

**Quando estiver pronto:** abre o Claude e digita `instalar kpa30`.
