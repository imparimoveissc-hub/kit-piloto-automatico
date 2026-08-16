# Guia de Referência Rápida | Kit Piloto Automático com IA

## Instalação (15 minutos)

### Passo 1: Instalar o Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```
Se der erro de permissão no Windows, abra o terminal como Administrador.

### Passo 2: Fazer login
```bash
claude login
```
Vai abrir o navegador. Faça login com sua conta Anthropic.

### Passo 3: Copiar os agentes
Copie a pasta `agentes/` pra dentro do seu projeto:
```bash
cp -r agentes/ seu-projeto/.claude/agents/
```

### Passo 4: Copiar os templates
Copie a pasta `templates/` pra qualquer lugar do seu computador. Recomendo:
```
Documentos/kit-piloto-automatico/templates/
```

### Passo 5: Testar
```bash
cd seu-projeto
claude
```
Dentro do Claude Code, digite:
```
/briefing-agent
```
Se aparecer o agente, está tudo instalado.

---

## Comandos do Dia a Dia

| O que você quer fazer | Comando |
|-----------------------|---------|
| Montar briefing de cliente | `/briefing-agent` |
| Criar conteúdo/copy | `/criacao-agent` |
| Revisar o que foi criado | `/revisao-agent` |
| Formatar pra entrega | `/entrega-agent` |
| Montar relatório | `/relatorio-agent` |

---

## Como Usar os Templates

1. Abra a pasta `templates/` no seu computador
2. Escolha seu segmento (tráfego, social media, designer, videomaker)
3. Copie o template que precisa
4. Preencha os campos marcados com `[PREENCHER]`
5. Entregue pro cliente

---

## Como Usar os Prompts

1. Abra a pasta `prompts/`
2. Escolha a categoria (briefing, criação, revisão, relatório, whatsapp)
3. Copie o prompt que precisa
4. Cole no Claude Code, Claude ou ChatGPT
5. Substitua os placeholders ([NOME DO CLIENTE], [NICHO], etc.)
6. Use o resultado

---

## Automação de WhatsApp

1. Configure seguindo o guia em `docs/setup-whatsapp.md`
2. Conecte seu número
3. Ative os fluxos (atendimento, follow-up, onboarding)
4. Os fluxos rodam sozinhos 24h

---

## Precisa de Ajuda?

- Consulte o `troubleshooting.md` pra problemas comuns
- Consulte o `glossario.md` pra termos que não conhece
- Consulte o `faq.md` pra perguntas frequentes
