#!/usr/bin/env bash
# =============================================================================
#  Instalador — roda no Mac NOVO
#  Instala Homebrew, Node, ngrok, git, gh, Python, uv, Claude Code CLI,
#  navegadores do Playwright, restaura ~/.claude (skills, settings, plugins,
#  tarefas agendadas, memoria), restaura o authtoken do ngrok, reconstroi o
#  video-use e o ambiente Python do NF-em Joinville.
#
#  Uso (Terminal do Mac novo, depois do iCloud baixar o Kit):
#     bash "<caminho-do-kit>/19_BACKUP_CLAUDE/instalar-nova-maquina.sh"
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SNAP="$SCRIPT_DIR/snapshot"
CLAUDE_DIR="$HOME/.claude"
OLD_HOME="/Users/user"          # home da maquina de origem (para reescrever caminhos)

c_ok()   { printf "\033[32m✔\033[0m %s\n" "$1"; }
c_info() { printf "\033[36m==>\033[0m %s\n" "$1"; }
c_warn() { printf "\033[33m!\033[0m %s\n" "$1"; }

echo "============================================================"
echo "  INSTALADOR KIT PILOTO AUTOMATICO V30 + CLAUDE CODE"
echo "  Mac novo: $(hostname) — usuario: $USER"
echo "  Kit em: $KIT_DIR"
echo "============================================================"
echo ""

if [ ! -d "$SNAP" ]; then
  c_warn "Snapshot nao encontrado em $SNAP"
  c_warn "Rode 'bash backup-claude.sh' no Mac antigo e espere o iCloud sincronizar."
  exit 1
fi

# ---------------------------------------------------------------------------
# 1) Xcode Command Line Tools (git etc.)
# ---------------------------------------------------------------------------
if ! xcode-select -p >/dev/null 2>&1; then
  c_info "Instalando Xcode Command Line Tools (aceite a janela que abrir)…"
  xcode-select --install || true
  echo "    Aguardando terminar a instalacao das Command Line Tools…"
  until xcode-select -p >/dev/null 2>&1; do sleep 10; done
fi
c_ok "Command Line Tools presentes"

# ---------------------------------------------------------------------------
# 2) Homebrew
# ---------------------------------------------------------------------------
if ! command -v brew >/dev/null 2>&1; then
  c_info "Instalando Homebrew…"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
# carrega o brew no PATH (Apple Silicon usa /opt/homebrew)
if [ -x /opt/homebrew/bin/brew ]; then eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then eval "$(/usr/local/bin/brew shellenv)"; fi
c_ok "Homebrew: $(brew --version | head -1)"

# ---------------------------------------------------------------------------
# 3) Ferramentas base via brew
# ---------------------------------------------------------------------------
c_info "Instalando node, git, gh, python, ngrok…"
brew install node git gh python@3.12 2>/dev/null || true
brew install --cask ngrok 2>/dev/null || brew install ngrok 2>/dev/null || true
c_ok "node $(node --version 2>/dev/null) | ngrok $(ngrok --version 2>/dev/null | head -1)"

# uv (gerenciador Python usado pelo Meta CLI e afins)
if ! command -v uv >/dev/null 2>&1; then
  c_info "Instalando uv…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
c_ok "uv $(uv --version 2>/dev/null || echo instalado)"

# ---------------------------------------------------------------------------
# 4) Claude Code CLI
# ---------------------------------------------------------------------------
if ! command -v claude >/dev/null 2>&1; then
  c_info "Instalando Claude Code CLI (npm global)…"
  npm install -g @anthropic-ai/claude-code
fi
c_ok "Claude Code: $(claude --version 2>/dev/null || echo instalado)"

# ---------------------------------------------------------------------------
# 5) Restaurar ~/.claude (skills, settings, plugins, tarefas, memoria)
#    Reescreve caminhos /Users/user -> $HOME quando o usuario for diferente.
# ---------------------------------------------------------------------------
c_info "Restaurando configuracao do Claude (~/.claude)…"
mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/plugins"

