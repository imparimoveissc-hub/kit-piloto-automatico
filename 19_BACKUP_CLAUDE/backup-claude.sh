#!/usr/bin/env bash
# =============================================================================
#  Backup claude  —  roda no Mac ATUAL (o que já funciona)
#  Recolhe tudo que o Claude Code guarda FORA do iCloud (~/.claude, ngrok,
#  versoes, video-use) e salva em 19_BACKUP_CLAUDE/snapshot/ dentro do Kit.
#  Como o Kit inteiro fica no iCloud Drive, o snapshot viaja sozinho pro Mac novo.
#
#  Uso:  bash backup-claude.sh
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SNAP="$SCRIPT_DIR/snapshot"
CLAUDE_DIR="$HOME/.claude"
NGROK_YML="$HOME/Library/Application Support/ngrok/ngrok.yml"

echo "==> Limpando snapshot anterior"
rm -rf "$SNAP"
mkdir -p "$SNAP/dot-claude" "$SNAP/meta"

# ---------------------------------------------------------------------------
# 1) Config do Claude Code (~/.claude) — só o que importa, sem sessoes/cache
# ---------------------------------------------------------------------------
echo "==> Copiando ~/.claude (skills, settings, plugins, scheduled-tasks)"
# skills reais (o symlink video-use é tratado à parte no instalador)
if [ -d "$CLAUDE_DIR/skills" ]; then
  mkdir -p "$SNAP/dot-claude/skills"
  # -L nao segue symlink de topo; copiamos só as pastas reais
  for d in "$CLAUDE_DIR"/skills/*/; do
    name="$(basename "$d")"
    if [ -L "${d%/}" ]; then
      echo "    (symlink ignorado: $name — recriado pelo instalador)"
    else
      cp -R "$d" "$SNAP/dot-claude/skills/$name"
    fi
  done
fi

[ -f "$CLAUDE_DIR/settings.json" ] && cp "$CLAUDE_DIR/settings.json" "$SNAP/dot-claude/settings.json"
[ -f "$CLAUDE_DIR/CLAUDE.md" ]      && cp "$CLAUDE_DIR/CLAUDE.md"      "$SNAP/dot-claude/CLAUDE.md"

# plugins: só os JSONs de registro (o conteudo do marketplace vive no iCloud)
if [ -d "$CLAUDE_DIR/plugins" ]; then
  mkdir -p "$SNAP/dot-claude/plugins"
  for f in installed_plugins.json known_marketplaces.json; do
    [ -f "$CLAUDE_DIR/plugins/$f" ] && cp "$CLAUDE_DIR/plugins/$f" "$SNAP/dot-claude/plugins/$f"
  done
fi

# tarefas agendadas
[ -d "$CLAUDE_DIR/scheduled-tasks" ] && cp -R "$CLAUDE_DIR/scheduled-tasks" "$SNAP/dot-claude/scheduled-tasks"

# memoria persistente do projeto (fica em ~/.claude/projects/.../memory)
if [ -d "$CLAUDE_DIR/projects" ]; then
  mkdir -p "$SNAP/dot-claude/projects"
  # copia só as pastas memory/ (leves), nao os historicos de sessao
  find "$CLAUDE_DIR/projects" -type d -name memory 2>/dev/null | while read -r m; do
    proj="$(basename -- "$(dirname -- "$m")")"   # nome da pasta do projeto (pode comecar com '-')
    mkdir -p "$SNAP/dot-claude/projects/$proj"
    cp -R "$m" "$SNAP/dot-claude/projects/$proj/memory"
  done
fi

# ---------------------------------------------------------------------------
# 2) ngrok authtoken
# ---------------------------------------------------------------------------
echo "==> Copiando ngrok.yml (authtoken)"
if [ -f "$NGROK_YML" ]; then
  cp "$NGROK_YML" "$SNAP/ngrok.yml"
else
  echo "    (ngrok.yml nao encontrado — pule)"
fi

# ---------------------------------------------------------------------------
# 3) video-use (repo separado, fora do iCloud) — guardamos só o .env
#    O codigo é re-clonado do GitHub pelo instalador.
# ---------------------------------------------------------------------------
if [ -d "$HOME/Developer/video-use" ]; then
  echo "==> Guardando .env do video-use"
  mkdir -p "$SNAP/video-use"
  [ -f "$HOME/Developer/video-use/.env" ] && cp "$HOME/Developer/video-use/.env" "$SNAP/video-use/.env"
  git -C "$HOME/Developer/video-use" remote get-url origin 2>/dev/null > "$SNAP/video-use/REMOTE.txt" || true
fi

# ---------------------------------------------------------------------------
# 4) Manifesto de versoes / pacotes (pro instalador reproduzir)
# ---------------------------------------------------------------------------
echo "==> Gravando manifesto de versoes"
{
  echo "# Snapshot gerado em: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "# Maquina de origem: $(hostname) — usuario: $USER"
  echo "node=$(node --version 2>/dev/null || echo ausente)"
  echo "npm=$(npm --version 2>/dev/null || echo ausente)"
  echo "ngrok=$(ngrok --version 2>/dev/null || echo ausente)"
  echo "python3=$(python3 --version 2>/dev/null || echo ausente)"
  echo "uv=$(uv --version 2>/dev/null || echo ausente)"
  echo "brew=$(brew --version 2>/dev/null | head -1 || echo ausente)"
} > "$SNAP/meta/versoes.txt"

npm ls -g --depth=0 2>/dev/null > "$SNAP/meta/npm-globais.txt" || true
brew leaves 2>/dev/null > "$SNAP/meta/brew-leaves.txt" || true
brew list --cask 2>/dev/null > "$SNAP/meta/brew-casks.txt" || true

# ---------------------------------------------------------------------------
# 5) Snapshot dos .env do Kit (redundante — ja estao no iCloud — mas garante)
# ---------------------------------------------------------------------------
echo "==> Copiando .env do Kit para o snapshot"
mkdir -p "$SNAP/envs"
[ -f "$SCRIPT_DIR/../.env" ] && cp "$SCRIPT_DIR/../.env" "$SNAP/envs/raiz.env"
[ -f "$SCRIPT_DIR/../18_AUTOMATION_STACK/nfem-joinville/.env" ] && \
  cp "$SCRIPT_DIR/../18_AUTOMATION_STACK/nfem-joinville/.env" "$SNAP/envs/nfem-joinville.env"

echo ""
echo "============================================================"
echo " BACKUP CONCLUIDO"
echo " Snapshot em: $SNAP"
echo " Ele sincroniza pelo iCloud junto com o Kit."
echo ""
echo " No Mac NOVO, depois que o iCloud terminar de baixar o Kit,"
echo " abra o Terminal e rode:"
echo ""
echo "   bash \"$SCRIPT_DIR/instalar-nova-maquina.sh\""
echo "============================================================"
