#!/usr/bin/env bash
set -u

# Validate Messenger Bridge configuration before deployment
# Run: bash validate-config.sh

echo "🔍 Validating Impar Messenger Bridge Configuration..."
echo ""

ERRORS=0
WARNINGS=0

# Load env file if exists
if [ -f "/etc/impar/messenger-bridge.env" ]; then
    echo "📄 Loading /etc/impar/messenger-bridge.env..."
    source /etc/impar/messenger-bridge.env
else
    echo "⚠️ WARNING: /etc/impar/messenger-bridge.env not found (will use defaults)"
    ((WARNINGS++))
fi

# Check required variables
echo ""
echo "Checking configuration..."

check_var() {
    local var_name=$1
    local var_value="${!var_name:-}"

    if [ -z "$var_value" ]; then
        echo "  ❌ $var_name: NOT SET"
        ((ERRORS++))
    else
        echo "  ✅ $var_name: OK (${#var_value} chars)"
    fi
}

check_var "WHATSAPP_SEND_WEBHOOK_URL"
check_var "WHATSAPP_SEND_TOKEN"
check_var "MESSENGER_SEND_WEBHOOK_URL"
check_var "MESSENGER_SEND_TOKEN"

echo ""
echo "Checking optional/defaults..."
echo "  MESSENGER_BRIDGE_BIND_HOST: ${MESSENGER_BRIDGE_BIND_HOST:-0.0.0.0}"
echo "  MESSENGER_BRIDGE_PORT: ${MESSENGER_BRIDGE_PORT:-8791}"
echo "  MESSENGER_BRIDGE_DRY_RUN: ${MESSENGER_BRIDGE_DRY_RUN:-false}"

# Check file system
echo ""
echo "Checking file system..."
WORKSPACE="/opt/impar/kpa30/05_WORKSPACE/clientes/impar-imoveis"
if [ -d "$WORKSPACE" ]; then
    echo "  ✅ Workspace directory exists: $WORKSPACE"
    if [ -w "$WORKSPACE" ]; then
        echo "  ✅ Workspace is writable"
    else
        echo "  ❌ Workspace is NOT writable (as impar user?)"
        ((ERRORS++))
    fi
else
    echo "  ⚠️ Workspace directory not found: $WORKSPACE"
    ((WARNINGS++))
fi

# Check Python dependencies
echo ""
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    echo "  ✅ python3 found: $(python3 --version)"
else
    echo "  ❌ python3 not found"
    ((ERRORS++))
fi

# Check systemd
echo ""
echo "Checking systemd service..."
if systemctl list-unit-files 2>/dev/null | grep -q "impar-messenger-bridge"; then
    echo "  ✅ Service file registered"
else
    echo "  ⚠️ Service file not registered (run: sudo systemctl daemon-reload)"
    ((WARNINGS++))
fi

# Summary
echo ""
echo "=================================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ Configuration is VALID - Ready for deployment"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Configuration has $WARNINGS warnings - Deployable with caution"
    exit 0
else
    echo "❌ Configuration has $ERRORS ERRORS - Fix before deploying"
    exit 1
fi
