# Projects Recomendados no Claude Desktop

> Em vez de 1 Project gigante, 3-5 Projects focados funcionam melhor. Cada um com knowledge dedicado e system prompt especifico.

## Por que multiplos Projects

- **Knowledge isolado:** evita poluir contexto com arquivos irrelevantes.
- **System prompt especifico:** CoS de Trafego ≠ CoS de WhatsApp.
- **Sidebar como menu:** clica no Project = entra no modo certo.
- **Sem conflito de comando:** mesma palavra-chave pode significar coisas diferentes por Project.

## Projects recomendados

### 1. `KPA Hub` (CoS V30 geral) — OBRIGATORIO

**Funcao:** entrada principal. Roteamento geral. Setup. Primeira entrega.

**System prompt:** `cos-desktop-system-prompt.md` completo

**Knowledge:** Lista "Project 1" em `knowledge-files.md` (Tier 1 + 2)

**Quando usar:**
- Primeiro dia
- Setup de cliente novo
- Quando nao sabe qual Project abrir
- Operacao do dia a dia generica

### 2. `KPA Trafego` — Trafego DR

**Funcao:** operacao de campanhas pagas Meta/Google. Diagnostico, criativos, escala.

**System prompt:** `cos-desktop-system-prompt.md` + adendo:

```text
# Adendo Trafego DR

Voce esta no Project Trafego DR. Suas trilhas principais sao:

- *diagnostico [janela] — saude geral
- *criativos [janela] — analise hook/retention/DNA
- *funil — drop-off por estagio
- *atribuicao — Pixel/CAPI saude, Standard vs Incremental
- *queda — root cause analysis em 6 camadas
- *escalar — plano de escala (ABO/CBO/Oxigenio)
- *espiar [concorrente] — engenharia reversa

NUNCA pause/edite/ative campanha sem confirmacao humana.
Nunca aprove gasto >20% mudanca de budget sem confirmacao.
Standard ROAS ≠ Incremental ROAS — sempre qualifique.
Paused-First Protocol: toda criacao inicia em PAUSED.
```

**Knowledge:** Lista "Project 2" em `knowledge-files.md` (12 arquivos da Traffic Stack)

**Quando usar:**
- Vai operar campanha paga
- Auditar tracking
- Analisar criativos
- Diagnosticar queda
- Planejar escala

### 3. `KPA WhatsApp` — WhatsApp + Cowork

**Funcao:** fluxos de WhatsApp, SDR, atendimento, Cowork docs.

**System prompt:** `cos-desktop-system-prompt.md` + adendo:

```text
# Adendo WhatsApp

Voce esta no Project WhatsApp Stack. Trilhas:

- *whatsapp-map — mapear bots e estados
- *sdr — fluxo SDR
- *follow — follow-up por estagio
- *cowork — gerar docs Cowork
- *qa-whats — validar fluxo

REGRAS INVIOLAVEIS:
- Bot nao finge ser humano.
- Sem disparo em massa sem confirmacao humana.
- Handoff humano obrigatorio em assunto sensivel.
- Stop rules sempre.
- Opt-out claro.
- Tudo em modo draft ate ativacao real.
```

**Knowledge:** Lista "Project 3" em `knowledge-files.md` (10 arquivos da WhatsApp Stack)

**Quando usar:**
- Criar/revisar fluxo WhatsApp
- Documentar Cowork
- Treinar SDR
- Configurar atendimento

### 4. `KPA Auto` — Automacoes (OPCIONAL)

**Funcao:** transformar processos do mentorado em automacoes documentadas.

**System prompt:** `cos-desktop-system-prompt.md` + adendo:

```text
# Adendo Automacoes

Voce esta no Project Automation Stack.

Workflow padrao:
1. Entender processo atual (perguntas guiadas).
2. Separar entradas/decisoes/saidas/responsaveis.
3. Marcar etapas: manual / ai_assisted / automated / blocked.
4. Gerar blueprint YAML.
5. Gerar SOP humano.
6. Gerar matriz de ferramentas/acessos.
7. Definir teste + rollback.
8. Marcar tudo como draft.

NUNCA ativar automacao real sem:
- Teste validado
- Rollback documentado
- Handoff humano definido
- Confirmacao explicita do mentorado
```

**Knowledge:** Lista "Project 4" em `knowledge-files.md`

**Quando usar:**
- Quer padronizar processo recorrente
- Conectar ferramentas (n8n, Make, Zapier, Cowork)
- Documentar fluxo de onboarding/follow-up/relatorio

### 5. `KPA Forge` — Builder (OPCIONAL — pra quem expande kit)

**Funcao:** criar agentes, skills, tasks, diretrizes novas.

**System prompt:** Conteudo de `21_BUILDER_KIT/agents/forge.md`

**Knowledge:** Lista "Project 5" em `knowledge-files.md`

**Quando usar:**
- Quer adicionar capacidade nova ao kit.
- Quer criar agente especializado pro nicho do mentorado.
- Quer expandir Traffic/WhatsApp/Automation Stack.

## Setup recomendado por perfil

### Mentorado leigo focado em servico

| Projects |
|---|
| KPA Hub (sempre) |
| KPA WhatsApp |

(2 Projects, simples e funcional)

### Mentorado que vende infoproduto

| Projects |
|---|
| KPA Hub |
| KPA Trafego |
| KPA WhatsApp |
| KPA Auto |

(4 Projects, cobre fluxo todo)

### Mentorado que opera agencia/servico digital

| Projects |
|---|
| KPA Hub |
| KPA Trafego |
| KPA WhatsApp |
| KPA Auto |
| KPA Forge |

(5 Projects — ele expande o kit)

## Tips

- **Project pode ter custom emoji/cor na sidebar.** Usa cor diferente pra cada (Trafego vermelho, WhatsApp verde, etc.).
- **Project tem URL.** Compartilha com equipe (se Team plan).
- **Knowledge update e manual.** Quando kit muda, mentorado refaz upload (ou Forge gera bundle ZIP).
