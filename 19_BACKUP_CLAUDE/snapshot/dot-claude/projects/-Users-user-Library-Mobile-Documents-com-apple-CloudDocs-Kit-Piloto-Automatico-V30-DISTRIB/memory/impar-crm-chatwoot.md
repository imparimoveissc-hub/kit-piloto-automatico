---
name: impar-crm-chatwoot
description: Migração do Papo AI (R$147/mês) para stack próprio Chatwoot + Claude + API Meta na VM Oracle
metadata: 
  node_type: memory
  type: project
  originSessionId: 45c74ff0-2dd2-4dda-a7ed-93d3e9c4e9a8
---

Impar Imóveis vai **substituir o Papo AI (R$147/mês)** por um CRM próprio de custo ~zero, copiando as funções: etiquetas com nome livre, funil inteligente (15 etapas), follow-up com template Meta, multi-atendente com nome, e **EQUIPES (Atendimento, Jurídico, Financeiro, RH)** — o Jonata gosta muito de equipes.

Stack (3 camadas):
1. **API oficial da Meta em modo COEXISTÊNCIA** (Jonata quer responder pelo celular WhatsApp Business E pelo CRM ao mesmo tempo — isso exige o fluxo Embedded Signup/Coexistence, normalmente via BSP tipo 360dialog; NÃO a migração padrão, que tira o número do app). Número: 47 92002-6017 / 5547920026017. Regra: abrir o app a cada 14 dias senão a API cai. CORRIGE conselho antigo de que "o número sai do app".
2. **Chatwoot** (open-source) hospedado na **VM Oracle 163.176.220.163** (mesma do n8n) = a "cara" do CRM (inbox de time, etiquetas, equipes, funil, assinatura por atendente).
3. **Cérebro Claude** via n8n (Claude Haiku 4.5 em produção) = responde, etiqueta, move no funil, roteia p/ equipe, coleta documento, agenda visita, handoff pro Jonata.

Pacote pronto em `05_WORKSPACE/clientes/impar-imoveis/whatsapp/chatwoot/`: `PLANO.md`, `instalacao-oracle.md`, `cerebro-atendimento.md`. Master prompt em `../master-prompt-papo-ai.txt`.

Papo AI atual: agente "Assistente Impar Imóveis" em gpt-4.1-mini, conectado ao 5547920026017, Funil Imobiliária com 15 etapas e 39 leads.

**Descoberta 2026-07-04:** a VM Oracle atual (163.176.220.163) tem só **956 MB RAM e SEM Docker** — pequena demais pro Chatwoot (algo já roda na :8080). NÃO instalar lá. Jonata **não tem cartão de crédito no momento e achou VPS caro** → decisão: usar o **Oracle Ampere A1 Always Free** (ARM, até 4 OCPU/24GB, grátis) na **conta Oracle que ele JÁ tem** (a cota ARM ainda não foi usada — só a AMD micro). Zero custo, zero cartão novo. Risco: "out of capacity" do A1 grátis (tentar outro AD/horário). Subdomínio: NÃO precisa comprar — registro DNS grátis no imparimoveis.com.

**Servidor escolhido (2026-07-04):** Oracle A1 deu "out of capacity" em SP (AD-1 único). Jonata sem cartão de bom limite → vai de **VPS QNAX plano "Value"**: 2 vCPU, **6 GB RAM**, 50 GB NVMe, **R$69,90/mês MENSAL sem fidelidade**, datacenter SP/BR, paga PIX/boleto/cartão. (Ele topou passar dos R$40 pra ter RAM p/ mais projetos.)

**Chave SSH já gerada** no Mac: `~/.ssh/id_ed25519_chatwoot` (pública: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA22aCsJRSDAqpYJPJTK7C9TmZY2p9z6C1Hs0piOYbaf chatwoot-impar-oracle`).

**INSTALADO 2026-07-04:** VPS QNAX ativo, IP **45.140.193.77** (root, acesso por chave `~/.ssh/id_ed25519_chatwoot`). Chatwoot rodando via Docker em `/root/chatwoot` (compose+.env com senhas geradas). Swap 2GB + Docker 29.6. **HTTPS via Caddy + domínio temporário `https://45-140-193-77.sslip.io`** (proxy p/ localhost:3000; porta 3000 tb exposta como fallback). Conta admin: Account "Impar Imóveis", user jonata_oliveira@outlook.com.br. Criados: **5 equipes** (Atendimento, SAC, Juridico, Financeiro, RH), **12 etiquetas**, **funil de 15 etapas** (custom attribute conversa `etapa_funil`), **Agent Bot "Cerebro Impar (IA)"** scaffold (id=1, token kLxuZ6e6f9GX4eCQzfcNVZAe, outgoing_url placeholder localhost:5678).

**Pendente:** (a) trocar sslip.io por **crm.imparimoveis.com** (Jonata aponta DNS A → 45.140.193.77, aí ajusto Caddyfile+FRONTEND_URL); (b) **cérebro LIVE** precisa: inbox WhatsApp + chave de API de LLM (recomendo Claude) + glue (n8n ou serviço webhook) ligando Agent Bot↔LLM↔Chatwoot; (c) **conectar WhatsApp** via Meta coexistência (credenciais Phone Number ID+Token) — fase final; (d) convidar Sidnei como agente.

**How to apply:** ao retomar, confirmar os 3 pendentes; instalar Chatwoot via Docker; criar equipes/etiquetas/funil; plugar o cérebro via n8n; migrar os 39 leads; testar e desligar o Papo AI. Ver [[impar-followup-leads-email]].
