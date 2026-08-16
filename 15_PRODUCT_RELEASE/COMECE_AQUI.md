# Comece Aqui

## 1 comando pra instalar tudo

Dentro do Claude (Desktop ou Code), digite:

```text
instalar kpa30
```

(no Code voce tambem pode digitar `/instalar-kpa30`)

## O que vai acontecer

O wizard guia voce em 7 etapas, em torno de 15-20 minutos:

1. Confere dependencias do seu computador.
2. Configura o arquivo `.env`.
3. Ativa MCPs essenciais (Composio Rube, WhatsApp, Filesystem, Playwright).
4. Configura Meta Ads CLI (se voce roda trafego pago — opcional).
5. Cria Projects no Claude Desktop (se voce usa o app).
6. Te conhece em 6 perguntas (empresa, nicho, produto, publico, canal, gargalo).
7. Gera sua primeira tarefa util ja adaptada ao seu negocio.

Resultado: kit configurado, primeira entrega pronta, proximos comandos sugeridos.

## Antes de comecar

1. Confira que esta pasta esta em um local facil (Desktop ou Documents).
2. Abra o Claude:
   - **App Desktop:** se for primeira vez, crie Project conforme `22_CLAUDE_DESKTOP/setup-project.md`. Mais simples: depois de criar o Project, digite "instalar kpa30".
   - **Claude Code (terminal):** navegue ate esta pasta e rode `claude`.
3. Digite o comando.

## Depois de instalar

Use os comandos do dia a dia:

| Comando | Funcao |
|---|---|
| `instalar kpa30` ou `/instalar-kpa30` | Instalacao inicial (1 vez por maquina) |
| `primeira tarefa` ou `/primeira-tarefa` | Gera nova entrega util |
| `briefing` ou `/briefing` | Cria briefing de cliente novo |
| `whatsapp` ou `/whatsapp-system` | Monta fluxo WhatsApp (draft) |
| `automatizar` ou `/automatizar-processo` | Documenta automacao |
| `forge` ou `/forge` | Cria agente/skill novo |
| `mcp setup` ou `/mcp-setup` | Adiciona MCPs depois |

## Estrutura da pasta

- `15_PRODUCT_RELEASE/` — release publica simples (uso diario)
- `00_OS/` — motor (CoS, gates, router)
- `02_AGENTS/` — especialistas reduzidos
- `04_DIRETRIZES/` — conhecimento sob demanda
- `20_MCP_SETUP/` — conectores externos
- `21_BUILDER_KIT/` — Forge (criar agentes novos)
- `22_CLAUDE_DESKTOP/` — adaptacao pro app

## Se algo der errado

1. Cole o erro no chat — o instalador te orienta como corrigir.
2. Veja `docs/troubleshooting.md` pra problemas comuns.
3. Documentacao completa em `00_INDEX.md` da raiz.

## Se voce nao sabe qual e seu nicho

Sem problema. O wizard classifica seu negocio em 1 das 8 familias operacionais automatica:

1. Servico local
2. Profissional liberal
3. B2B consultivo
4. Ecommerce
5. Infoproduto
6. Agencia / servico digital
7. Clinica / saude
8. Juridico / regulado

Tudo isso e feito pelo `instalar kpa30`.
