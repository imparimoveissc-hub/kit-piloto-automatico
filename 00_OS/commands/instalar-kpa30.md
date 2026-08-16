# Command — /instalar-kpa30

> **Wizard unico de instalacao do Kit V30.** Roda 1 vez por maquina. Cobre dependencias + MCPs + onboarding do negocio + primeira tarefa.

## Triggers

- `/instalar-kpa30`
- "instalar kpa30"
- "instalar kit"
- "instalar kpa v30"
- "comecar a usar o kit"
- "primeira instalacao"

## Objetivo final

Ao terminar o wizard, o mentorado tem:

1. Dependencias base instaladas (Node, Python se aplicavel).
2. `.env` local configurado.
3. MCPs Tier 1 ativos.
4. Projects do Claude Desktop criados (se estiver no app).
5. Context do negocio salvo (`.claude/config.md` + `current-context.md`).
6. Familia operacional classificada.
7. Primeira tarefa util gerada.

## Identificacao de plataforma

ANTES de comecar, detectar onde esta rodando:

```bash
# Tentar:
uname -s 2>/dev/null     # Mac/Linux retorna Darwin/Linux
ver 2>/dev/null          # Windows CMD
$PSVersionTable.OS       # PowerShell

# Detectar Claude Code vs Desktop:
# - Claude Code: tem acesso a Bash, PowerShell, Read/Write/Edit tools nativos
# - Claude Desktop: sem Bash nativo. Tem que orientar mentorado a abrir terminal proprio.
```

Variavel mental: `PLATFORM` (`code` ou `desktop`).

## Fluxo

### Etapa 0 — Boas-vindas + confirmacao

Mensagem ao mentorado:

```text
Beleza, vou te ajudar a instalar o Kit Piloto Automatico V30.

O processo tem 7 etapas e leva uns 15-20 minutos:

1. Conferir dependencias do seu computador
2. Configurar arquivo .env
3. Ativar MCPs essenciais (Drive, WhatsApp, etc.)
4. Configurar Meta Ads CLI (se voce usa trafego pago)
5. Criar Projects no Claude Desktop (se voce usa o app)
6. Te conhecer (empresa, nicho, produto, gargalo)
7. Gerar sua primeira tarefa util

Comecar? (sim / ainda nao)
```

Se "ainda nao": parar e dar opcao de retomar depois.
Se "sim": seguir.

### Etapa 1 — Conferir dependencias

#### No Claude Code

```bash
node --version           # esperar >= v18
npm --version
git --version
```

Se faltar Node:
- **Mac:** `brew install node` (precisa Homebrew)
- **Windows:** baixar em https://nodejs.org (versao LTS)
- **Linux:** `sudo apt install nodejs npm` ou via nvm

Confirma com mentorado antes de qualquer install que afeta sistema.

#### No Claude Desktop

Orientar mentorado:

```text
Pra continuar, preciso que voce confira se tem Node.js instalado.

1. Abre Terminal (Mac) ou PowerShell (Windows) ou Terminal (Linux)
2. Cola: node --version
3. Me manda o resultado aqui

Se aparecer "command not found" ou erro, eu te ajudo a instalar.
Se aparecer "v20.X.X" ou similar, ta tudo certo.
```

Aguarda resposta. Se Node faltar, da link de download.

### Etapa 2 — Configurar .env

Verifica se `.env` ja existe. Se nao:

#### No Code

```bash
cp .env.example .env       # Mac/Linux
copy .env.example .env     # Windows
```

#### No Desktop

```text
Pra criar o arquivo de configuracao do kit:

1. No Terminal/PowerShell, navega ate a pasta do kit:
   cd <caminho do kit>

2. Cola:
   cp .env.example .env    (Mac/Linux)
   copy .env.example .env  (Windows)

3. Me avisa quando terminar.
```

Pergunta dados nao-sensiveis pra preencher (OPERATOR_NAME, OPERATOR_BRAND). NAO pede token nem credencial.

### Etapa 3 — MCPs Tier 1

