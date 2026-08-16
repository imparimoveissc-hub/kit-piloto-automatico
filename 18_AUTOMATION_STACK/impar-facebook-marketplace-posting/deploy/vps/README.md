# Deploy VPS - Messenger Marketplace Impar

Status: pacote preparado, ativacao real depende de acesso SSH e conectores autorizados.

## Objetivo

Rodar a ponte `Messenger -> WhatsApp` em uma VPS para tirar a dependencia do MacBook ligado.

Este pacote sobe o servico HTTP que recebe eventos normalizados em:

```text
POST /webhook/messenger-lead
```

Por seguranca, ele inicia com:

```text
MESSENGER_BRIDGE_DRY_RUN=true
MESSENGER_BRIDGE_BIND_HOST=127.0.0.1
```

Assim ele grava outbox/logs, mas nao envia mensagem real enquanto os webhooks autorizados nao forem validados.

## O que a VPS resolve

- Mantem a ponte online 24/7 via `systemd`.
- Recebe eventos de um conector externo como n8n, Chatwoot, Cowork ou Meta webhook autorizado.
- Gera resposta Messenger, abertura WhatsApp e alerta interno respeitando D0 unico e limite de follow-up.
- Remove a necessidade do MacBook para o runtime da ponte.

## O que ainda precisa de canal oficial

Facebook Marketplace/Messenger lido por navegador logado nao fica 100% resolvido apenas com VPS. Para operar sem MacBook, escolha uma destas rotas:

1. Rota recomendada: Meta/Chatwoot/n8n/Cowork envia payload normalizado para a ponte na VPS.
2. Rota alternativa: VPS com ambiente grafico + Chrome persistente + login manual no Facebook, parando em captcha, 2FA ou checkpoint.

A primeira rota e mais estavel. A segunda ainda depende de sessao de navegador e pode bloquear por seguranca do Facebook.

## Requisitos da VPS

- Ubuntu 22.04/24.04 ou Debian 12.
- 1 vCPU e 1 GB RAM para a ponte; 2 GB+ se tambem rodar navegador.
- Python 3.
- Dominio ou tunnel HTTPS se o webhook precisar ser publico.
- SSH root ou usuario com `sudo`.

## Instalacao

1. Enviar este kit para a VPS em:

```text
/opt/impar/kpa30
```

2. Rodar:

```bash
cd /opt/impar/kpa30
sudo bash 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/deploy/vps/install-vps.sh
```

3. Editar os segredos:

```bash
sudo nano /etc/impar/messenger-bridge.env
```

4. Reiniciar:

```bash
sudo systemctl restart impar-messenger-bridge
```

5. Validar:

```bash
curl http://127.0.0.1:8791/health
sudo journalctl -u impar-messenger-bridge -n 80 --no-pager
```

## HTTPS publico

Use o `Caddyfile.example` como base. Troque:

```text
messenger.impar.example.com
```

pelo dominio real.

Se preferir Cloudflare Tunnel, mantenha a ponte em `127.0.0.1:8791` e publique apenas `/webhook/messenger-lead` e `/health`.

## Payload de teste

```bash
curl -X POST http://127.0.0.1:8791/webhook/messenger-lead \
  -H "Content-Type: application/json" \
  -d '{
    "lead_name": "Lead Teste",
    "phone": "47 99999-0000",
    "messenger_id": "psid_teste_123",
    "codigo_imovel": "4278482",
    "message": "Tenho interesse nesse apartamento para locacao e posso visitar."
  }'
```

## Ativacao real

Antes de trocar `MESSENGER_BRIDGE_DRY_RUN=false`, validar:

- webhook do WhatsApp envia pela conta correta da Impar;
- webhook do Messenger responde no canal correto;
- alerta interno vai para `554796876631`;
- nenhum alerta duplicado e gerado para o mesmo telefone no mesmo dia;
- D0/link nao e reenviado para lead ja tratado;
- rollback testado: voltar `MESSENGER_BRIDGE_DRY_RUN=true` e reiniciar o servico.

## Comandos operacionais

```bash
sudo systemctl status impar-messenger-bridge
sudo systemctl restart impar-messenger-bridge
sudo journalctl -u impar-messenger-bridge -f
```
