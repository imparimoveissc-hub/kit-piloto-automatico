---
name: criar
description: Gera conteudo, copy, posts, relatorios e materiais
---

# /criar — Criar Conteudo

## Processo

### 1. Ler contexto
Leia `.claude/config.md` pra saber segmento e tom de voz.

### 2. Identificar a demanda
Pergunte: "O que precisa criar?"

Se o usuario mencionar um cliente, leia o briefing em `clientes/[nome]/briefing.md`.

### 3. Tipos de criacao (adaptar ao segmento)

**Copy de anuncio:**
- Gere 5 variacoes com: headline, texto, CTA
- Adapte ao canal (Facebook, Instagram, Google)

**Post de feed:**
- Gere copy + sugestao de visual + hashtags
- Formato: carrossel, estático ou video

**Roteiro de Reels/Stories:**
- Hook (0-3s), corpo, CTA
- Texto na tela + narração

**Calendario editorial:**
- 7 dias, 1-2 posts por dia
- Formato, pilar, copy, horario

**Email:**
- Assunto + corpo + CTA
- Variações pra teste A/B

**Relatorio (basico):**
- Use /relatorio pra relatorios completos

**Proposta:**
- Use /proposta pra propostas comerciais

**Peca juridica (advocacia):**
- Estrutura organizacional, nao conteudo juridico
- Organiza argumentos e referencias

**Material de vendas (B2B):**
- Deck, one-pager, case study

**Conteudo pra clinica:**
- Posts educativos, FAQ de procedimentos

### 4. Gerar

Ao gerar qualquer conteudo:
- Use o tom de voz do config.md
- Adapte ao publico do cliente (do briefing)
- Entregue PRONTO PRA USAR (copiar e colar)
- Quando fizer sentido, gere 2-3 variacoes

### 5. Proximo passo
Pergunte: "Material criado. Quer que eu revise antes de entregar? (/revisar)"
