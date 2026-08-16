# Configurar Webhook do Facebook Messenger → Impar

**Objetivo:** Conectar Facebook Marketplace Messenger com o bridge Messenger-WhatsApp para capturar leads automaticamente.

**Status:** 🟡 Pronto para ativar (bridge 100% operacional)

---

## 📋 Pré-requisitos

- ✅ Bridge rodando em `8791`
- ✅ Conta de desenvolvedor no Facebook
- ✅ App do Facebook criado
- ✅ Página do Marketplace da Impar no Facebook
- ✅ Acesso à aba "App Roles" no Facebook

---

## 🔧 Passo 1: Criar/Usar App do Facebook

### 1.1 Acessar Facebook Developers
1. Ir para https://developers.facebook.com/
2. Logar com a conta de desenvolvedor
3. Clicar em "My Apps" → "Create App"

### 1.2 Configurar App
- **App Name:** `impar-marketplace-bridge`
- **App Purpose:** Business
- **Type:** Messenger

---

## 🔌 Passo 2: Configurar Webhook

### 2.1 Ir para Configurações de Webhook
1. No painel do app → **Messenger** → **Settings**
2. Ir até a seção **Webhooks**

### 2.2 Preencher Dados do Webhook
```
Callback URL: http://seu-servidor-publico:8791/webhook/messenger-lead

Verify Token: gerar_token_seguro_aqui
(Exemplo: xK9mP2vL5qR8nJ3wB7xF)

Subscribe to Webhook Fields:
  ☑ messages
  ☑ messaging_postbacks
```

### 2.3 Clicar em "Verify and Save"

---

## 🔑 Passo 3: Obter Access Token

### 3.1 Ir para Token Settings
**Messenger** → **Settings** → **Access Tokens**

### 3.2 Gerar Token
1. Selecionar a página do Impar Marketplace
2. Copiar o **Page Access Token**
3. Guardar em local seguro

---

## 🔐 Passo 4: Subscrever Página ao Webhook

### Via API (Recomendado)
```bash
curl -X POST "https://graph.facebook.com/v18.0/{PAGE_ID}/subscribed_apps?access_token={PAGE_ACCESS_TOKEN}"
```

### Substituir:
- `{PAGE_ID}` = ID da página Impar
- `{PAGE_ACCESS_TOKEN}` = Token do passo 3.2

---

## 📝 Passo 5: Atualizar Configuração Local

### 5.1 Salvar Token em `.env`
```bash
# 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/.env

FACEBOOK_PAGE_ACCESS_TOKEN=seu_token_aqui
FACEBOOK_VERIFY_TOKEN=xK9mP2vL5qR8nJ3wB7xF
FACEBOOK_WEBHOOK_URL=http://seu-servidor-publico:8791/webhook/messenger-lead
```

### 5.2 Validar Configuração
```bash
cd 18_AUTOMATION_STACK/impar-facebook-marketplace-posting

# Testar se bridge responde
curl http://localhost:8791/health

# Testar webhook
curl -X POST http://localhost:8791/webhook/messenger-lead \
  -H "Content-Type: application/json" \
  -d '{"lead_name":"Test","phone":"47999999999","messenger_id":"test_123","message":"teste"}'
```

---

## 🌐 Passo 6: Configurar URL Pública (se necessário)

Se você está testando localmente, precisa expor o bridge para a internet:

### Opção 1: ngrok (Teste)
```bash
brew install ngrok
ngrok http 8791

# Copiar URL gerada (ex: https://abc123.ngrok.io)
# Usar como Callback URL: https://abc123.ngrok.io/webhook/messenger-lead
```

### Opção 2: Servidor Dedicado (Produção)
- Usar servidor dedicado (AWS, Heroku, DigitalOcean)
- URL pública: `http://seu-servidor.com:8791/webhook/messenger-lead`

### Opção 3: Túnel SSH (VPS)
```bash
ssh -R 8791:localhost:8791 user@seu-vps.com
# Acessível em: http://seu-vps.com:8791
```

---

## ✅ Passo 7: Testar Webhook