Pergunta ao mentorado:

```text
Vou ativar conectores essenciais. Quais voce precisa? (responde com numeros, ex: 1, 2, 3)

1. Composio Rube (Drive, Slack, Notion, Gmail, HubSpot, Linear, X/LinkedIn...) - RECOMENDADO
2. WhatsApp (gerenciar WhatsApp Web direto) - se voce atende/vende por WhatsApp
3. Filesystem (acesso facil a pastas locais) - util pra organizar entregas
4. Playwright (auditar LPs e capturar screenshots) - opcional, util pra trafego

Recomendado pra todo mundo: 1 e 3.
Pra quem usa WhatsApp comercial: 1, 2 e 3.
Pra quem trabalha com trafego/agencia: 1, 2, 3 e 4.
```

Pra cada selecionado:

#### No Code

```bash
# Composio Rube
claude mcp add rube --command "npx -y @composio/rube-mcp"

# WhatsApp (precisa clone do repo)
cd ~/mcps 2>/dev/null || mkdir -p ~/mcps && cd ~/mcps
git clone https://github.com/verygoodplugins/whatsapp-mcp.git
cd whatsapp-mcp && npm install
claude mcp add whatsapp --command "node $HOME/mcps/whatsapp-mcp/index.js"

# Filesystem
claude mcp add filesystem --command "npx -y @modelcontextprotocol/server-filesystem $PWD"

# Playwright
claude mcp add playwright --command "npx -y @modelcontextprotocol/server-playwright"
```

#### No Desktop

```text
No Desktop, MCPs sao configurados manualmente no arquivo claude_desktop_config.json.

Vou te dar o caminho do arquivo e o que colar dentro:

[Mac]: ~/Library/Application Support/Claude/claude_desktop_config.json
[Windows]: %APPDATA%\Claude\claude_desktop_config.json
[Linux]: ~/.config/Claude/claude_desktop_config.json

Abre esse arquivo (com Notepad/TextEdit/VSCode) e cola:

{
  "mcpServers": {
    "rube": {
      "command": "npx",
      "args": ["-y", "@composio/rube-mcp"]
    },
    [outros que voce escolheu]
  }
}

Depois de salvar:
1. Fecha o Claude Desktop totalmente
2. Reabre
3. Me avisa
```

Valida com `claude mcp list` (Code) ou pedindo mentorado testar comando MCP (Desktop).

### Etapa 4 — Meta Ads CLI (opcional)

```text
Voce roda trafego pago no Meta Ads (Facebook/Instagram Ads)? (sim / nao)
```

Se sim, executar fluxo de `/meta-cli-install` (skill em `11_TRAFFIC_STACK/skills/meta-cli-install/SKILL.md`).

Se nao, pular.

### Etapa 5 — Projects do Claude Desktop (so se for Desktop)

Pular se estiver no Claude Code.

Se estiver no Desktop:

```text
O Claude Desktop usa Projects pra manter contexto por area. Vou te ajudar a criar 3:

1. KPA Hub (geral) - obrigatorio
2. KPA WhatsApp (so se voce atende por WhatsApp)
3. KPA Trafego (so se voce roda Meta Ads)

Quer criar os 3 ou so o Hub? (3 / so 1)
```

Pra cada Project:

1. Da instrucao pro mentorado:
   - "Clica em + New Project na sidebar"
   - "Nome: [nome]"
   - "Cola system prompt: [conteudo de cos-desktop-system-prompt.md]"
   - "Faz upload dos arquivos: [lista de knowledge-files.md correspondente]"
2. Aguarda confirmacao
3. Proximo Project

Detalhes completos em `22_CLAUDE_DESKTOP/setup-project.md`.

### Etapa 6 — Onboarding do negocio (PRINCIPAL)

Agora coleta info do negocio do mentorado. Faz UMA pergunta de cada vez:

```text
Vou te conhecer pra adaptar o kit. 6 perguntas rapidas.

1. Qual o nome da sua empresa/marca?
```

Aguarda resposta. Salva como `business.name`.

