#!/usr/bin/env bash
set -euo pipefail

echo "Instalador do backup Codex / KPA30"
echo "=================================="
echo

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCHIVE="${1:-}"

if [[ -z "$ARCHIVE" ]]; then
  ARCHIVE="$(find "$SCRIPT_DIR" -maxdepth 1 -type f -name 'Kit-Piloto-Automatico-V30-DISTRIB-*.tar.gz' | head -n 1 || true)"
fi

if [[ -z "$ARCHIVE" || ! -f "$ARCHIVE" ]]; then
  echo "Nao encontrei o arquivo .tar.gz do backup nesta pasta."
  echo "Coloque o arquivo Kit-Piloto-Automatico-V30-DISTRIB-*.tar.gz ao lado deste script"
  echo "ou rode: bash install_backup_codex.sh /caminho/arquivo.tar.gz"
  exit 1
fi

echo "Backup encontrado:"
echo "$ARCHIVE"
echo

DEFAULT_DEST="$HOME/Documents"
read -r -p "Onde restaurar? [$DEFAULT_DEST] " DEST
DEST="${DEST:-$DEFAULT_DEST}"
mkdir -p "$DEST"

TARGET="$DEST/Kit-Piloto-Automatico-V30-DISTRIB"
if [[ -e "$TARGET" ]]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  TARGET="$DEST/Kit-Piloto-Automatico-V30-DISTRIB-restaurado-$TS"
  echo "Ja existe uma pasta com esse nome. Vou restaurar em:"
  echo "$TARGET"
  mkdir -p "$TARGET"
  tar -xzf "$ARCHIVE" -C "$TARGET" --strip-components=1
else
  tar -xzf "$ARCHIVE" -C "$DEST"
fi

if [[ ! -d "$TARGET" ]]; then
  TARGET="$DEST/Kit-Piloto-Automatico-V30-DISTRIB"
fi

echo
echo "Restaurado em:"
echo "$TARGET"
echo

cd "$TARGET"

missing=0
check_path() {
  local path="$1"
  if [[ -e "$path" ]]; then
    echo "[ok] $path"
  else
    echo "[falta] $path"
    missing=$((missing + 1))
  fi
}

echo "Checando arquivos-chave..."
check_path "00_INDEX.md"
check_path "00_OS/cos.md"
check_path ".env"
check_path ".claude"
check_path ".codex"
check_path "18_AUTOMATION_STACK"
check_path "07_LOGS/task-ledger.md"
echo

{
  echo "# Relatorio de restauracao"
  echo
  echo "Data: $(date)"
  echo "Arquivo de backup: $ARCHIVE"
  echo "Destino: $TARGET"
  echo "Pendencias de arquivos-chave: $missing"
  echo
  echo "## Dependencias"
  echo
  command -v git >/dev/null && echo "- Git: $(git --version)" || echo "- Git: NAO ENCONTRADO"
  command -v python3 >/dev/null && echo "- Python: $(python3 --version 2>&1)" || echo "- Python3: NAO ENCONTRADO"
  command -v node >/dev/null && echo "- Node: $(node --version)" || echo "- Node: NAO ENCONTRADO"
  command -v npm >/dev/null && echo "- npm: $(npm --version)" || echo "- npm: NAO ENCONTRADO"
  echo
  echo "## Proximas acoes"
  echo
  echo "1. Instalar/abrir Codex no Mac novo."
  echo "2. Abrir esta pasta no Codex: $TARGET"
  echo "3. Instalar Google Chrome se ainda nao existir."
  echo "4. Instalar Codex Chrome Extension:"
  echo "   https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg"
  echo "5. Conferir .env e logins antes de rodar automacoes reais."
} > RESTORE-REPORT.md

echo "Relatorio criado:"
echo "$TARGET/RESTORE-REPORT.md"
echo

echo "Proximos passos no Mac novo:"
echo "1. Abra o Codex."
echo "2. Abra a pasta restaurada:"
echo "   $TARGET"
echo "3. Peça: verificar instalacao backup codex"
echo

if [[ "$missing" -gt 0 ]]; then
  echo "Atencao: alguns arquivos-chave nao foram encontrados. Veja RESTORE-REPORT.md."
  exit 2
fi

echo "Restauracao concluida."

