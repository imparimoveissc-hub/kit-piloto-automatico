#!/usr/bin/env bash
# Sobe o listener de emissão de nota por WhatsApp.
# Pré-requisito: rodar antes `python3 -m src.cli login-manual` (salva a sessão).
set -euo pipefail
cd "$(dirname "$0")"
exec python3 -m src.whatsapp_listener
