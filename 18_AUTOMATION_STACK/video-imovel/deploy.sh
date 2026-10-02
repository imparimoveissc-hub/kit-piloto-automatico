#!/bin/bash
# IMPAR STUDIO — Deploy na VPS (Ubuntu 22.04+)
set -e

APP_DIR="/opt/impar-studio"
REPO="https://github.com/imparimoveissc-hub/kit-piloto-automatico.git"
BRANCH="claude/nifty-mccarthy-3roe2r"
SRC_PATH="18_AUTOMATION_STACK/video-imovel"
PORT=5001

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     IMPAR STUDIO — Deploy VPS        ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── 1. Dependências do sistema ────────────────────────────────
echo "▶ Instalando dependências do sistema..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv ffmpeg git curl

# ── 2. Clone / atualiza o repo ────────────────────────────────
echo "▶ Clonando repositório..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR"
    git fetch origin "$BRANCH"
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
else
    git clone --branch "$BRANCH" --depth 1 "$REPO" "$APP_DIR"
fi

# ── 3. Virtualenv + dependências Python ───────────────────────
echo "▶ Instalando dependências Python..."
cd "$APP_DIR/$SRC_PATH"
python3 -m venv .venv
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q flask pillow moviepy requests

# ── 4. Cria arquivo .env se não existir ───────────────────────
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "▶ .env criado (edite para adicionar REPLICATE_API_TOKEN se quiser)"
fi

# ── 5. Cria diretórios de runtime ─────────────────────────────
mkdir -p uploads outputs

# ── 6. Serviço systemd ────────────────────────────────────────
echo "▶ Configurando serviço systemd..."
cat > /etc/systemd/system/impar-studio.service << UNIT
[Unit]
Description=IMPAR STUDIO
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR/$SRC_PATH
ExecStart=$APP_DIR/$SRC_PATH/.venv/bin/python3 app.py
Restart=always
RestartSec=5
Environment=PORT=$PORT
EnvironmentFile=-$APP_DIR/$SRC_PATH/.env

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable impar-studio
systemctl restart impar-studio

# ── 7. Abre porta no firewall (ufw se ativo) ──────────────────
if command -v ufw &>/dev/null && ufw status | grep -q "Status: active"; then
    ufw allow $PORT/tcp
fi

# ── 8. Verifica ───────────────────────────────────────────────
sleep 3
if curl -sf "http://localhost:$PORT/" > /dev/null; then
    echo ""
    echo "╔══════════════════════════════════════╗"
    echo "║  ✅  IMPAR STUDIO rodando!            ║"
    echo "║                                      ║"
    printf "║  🌐  http://%-25s  ║\n" "$(curl -sf ifconfig.me 2>/dev/null || echo '45.140.193.77'):$PORT"
    echo "╚══════════════════════════════════════╝"
else
    echo "⚠ Servidor não respondeu — verifique:"
    echo "  journalctl -u impar-studio -n 30"
fi
