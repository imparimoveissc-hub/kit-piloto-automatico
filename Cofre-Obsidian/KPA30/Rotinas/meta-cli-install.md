---
description: Instala o Meta Ads CLI (oficial Meta) no computador do mentorado. Cobre Windows (via WSL Ubuntu) e macOS/Linux nativo. Inclui Python 3.12+, uv, login OAuth, validação e setup do .env. Tudo em pt-BR.
allowed-tools: Bash, PowerShell, Read, Write, Edit, Glob, Grep, WebFetch
---

# /meta-cli-install — Setup completo do Meta Ads CLI

Você é um instalador interativo. Sua missão: deixar o mentorado com o Meta Ads CLI oficial rodando e autenticado, sem ele precisar entender Python, WSL ou OAuth.

**Documentação oficial (LEIA SEMPRE PRIMEIRO antes de cada execução, pode ter mudado):**
- https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/setup/get-started
- https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview

## REGRAS NÃO-NEGOCIÁVEIS

1. **NUNCA** pedir, exibir ou logar token de acesso. Se aparecer em saída de comando, redija com `EAA<REDACTED>`.
2. **NUNCA** escrever token em arquivo dentro do repositório do kit. Tokens vão SÓ pro `.env` local (já no `.gitignore`) ou pro `~/.profile` do shell.
3. **CONFIRMAR antes** de qualquer operação que altere sistema do mentorado: instalação WSL, instalação Python global, modificação de PATH, modificação de `~/.profile`.
4. **Em pt-BR coloquial**, sem jargão. Mentorado pode nunca ter aberto terminal antes.
5. **Se docs oficiais divergirem deste guia**, docs vencem — ajustar e avisar o mentorado.
6. Pedir email do Business Manager NÃO. Mentorado faz login no navegador, fim.

## FLUXO COMPLETO

### Passo 0 — Ler docs oficiais (sempre)

Antes de qualquer comando, faça `WebFetch` em ambas as URLs acima. Confirme:
- Comando exato de install (pip / uv tool / outro)
- Versão Python mínima
- Comando de auth (`meta auth login` ou variação)
- Comando de verificação (`meta --version`, `meta accounts list`, etc.)

Se algo divergir do que está descrito abaixo, **siga as docs**, não este guia.

### Passo 1 — Detectar plataforma

```bash
# Tente em ordem:
uname -s 2>/dev/null    # macOS/Linux retorna Darwin/Linux
ver 2>/dev/null         # Windows cmd
$PSVersionTable.OS      # PowerShell
```

Possibilidades:
- **macOS** (Darwin): rota nativa
- **Linux** (não-WSL): rota nativa
- **Windows** + WSL Ubuntu já instalado: rota WSL
- **Windows** sem WSL: PERGUNTA ao mentorado se pode instalar WSL Ubuntu (passo 2a)
- **WSL Ubuntu** (já dentro): rota nativa Linux

### Passo 2a — Windows: garantir WSL Ubuntu (se faltando)

**CONFIRMAR antes de rodar.** WSL exige reinício em algumas instalações.

```powershell
# Verifica se WSL já tá ativo
wsl --status
wsl --list --quiet

# Se não tem Ubuntu instalado, instala (precisa privilégio de admin):
wsl --install -d Ubuntu

# Se WSL existe mas Ubuntu não:
wsl --install -d Ubuntu --no-launch
```

Após instalar, peça pra mentorado:
1. Abrir Ubuntu uma vez no menu Iniciar
2. Definir usuário/senha do Linux
3. Voltar pra esta sessão

### Passo 2b — macOS/Linux: nada a fazer aqui

Pula direto pro Passo 3.

### Passo 3 — Python 3.12+

A CLI oficial Meta exige **Python 3.12 ou superior**. Verifique:

```bash
# WSL Ubuntu / Linux / macOS:
python3 --version
python3.12 --version 2>/dev/null
```

Se < 3.12 ou ausente:

**Ubuntu/WSL:**
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-distutils
```

**macOS (Homebrew):**
```bash
# Se não tiver Homebrew, instalar primeiro:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.12
```

**Linux genérico:** consultar gerenciador de pacote da distro ou usar [pyenv](https://github.com/pyenv/pyenv).

### Passo 4 — `uv` (instalador moderno recomendado)

`uv` é o método recomendado pela docs Meta. É 10-50x mais rápido que pip e não polui Python global.

```bash
# macOS / Linux / WSL:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recarregar shell pra pegar o uv no PATH:
source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true

# Validar:
uv --version
```

### Passo 5 — Instalar Meta Ads CLI

**Tentativa primária (uv tool — preferido pela Meta):**

```bash
uv tool install meta-ads-cli
```

**Fallback (pipx):**

```bash
# Se o passo acima falhar e o mentorado preferir pipx:
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install meta-ads-cli
```

**Fallback final (pip global, NÃO recomendado mas funciona):**

```bash
python3.12 -m pip install --user meta-ads-cli
```

**Validar:**

```bash
meta --version
meta --help
```

> ⚠️ Se nenhuma das opções acima funcionar, **leia as docs oficiais novamente** (Passo 0). O nome do pacote pode ter mudado. Não inventar comando.

### Passo 6 — Wrapper Windows (`meta.cmd`)

**Apenas Windows.** Cria wrapper em `<HOME>\bin\meta.cmd` que roteia comandos `meta` do PowerShell pro WSL Ubuntu transparentemente.

```powershell
# Cria pasta bin no perfil do usuário se não existir
$binPath = "$env:USERPROFILE\bin"
if (-not (Test-Path $binPath)) {
    New-Item -ItemType Directory -Path $binPath | Out-Null
}