### 7.1 Simular Mensagem do Marketplace
```bash
curl -X POST https://seu-url-publica:8791/webhook/messenger-lead \
  -H "Content-Type: application/json" \
  -d '{
    "lead_name": "João Silva",
    "phone": "47 99999-0000",
    "messenger_id": "psid_12345",
    "codigo_imovel": "4278482",
    "message": "Tenho interesse nesse imóvel"
  }'
```

### 7.2 Resposta Esperada
```json
{
  "ok": true,
  "whatsapp_to": "47999990000",
  "message": "Olá João\n\nEstávamos conversando no facebook referente ao imóvel\nhttps://impar.com/ap001\n\nGostaria de retirar mais dúvidas? Ou agendar uma visita?",
  "send_result": {
    "sent": true,
    "status": "queued_for_send"
  }
}
```

---

## 📊 Passo 8: Monitorar em Produção

### Ver Logs
```bash
tail -f 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/logs/bridge-$(date +%Y-%m-%d).log
```

### Verificar Leads Recebidos
```bash
grep "facebook" 05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv | tail -10
```

### Dashboard
- Abrir: `05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv`
- Filtrar por `canal_entrada = "facebook"`
- Ver status em tempo real

---

## 🔄 Fluxo Automático (Após Configuração)

```
1. Lead entra no Facebook Marketplace
   └─ Envia mensagem sobre imóvel
      
2. Facebook envia webhook ao bridge
   └─ POST /webhook/messenger-lead
      
3. Bridge processa
   └─ Extrai: nome, telefone, imóvel
   └─ Encontra link do anúncio
   └─ Constrói mensagem D0
      
4. Envia WhatsApp ao lead
   └─ "Olá {{NOME}}, estávamos conversando no facebook..."
   └─ Link do imóvel incluído
      
5. Registra em dashboard
   └─ Adiciona à leads-followup.csv
   └─ Canal: facebook
   └─ Status: em_followup
      
6. Jonata atende
   └─ Vê novo lead no dashboard
   └─ Responde via WhatsApp
   └─ Follow-up automático (D1, D3, etc)
```

---

## 🧪 Troubleshooting

### Webhook não recebe mensagens
**Verificar:**
1. URL pública está acessível? (`curl https://seu-url/health`)
2. Verify Token está correto?
3. Página está subscrita ao webhook?
4. Firewall não está bloqueando porta 8791?

### Mensagens não chegam no WhatsApp
**Verificar:**
1. Bridge está rodando? (`ps aux | grep messenger_to_whatsapp_bridge`)
2. MCP WhatsApp ativo? (`grep IMPAR_WHATSAPP_AUTOMATION .env`)
3. Número do lead está correto? (com código de país)
4. Logs têm erro? (`tail logs/bridge-*.log`)

### Lead não aparece no CSV
**Verificar:**
1. Arquivo existe? (`ls -la leads-followup.csv`)
2. Permissões de escrita? (`chmod 644 leads-followup.csv`)
3. Imóvel foi encontrado? (checar log de `find_property()`)

---

## 🔐 Segurança

- ✅ Usar HTTPS em produção
- ✅ Guardar tokens em `.env` (não no git)
- ✅ Rotacionar tokens periodicamente
- ✅ Validar Verify Token em cada webhook
- ✅ Limitar taxa de requisições (rate limiting)

---

## 📞 Suporte

**Documentação completa:**
- Bridge: `GERENCIAMENTO-BRIDGE.md`
- Fluxo: `FLUXO-MESSENGER-LEADS.md`
- Técnico: `WEBHOOK-MESSENGER-LEADS.md`

**Contato:**
- Bridge rodando em: Port 8791
- Logs: `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/logs/`
- Dashboard: `05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv`

---

## 🎯 Checklist de Ativação

- [ ] App criado no Facebook Developers
- [ ] Webhook configurado (URL + Verify Token)
- [ ] Page Access Token obtido
- [ ] Página subscrita ao webhook
- [ ] `.env` atualizado com tokens
- [ ] Bridge testado localmente
- [ ] URL pública ativa (ngrok/servidor)
- [ ] Webhook testado com curl
- [ ] Leads aparecem no CSV
- [ ] Mensagens chegam no WhatsApp
- [ ] Dashboard monitorado
- [ ] Documentação lida por Jonata

**Quando tudo estiver checado, a automação estará 100% ativa!** 🚀
