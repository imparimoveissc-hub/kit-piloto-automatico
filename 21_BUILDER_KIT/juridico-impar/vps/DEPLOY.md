# Deploy Jurídico Dashboard — VPS 24/7

## Como funciona

Qualquer push para `main` que altere o arquivo do dashboard dispara
automaticamente o GitHub Actions, que conecta na VPS via SSH e atualiza o
arquivo. Sem QNAX, sem terminal, sem intervenção manual.

## Configuração única (fazer 1 vez)

### 1. Preparar a VPS

Conectar na VPS uma vez só (pelo QNAX, terminal ou qualquer método):

```bash
# Cria a chave SSH para o GitHub Actions usar
ssh-keygen -t ed25519 -C "github-actions-juridico" -f ~/.ssh/github_actions -N ""

# Autoriza a chave na VPS
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys

# Mostra a chave PRIVADA (copiar para o GitHub)
cat ~/.ssh/github_actions
```

Ainda na VPS, roda o setup:

```bash
curl -fsSL https://raw.githubusercontent.com/imparimoveissc-hub/kit-piloto-automatico/main/21_BUILDER_KIT/juridico-impar/vps/setup-vps.sh | bash -s -- juridico.seudominio.com.br
```

### 2. Adicionar secrets no GitHub

Ir em: **github.com/imparimoveissc-hub/kit-piloto-automatico → Settings → Secrets → Actions**

| Secret | Valor |
|--------|-------|
| `VPS_HOST` | IP ou hostname da VPS (ex: `45.123.45.67`) |
| `VPS_USER` | Usuário SSH (geralmente `root` ou `ubuntu`) |
| `VPS_SSH_KEY` | Conteúdo da chave privada `~/.ssh/github_actions` |

### 3. Testar

Fazer qualquer alteração no dashboard e commitar para `main`.
O GitHub Actions vai rodar e o dashboard atualiza em ~30 segundos.

## Monitorar deploys

github.com/imparimoveissc-hub/kit-piloto-automatico → **Actions**

Cada deploy aparece lá com log completo. Se falhar, o GitHub notifica por email.

## Acessar o dashboard

`http://IP_DA_VPS` ou `http://juridico.seudominio.com.br` (após apontar DNS)

Para HTTPS gratuito com Let's Encrypt, rodar na VPS:
```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d juridico.seudominio.com.br
```