```text
2. Em uma frase, o que voce vende? (produto, servico, oferta principal)
```

Salva `business.offer`.

```text
3. Qual seu segmento/nicho?
   Ex: "consultoria de marketing", "clinica odontologica", "loja de cosmeticos online",
   "advogado civel", "gestor de trafego freelancer"
```

Salva `business.segment`.

```text
4. Quem e seu cliente ideal? (perfil em 1-2 linhas)
```

Salva `business.target_audience`.

```text
5. Qual seu canal principal hoje?
   - WhatsApp / Instagram / Google / Indicacao / Site / outro
```

Salva `business.main_channel`.

```text
6. Qual seu maior gargalo operacional hoje?
   Ex: nao consigo atender todo mundo, perco lead por falta de follow-up,
   nao tenho tempo de criar conteudo, conversao baixa, etc.
```

Salva `business.current_bottleneck`.

### Etapa 7 — Classificar familia + criar context

Com base nas 6 respostas, classifica em UMA das 8 familias operacionais:

| Sinais | Familia |
|---|---|
| atende por cidade/bairro, WhatsApp, agenda | servico-local |
| vende expertise individual, agenda, confianca | profissional-liberal |
| vende pra empresas, ciclo longo, multiplos decisores | b2b-consultivo |
| produto, pedido, carrinho, entrega | ecommerce |
| curso, mentoria, area de membros, lancamento | infoproduto |
| social media, trafego, design, video, copy | agencia-servico-digital |
| paciente, consulta, agendamento, saude | clinica-saude |
| caso, processo, prazo, confidencialidade | juridico-regulado |

Depois cria 2 arquivos:

#### `.claude/config.md`

```markdown
# Config do mentorado

```yaml
business:
  name: "<resposta 1>"
  offer: "<resposta 2>"
  segment: "<resposta 3>"
  target_audience: "<resposta 4>"
  main_channel: "<resposta 5>"
  current_bottleneck: "<resposta 6>"
  family: "<familia classificada>"
preset_used: "<preset ou null>"
tom_de_voz: "<derivado do segmento>"
mcps_ativos: [<lista>]
recommended_templates: [<lista>]
recommended_whatsapp_flows: [<lista>]
recommended_automation: "<sugerido>"
first_task: "<primeira tarefa>"
created_at: "<data>"
```

## Arquivos do kit adaptados

- Familia operacional: `15_PRODUCT_RELEASE/exemplos/familias/<familia>.md`
- Preset (se houver): `15_PRODUCT_RELEASE/nichos/<nicho>/`
- Squad inicial: `13_ADAPTIVE_SQUADS/`
```

#### `05_WORKSPACE/current-context.md`

```yaml
projeto: "<nome do negocio>"
objetivo: "<inferido do gargalo>"
publico: "<target_audience>"
oferta: "<offer>"
mecanismo: "[A PREENCHER apos primeira tarefa]"
tom: "<derivado>"
provas_confirmadas: []
restricoes: []
status: "onboarded"
proxima_task: "primeira-tarefa"
arquivos_relevantes:
  - ".claude/config.md"
  - "15_PRODUCT_RELEASE/exemplos/familias/<familia>.md"
squad_manifest: "[A PREENCHER quando cliente piloto for definido]"
whatsapp_status: "<nao_mapeado | sera_mapeado | nao_aplica>"
preflight_status: "instalacao_concluida"
```

### Etapa 8 — Gerar primeira tarefa util

Com base na familia, sugere primeira entrega. Pergunta:

```text
Pra fechar a instalacao com chave de ouro, vou gerar sua primeira entrega util agora.

Considerando seu cenario:
- Negocio: <name>
- Familia: <familia>
- Maior gargalo: <bottleneck>

Eu sugiro comecar com: <primeira-tarefa-sugerida>

Concorda ou prefere outra opcao? (sim / outra)
```

Opcoes por familia:

| Familia | Primeira tarefa default |
|---|---|
| servico-local | Fluxo WhatsApp de triagem de novo atendimento |
| profissional-liberal | Briefing de diagnostico de prospect |
| b2b-consultivo | Script de qualificacao SDR |
| ecommerce | Fluxo WhatsApp de atendimento de duvida de produto |
| infoproduto | Sequencia de onboarding pos-compra |
| agencia-servico-digital | Briefing organizado de cliente novo |
| clinica-saude | Fluxo WhatsApp de agendamento seguro |
| juridico-regulado | Intake seguro de novo caso |

Roda a primeira tarefa **agora**, gerando o output.

### Etapa 9 — Resumo final

```text
Pronto! Kit V30 instalado e adaptado pro seu negocio.

✓ Dependencias verificadas
✓ .env configurado
✓ MCPs ativos: <lista>
✓ Meta Ads CLI: <sim/nao/N/A>
✓ Projects Desktop: <quantidade ou N/A>
✓ Familia operacional: <familia>
✓ Primeira tarefa gerada: <nome>

Salvei tudo em:
- .claude/config.md (perfil do seu negocio)
- 05_WORKSPACE/current-context.md (estado atual)
- 06_OUTPUTS/<data>_primeira-tarefa/ (sua primeira entrega)

Proximos comandos:

- /primeira-tarefa - gera outra entrega
- /briefing - cria briefing de cliente novo
- /whatsapp-system - monta fluxos WhatsApp (modo draft)
- /automatizar-processo - documenta automacao
- /forge - cria agente/skill novo
- /mcp-setup - adiciona mais MCPs depois

Documentacao publica: 15_PRODUCT_RELEASE/
Guia visual: 15_PRODUCT_RELEASE/index.html

Algum proximo passo? Posso:
1. Gerar outra entrega (proposta, follow-up, calendario)
2. Montar fluxo WhatsApp pra <gargalo>
3. Configurar mais MCPs
4. Explicar algo do kit
```

## Regras de execucao

1. **NUNCA pedir token no chat.** Tokens vao no `.env` manualmente pelo mentorado.
2. **NUNCA executar acao destrutiva sem confirmacao.** Mesmo Bash com `rm`, `mv`, etc.
3. **Pause sempre que mentorado precisar fazer algo manual.** Aguarde "feito" antes de seguir.
4. **Se etapa falhar, NAO MASCARAR.** Reporta o erro exato, sugere correcao, oferece pular.
5. **Mentorado pode interromper a qualquer momento.** Salva progresso em `05_WORKSPACE/current-context.md`.
6. **Pra Desktop, sempre orientar passo a passo.** Sem suposicoes do que ele consegue rodar sozinho.
7. **Tudo em pt-BR coloquial profissional.**

## Saida estruturada (handoff)

Ao terminar:

```yaml
install_status: complete | partial | aborted
platform: code | desktop
business:
  family:
  configured: yes | no
mcps_active: []
meta_cli: yes | no | skipped
projects_desktop: <num>
first_task_generated: yes | no
config_file: ".claude/config.md"
current_context: "05_WORKSPACE/current-context.md"
next_step: "<acao recomendada>"
pendencias: []
```

## Retomada

Se mentorado parou no meio, ao rodar `/instalar-kpa30` de novo:

1. Le `.claude/config.md` e `05_WORKSPACE/current-context.md`.
2. Identifica em qual etapa parou.
3. Pergunta: "Vi que voce ja instalou X. Quer continuar a partir de Y ou refazer do zero?"
4. Continua de onde parou.

## Erros comuns

| Sintoma | Solucao |
|---|---|
| `node: command not found` | Instalar Node antes de tudo (link nodejs.org) |
| `npx` retorna erro | Atualizar npm: `npm install -g npm@latest` |
| MCP nao aparece em `claude mcp list` | Reiniciar Claude Code |
| Project Desktop nao reconhece kit | Re-upload knowledge files |
| `.env` nao foi criado | Conferir pasta certa (raiz do kit) |
| Mentorado sem permissao admin | Pular Meta CLI, marcar como pendente |
