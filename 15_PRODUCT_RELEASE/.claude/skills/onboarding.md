---
name: onboarding
description: Inicia onboarding de cliente novo
---

# /onboarding — Onboarding de Cliente Novo

## Processo

### 1. Coletar dados do cliente
Pergunte:
- "Nome do cliente?"
- "Empresa?"
- "Contato (WhatsApp/email)?"
- "Qual servico contratou?"
- "Quando comeca?"

### 2. Criar estrutura

```bash
mkdir -p clientes/[nome-cliente-kebab]/entregas
mkdir -p clientes/[nome-cliente-kebab]/relatorios
```

### 3. Gerar checklist de onboarding

```markdown
# Onboarding — [Nome do Cliente]
Data inicio: [data]
Servico: [servico contratado]

## Checklist

### Dia 1 — Boas-vindas
- [ ] Enviar mensagem de boas-vindas
- [ ] Compartilhar cronograma
- [ ] Solicitar acessos necessarios
- [ ] Agendar kickoff

### Semana 1 — Setup
- [ ] Receber acessos (plataformas, redes, ferramentas)
- [ ] Fazer briefing completo (/briefing)
- [ ] Configurar ferramentas
- [ ] Definir rotina de comunicacao

### Semana 2 — Primeira entrega
- [ ] Entregar primeiro material
- [ ] Coletar feedback
- [ ] Ajustar processo se necessario

### Mensal
- [ ] Enviar relatorio (/relatorio)
- [ ] Reuniao de alinhamento
- [ ] Revisar escopo se necessario
```

### 4. Gerar mensagem de boas-vindas

**WhatsApp:**
```
Oi [nome], tudo bem? Aqui e [seu nome] da [empresa].

Bem-vindo(a)! Vamos comecar o projeto de [servico].

Pra gente iniciar com o pe direito, preciso de algumas coisas:

1. Acesso a [plataforma/rede/ferramenta]
2. Logo e identidade visual (se tiver)
3. Materiais de referencia (o que gosta e o que nao gosta)

Nosso proximo passo: [kickoff/briefing] em [data].

Qualquer duvida, estou por aqui.
Abraco!
```

### 5. Salvar
Salve checklist em `clientes/[nome]/onboarding.md`

### 6. Proximo passo
Pergunte: "Onboarding criado. Quer montar o briefing completo agora? (/briefing)"
