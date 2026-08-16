# Guia de Implementação Rápida | BÔNUS

> Tempo total: 15 minutos. Siga na ordem.

## Checklist de Instalação

### Passo 1: Instalar Node.js (2 min)
- [ ] Acesse nodejs.org
- [ ] Baixe a versão LTS
- [ ] Instale (Next, Next, Next, Finish)
- [ ] Abra o terminal e digite: `node --version`
- [ ] Se aparecer um número (ex: v20.11.0), está instalado

### Passo 2: Instalar o Claude Code (3 min)
- [ ] No terminal, digite: `npm install -g @anthropic-ai/claude-code`
- [ ] Aguarde a instalação (30-60 segundos)
- [ ] Digite: `claude --version`
- [ ] Se aparecer a versão, está instalado

### Passo 3: Fazer login (1 min)
- [ ] No terminal, digite: `claude login`
- [ ] O navegador vai abrir
- [ ] Faça login com sua conta Anthropic
- [ ] Volte pro terminal. Deve mostrar "Logged in successfully"

### Passo 4: Copiar os agentes (2 min)
- [ ] Abra a pasta `produto/agentes/` do kit
- [ ] Copie todos os arquivos .md
- [ ] No seu projeto, crie a pasta: `.claude/agents/`
- [ ] Cole os arquivos lá dentro
- [ ] Verifique: deve ter 5 arquivos + README

### Passo 5: Testar o primeiro agente (2 min)
- [ ] No terminal, navegue até seu projeto: `cd seu-projeto`
- [ ] Digite: `claude`
- [ ] Dentro do Claude Code, digite: `Faça um briefing para um cliente de clínica odontológica que quer atrair mais pacientes`
- [ ] O agente de briefing deve gerar um briefing estruturado
- [ ] Se funcionou, todos os agentes estão prontos

### Passo 6: Escolher seus templates (3 min)
- [ ] Abra a pasta `produto/templates/`
- [ ] Identifique seu segmento principal (tráfego, social media, designer, videomaker)
- [ ] Copie a pasta do seu segmento pro seu computador
- [ ] Abra um template e preencha com dados de um cliente real
- [ ] Se o template fez sentido pra sua entrega, está pronto

### Passo 7: Ativar a automação de WhatsApp (2 min)
- [ ] Siga o guia em `docs/setup-whatsapp.md`
- [ ] Conecte seu número comercial
- [ ] Ative o fluxo de atendimento automático
- [ ] Mande uma mensagem teste pro seu número
- [ ] Se recebeu resposta automática, está ativo

---

## Pronto. Seu time de agentes está instalado.

**Próximos passos:**
1. Use os agentes diariamente pra briefing, criação e revisão
2. Personalize os templates com sua marca
3. Explore os 50 prompts da biblioteca conforme a necessidade
4. Ajuste os fluxos de WhatsApp pro seu contexto

**Dica:** Comece pelo agente de briefing com um cliente real. É a forma mais rápida de sentir o poder do kit.