rewrite() { # reescreve OLD_HOME -> $HOME dentro de um arquivo, se preciso
  local f="$1"
  [ -f "$f" ] || return 0
  if [ "$HOME" != "$OLD_HOME" ]; then
    sed -i '' "s#${OLD_HOME}#${HOME}#g" "$f" 2>/dev/null || true
  fi
}

# skills reais
if [ -d "$SNAP/dot-claude/skills" ]; then
  for d in "$SNAP"/dot-claude/skills/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    rm -rf "$CLAUDE_DIR/skills/$name"
    cp -R "$d" "$CLAUDE_DIR/skills/$name"
  done
  c_ok "Skills restauradas: $(ls -1 "$CLAUDE_DIR/skills" | tr '\n' ' ')"
fi

# settings + CLAUDE.md global
[ -f "$SNAP/dot-claude/settings.json" ] && cp "$SNAP/dot-claude/settings.json" "$CLAUDE_DIR/settings.json" && rewrite "$CLAUDE_DIR/settings.json"
[ -f "$SNAP/dot-claude/CLAUDE.md" ]      && cp "$SNAP/dot-claude/CLAUDE.md"      "$CLAUDE_DIR/CLAUDE.md"

# plugins (registro + marketplace)
for f in installed_plugins.json known_marketplaces.json; do
  if [ -f "$SNAP/dot-claude/plugins/$f" ]; then
    cp "$SNAP/dot-claude/plugins/$f" "$CLAUDE_DIR/plugins/$f"
    rewrite "$CLAUDE_DIR/plugins/$f"
  fi
done

# tarefas agendadas
if [ -d "$SNAP/dot-claude/scheduled-tasks" ]; then
  cp -R "$SNAP/dot-claude/scheduled-tasks" "$CLAUDE_DIR/scheduled-tasks"
  find "$CLAUDE_DIR/scheduled-tasks" -type f \( -name "*.json" -o -name "*.md" -o -name "*.txt" \) -exec sed -i '' "s#${OLD_HOME}#${HOME}#g" {} \; 2>/dev/null || true
  c_ok "Tarefas agendadas restauradas: $(ls -1 "$CLAUDE_DIR/scheduled-tasks" | wc -l | tr -d ' ')"
fi

# memoria persistente
if [ -d "$SNAP/dot-claude/projects" ]; then
  cp -R "$SNAP/dot-claude/projects" "$CLAUDE_DIR/projects" 2>/dev/null || \
    cp -R "$SNAP/dot-claude/projects/." "$CLAUDE_DIR/projects/" 2>/dev/null || true
  c_ok "Memoria persistente restaurada"
fi

# ---------------------------------------------------------------------------
# 6) ngrok authtoken
# ---------------------------------------------------------------------------
if [ -f "$SNAP/ngrok.yml" ]; then
  TOKEN="$(grep -E 'authtoken:' "$SNAP/ngrok.yml" | sed -E 's/.*authtoken:[[:space:]]*//')"
  if [ -n "$TOKEN" ]; then
    c_info "Configurando authtoken do ngrok…"
    ngrok config add-authtoken "$TOKEN" >/dev/null 2>&1 && c_ok "ngrok autenticado"
  fi
fi

# ---------------------------------------------------------------------------
# 7) video-use (skill de edicao de video) — re-clonar + venv + symlink
# ---------------------------------------------------------------------------
if [ -f "$SNAP/video-use/REMOTE.txt" ]; then
  REMOTE="$(cat "$SNAP/video-use/REMOTE.txt")"
  DEST="$HOME/Developer/video-use"
  if [ -n "$REMOTE" ] && [ ! -d "$DEST/.git" ]; then
    c_info "Clonando video-use ($REMOTE)…"
    mkdir -p "$HOME/Developer"
    git clone "$REMOTE" "$DEST" && \
    ( cd "$DEST" && uv venv >/dev/null 2>&1 && uv pip install -e . >/dev/null 2>&1 ) || true
    [ -f "$SNAP/video-use/.env" ] && cp "$SNAP/video-use/.env" "$DEST/.env"
  fi
  # recria o symlink da skill
  if [ -d "$DEST" ]; then
    ln -sfn "$DEST" "$CLAUDE_DIR/skills/video-use"
    c_ok "Skill video-use religada"
  fi
