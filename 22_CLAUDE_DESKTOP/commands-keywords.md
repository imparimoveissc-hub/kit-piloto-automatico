# Commands -> Keywords Mapping

> No Claude Code voce digita `/comando`. No Claude Desktop voce digita **palavra-chave** que o system prompt do CoS reconhece.

## Comandos principais

| Claude Code (`/`) | Claude Desktop (palavras-chave) | O que faz |
|---|---|---|
| `/instalar-kpa30` | "instalar kpa30", "instalar kit", "primeira vez", "comecar a usar o kit" | **Wizard unico de instalacao** — 1 vez por maquina, cobre tudo |
| `/start-here` | "comecar", "por onde comeco", "novo aqui" | Setup legacy (substituido por instalar-kpa30) |
| `/preflight-acessos` | "preflight", "preflight acessos", "liberar acessos" | Coleta acessos no inicio |
| `/setup-nicho` | "setup nicho", "configurar negocio", "qual e meu nicho" | Classifica familia operacional |
| `/primeira-tarefa` | "primeira tarefa", "primeira entrega", "comecar a entregar" | Gera entrega util em <15min |
| `/briefing` | "briefing", "fazer briefing", "organizar cliente novo" | Briefing estruturado |
| `/criar` | "criar copy", "fazer post", "gerar email", "fazer ad" | Criacao de conteudo |
| `/revisar` | "revisar", "checar texto", "feedback de copy" | Revisao com checklist |
| `/entregar` | "entregar", "empacotar entrega", "mensagem de entrega" | Pacote final |
| `/relatorio` | "relatorio", "fazer report", "report mensal" | Relatorio de performance |
| `/proposta` | "proposta", "proposta comercial" | Proposta pra prospect |
| `/onboarding` | "onboarding", "onboardar cliente novo" | Onboarding de cliente |
| `/follow-up` | "follow up", "retomar lead", "cobrar resposta" | Mensagens follow-up |
| `/diagnostico` | "diagnostico", "analisar operacao" | Diagnostico da operacao |
| `/whatsapp-system` | "whatsapp", "criar fluxo whatsapp", "cowork" | WhatsApp Stack |
| `/automatizar-processo` | "automatizar", "criar automacao", "processo automatico" | Automation Stack |
| `/forge` | "forge", "criar agente", "nova skill", "nova diretriz" | Forge (Builder) |
| `/mcp-setup` | "mcp setup", "conectar drive", "conectar slack", "instalar mcps" | MCP Setup |
| `/meta-cli-install` | "instalar meta cli", "configurar meta ads", "trafego pago setup" | Meta CLI |

## Sintaxe flexivel

O CoS Desktop entende variacoes naturais. Tudo isso aciona o mesmo comando:

```text
"preciso fazer preflight"
"vamos rodar preflight"
"preflight de acessos"
"libera meus acessos pra comecar"
"o que voce precisa pra eu liberar?"
```

Todos disparam o **PREFLIGHT**.

## Prefixo "forge:" pra builder

Pra usar Forge, sempre prefixe com `forge:`:

```text
"forge: criar agente especialista em VSL"
"forge: nova skill pra montar headline"
"forge: documentar processo de cobranca como diretriz"
"forge: conectar Stripe como MCP"
```

## Comandos compostos

```text
"primeira tarefa para clinica odontologica" 
  -> /setup-nicho (clinica) + /primeira-tarefa
  
"criar follow-up para lead que sumiu ha 3 dias"
  -> /follow-up (contexto: pos-proposta, 3 dias)
  
"diagnostico de trafego dos ultimos 7 dias"
  -> Traffic Stack + diagnostico janela 7d
```

CoS interpreta e roteia compondo.

## Quando nao funciona

Se voce digitou e o CoS nao entendeu:

1. Tente palavra-chave mais especifica.
2. Pergunte: `"que comando voce usaria pra isso?"` — CoS sugere.
3. Veja a lista completa em `22_CLAUDE_DESKTOP/commands-keywords.md` (este arquivo).

## Atalhos no Desktop

Cada Project no Claude Desktop **tem um atalho clicável na sidebar**. Pedro chamou isso de "shortcut".

Estrategia recomendada:

| Project | Nome curto pra sidebar |
|---|---|
| CoS V30 geral | `KPA Hub` |
| Trafego DR | `KPA Trafego` |
| WhatsApp + Cowork | `KPA WhatsApp` |
| Automacoes | `KPA Auto` |
| Builder/Forge | `KPA Forge` |

Mentorado clica no Project = ja entra com contexto pronto.
