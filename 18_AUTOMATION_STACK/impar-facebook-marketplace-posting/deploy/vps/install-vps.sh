#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/impar/kpa30}"
SERVICE_NAME="impar-messenger-bridge"
RUN_USER="${RUN_USER:-impar}"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Rode como root: sudo bash deploy/vps/install-vps.sh"
  exit 1
fi

if [[ ! -d "$APP_DIR" ]]; then
  echo "APP_DIR nao existe: $APP_DIR"
  echo "Envie o kit para a VPS antes, por exemplo em /opt/impar/kpa30."
  exit 1
fi

if ! id "$RUN_USER" >/dev/null 2>&1; then
  useradd --system --home-dir /opt/impar --shell /usr/sbin/nologin "$RUN_USER"
fi

mkdir -p /etc/impar
if [[ ! -f /etc/impar/messenger-bridge.env ]]; then
  cp "$APP_DIR/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/deploy/vps/env.example" /etc/impar/messenger-bridge.env
  chmod 600 /etc/impar/messenger-bridge.env
fi

chown -R "$RUN_USER:$RUN_USER" /opt/impar
cp "$APP_DIR/18_AUTOMATION_STACK/impar-facebook-marketplace-posting/deploy/vps/${SERVICE_NAME}.service" "/etc/systemd/system/${SERVICE_NAME}.service"

systemctl daemon-reload
systemctl disable --now "$SERVICE_NAME" 2>/dev/null || true
echo "$SERVICE_NAME instalado, mas mantido desabilitado ate reconexao explicitamente solicitada."
