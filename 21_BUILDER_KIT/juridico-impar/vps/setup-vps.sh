#!/bin/bash
# setup-vps.sh — rodar UMA VEZ na VPS como root
# Configura nginx para servir o dashboard jurídico 24/7

set -e

DOMAIN="${1:-juridico.impar.local}"
DEPLOY_DIR=/var/www/juridico-impar
REPO_DIR=/opt/kit-piloto-automatico
GIT_REPO="https://github.com/imparimoveissc-hub/kit-piloto-automatico.git"

echo "=== Setup VPS Jurídico Impar ==="
echo "Domínio: $DOMAIN"
echo "Pasta deploy: $DEPLOY_DIR"

# Dependências
apt-get update -qq
apt-get install -y nginx git

# Clona o repositório
if [ ! -d "$REPO_DIR/.git" ]; then
  git clone "$GIT_REPO" "$REPO_DIR"
else
  cd "$REPO_DIR" && git pull origin main
fi

# Cria pasta pública e copia dashboard
mkdir -p "$DEPLOY_DIR"
cp "$REPO_DIR/21_BUILDER_KIT/juridico-impar/juridico-dashboard.html" "$DEPLOY_DIR/index.html"

# Configura nginx
cat > /etc/nginx/sites-available/juridico-impar <<NGINX
server {
    listen 80;
    server_name $DOMAIN;

    root $DEPLOY_DIR;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
        add_header Cache-Control "no-cache, must-revalidate";
    }

    # Bloqueia acesso a arquivos ocultos
    location ~ /\. {
        deny all;
    }
}
NGINX

# Ativa o site
ln -sf /etc/nginx/sites-available/juridico-impar /etc/nginx/sites-enabled/
nginx -t
systemctl enable nginx
systemctl reload nginx

echo ""
echo "✅ Setup concluído!"
echo "   Dashboard disponível em: http://$DOMAIN"
echo ""
echo "Próximo passo: adicionar os 3 secrets no GitHub:"
echo "   VPS_HOST  → IP ou hostname da VPS"
echo "   VPS_USER  → usuário SSH (ex: root ou ubuntu)"
echo "   VPS_SSH_KEY → chave privada SSH (cat ~/.ssh/id_ed25519)"