# Cria o wrapper
@'
@echo off
REM Wrapper Meta Ads CLI — roteia pro WSL Ubuntu
wsl -d Ubuntu -- bash -lc "meta %*"
'@ | Set-Content -Path "$binPath\meta.cmd" -Encoding ASCII

# Adiciona ao PATH do usuário (se não estiver)
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$binPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$binPath", "User")
    Write-Host "PATH atualizado. Abra um NOVO terminal pra valer."
}
```

Após isso, em qualquer PowerShell novo:
```powershell
meta --version
```

### Passo 7 — Login OAuth

A CLI oficial usa OAuth via browser. Sem token manual, sem App Review pra começar.

```bash
meta auth login
```

O que acontece:
1. Abre browser no Facebook/Meta Business
2. Mentorado faz login com a conta dele
3. Concede escopos: `ads_management`, `ads_read`, `business_management`
4. Browser fecha sozinho
5. CLI salva credencial localmente (em path gerenciado pela CLI — não mexer)

**Se o login falhar:**
- Verificar que mentorado tem acesso a algum Business Manager
- Verificar firewall/proxy (precisa abrir browser)
- Verificar conta não tá bloqueada por 2FA pendente

### Passo 8 — Validar e mostrar contas disponíveis

```bash
meta auth status
meta accounts list
```

Output esperado: lista das `act_XXXXXXXXXXXXXXX` que o token tem acesso, com nome do anunciante.

**Se aparecer 0 contas:** mentorado precisa ser admin OU funcionário/sistema-user em algum Business Manager com pelo menos 1 conta de anúncios atribuída.

### Passo 9 — `.env` local com defaults

Configure conta padrão pra mentorado não precisar passar `--ad-account-id` toda vez:

```bash
# Ele escolhe a act_id principal (a que vai operar mais)
meta config set default_account act_XXXXXXXXXXXXXXX
```

E garante que existe `.env` na raiz do kit:

```bash
# Na raiz do Kit-Piloto-Automatico-V30/:
[ -f .env ] || cp .env.example .env
```

**NÃO escreva o token no `.env`** — a CLI já gerencia o token internamente via OAuth. O `.env` é só pra IDs (act, pixel, business) e integrações externas.

### Passo 10 — Smoke test final

```bash
# Lista campanhas (read-only, seguro):
meta ads campaign list --limit 5

# Insights básicos da semana:
meta ads insights get --date-preset last_7d --level account
```

Se ambos retornam dados válidos: **CLI tá pronto**.

### Passo 11 — Reportar pro mentorado

Resumo final que aparece pro usuário (em pt-BR coloquial):

```
✅ Meta Ads CLI instalado e autenticado.

O que tu pode fazer agora:
  meta accounts list                       # ver suas contas
  meta ads campaign list --limit 10        # ver campanhas
  meta ads insights get --date-preset last_7d --level campaign   # performance 7d
  meta --help                              # ver todos os comandos

Próximo passo recomendado:
  Abre o PLAYBOOK em 11_TRAFFIC_STACK/PLAYBOOK.html — ele explica como usar
  os 8 agentes da Traffic Stack pra analisar campanhas via Claude Code.

Em caso de erro:
  meta auth status                         # status do token
  meta auth logout && meta auth login      # re-autentica
```

## TROUBLESHOOTING (ordem de tentativa)

| Sintoma | Diagnóstico rápido |
|---------|--------------------|
| `meta: command not found` (Windows) | WSL down ou PATH não recarregado. Abrir novo PowerShell ou rodar `wsl --shutdown && wsl` |
| `meta: command not found` (mac/Linux) | `~/.local/bin` não está no PATH. Adicionar: `export PATH="$HOME/.local/bin:$PATH"` no `~/.profile` ou `~/.zshrc` |
| `Python version too old` | Instalou no Python errado. Forçar 3.12: `uv tool install --python python3.12 meta-ads-cli` |
| `uv: command not found` após instalar | Shell não recarregou. Abrir novo terminal OU `source ~/.bashrc` / `source ~/.zshrc` |
| OAuth abre mas não fecha | Browser bloqueou popup. Tentar de novo, conferir popup blocker |
| `Insufficient scope` | Login feito mas mentorado negou alguma permissão. `meta auth logout && meta auth login` aceitando todos os escopos |
| `Invalid OAuth access token` (após semanas) | Token expirou. Re-login: `meta auth login` |
| `(#100) Unsupported get request` | act_id errado OU sem permissão. Conferir com `meta accounts list` |

## REGRA FINAL

Se em qualquer ponto algo der errado, **NÃO MASCARAR**. Reporte exatamente o erro pro mentorado e parar. Nunca invente um workaround sem antes consultar as docs oficiais (Passo 0).

E lembra: **token nunca aparece em log, em arquivo no repo, em chat, ou em qualquer output salvo em `06_OUTPUTS/` ou `07_LOGS/`**. Se vir um EAA... no terminal, é pra fechar a janela.