fi

# ---------------------------------------------------------------------------
# 8) NF-em Joinville — ambiente Python + Playwright
# ---------------------------------------------------------------------------
NFEM="$KIT_DIR/18_AUTOMATION_STACK/nfem-joinville"
if [ -f "$NFEM/requirements.txt" ]; then
  c_info "Preparando ambiente do NF-em Joinville…"
  ( cd "$NFEM"
    python3.12 -m venv .venv 2>/dev/null || python3 -m venv .venv
    ./.venv/bin/pip install --quiet --upgrade pip
    ./.venv/bin/pip install --quiet -r requirements.txt
    ./.venv/bin/python -m playwright install chromium
  ) && c_ok "NF-em Joinville pronto (.venv + Playwright)" || c_warn "Revise o NF-em manualmente"
fi

# ---------------------------------------------------------------------------
# 9) Rotinas agendadas — prompts restaurados; gera comando p/ recriar os cron
#    Os horarios (cron) vivem no servico de agendamento do Claude, nao em
#    disco. Aqui deixamos um prompt pronto p/ colar no Claude e recriar tudo.
# ---------------------------------------------------------------------------
ROTINAS_YAML="$SCRIPT_DIR/rotinas.yaml"
PROMPT_OUT="$SCRIPT_DIR/COLAR-NO-CLAUDE-recriar-rotinas.txt"
if [ -f "$ROTINAS_YAML" ]; then
  N_ROT="$(grep -cE '^\s*- nome:' "$ROTINAS_YAML" 2>/dev/null || echo '?')"
  {
    echo "Recrie TODAS as rotinas agendadas do arquivo abaixo, uma por uma, com a skill /schedule."
    echo "Para cada item use o campo cron como agendamento e o prompt correspondente em"
    echo "~/.claude/scheduled-tasks/<nome>/SKILL.md (ja restaurado nesta maquina)."
    echo "Fuso: America/Sao_Paulo. Nao dispare nenhuma agora; so agende."
    echo ""
    echo "Arquivo com as rotinas e horarios:"
    echo "$ROTINAS_YAML"
  } > "$PROMPT_OUT"
  c_ok "Rotinas ($N_ROT) prontas p/ reagendar — instrucao em: $PROMPT_OUT"
fi

echo ""
echo "============================================================"
echo "  INSTALACAO AUTOMATICA CONCLUIDA"
echo "============================================================"
echo ""
echo "  Faltam 4 passos MANUAIS (precisam de login/interface):"
echo ""
echo "  1) Logar no Claude Code:"
echo "        claude    (dentro do Kit)  ->  digite  /login"
echo ""
echo "  2) Reconectar os MCP/conectores (WhatsApp, Asaas, Outlook/Composio,"
echo "     Filesystem, Meta, Google Drive etc.) pelo app Claude/Cowork ->"
echo "     Conectores. Eles nao migram por arquivo; é so reautorizar cada um."
echo ""
echo "  3) Recriar as ROTINAS agendadas (horarios nao migram por arquivo):"
echo "     dentro do Claude, cole o conteudo de:"
echo "        $PROMPT_OUT"
echo "     (ele manda o Claude ler o rotinas.yaml e agendar as 9 rotinas)."
echo ""
echo "  4) Meta Ads CLI (so se usar trafego): dentro do Kit rode a skill"
echo "        /meta-cli-install"
echo ""
echo "  Depois, teste com:  claude  ->  \"instalar kpa30\" ou \"start-here\""
echo "============================================================"
