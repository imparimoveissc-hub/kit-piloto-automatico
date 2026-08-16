# Time de Agentes IA — Kit Piloto Automatico

Cinco agentes especializados que automatizam 90% da entrega do seu servico digital.
Cada agente funciona independente. Voce pode usar um, dois ou todos juntos.

---

## Instalacao

### Pre-requisito
- Claude Code instalado e funcionando no seu computador

### Passo 1 — Copiar os agentes

Copie a pasta `agentes/` para dentro do seu projeto:

```
seu-projeto/
├── .claude/
│   └── agents/          <-- colar os 5 arquivos .md aqui
│       ├── briefing-agent.md
│       ├── criacao-agent.md
│       ├── revisao-agent.md
│       ├── entrega-agent.md
│       └── relatorio-agent.md
├── clientes/
│   └── [nome-do-cliente]/
│       └── briefing.md
└── CLAUDE.md
```

### Passo 2 — Verificar

Abra o Claude Code no terminal e digite:

```
/agents
```

Voce deve ver os 5 agentes listados. Se aparecerem, esta pronto.

### Passo 3 — Usar

Para chamar um agente especifico:

```
@briefing-agent Preciso fazer um briefing pro meu cliente novo de trafego
```

Ou simplesmente descreva o que precisa e o Claude vai usar o agente certo.

---

## Os 5 Agentes

### 1. Briefing Agent (`briefing-agent.md`)
**O que faz:** Extrai escopo do cliente e gera briefing estruturado.

**Quando usar:**
- Cliente novo chegou
- Precisa alinhar escopo antes de comecar
- Quer organizar informacoes soltas num documento padrao

**Exemplo:**
```
@briefing-agent Meu cliente e a Loja Bella, e-commerce de moda feminina.
Preciso montar o briefing de social media pra ela.
```

---

### 2. Criacao Agent (`criacao-agent.md`)
**O que faz:** Gera conteudo profissional adaptado ao segmento.

**Quando usar:**
- Precisa criar copys de anuncio
- Precisa montar calendario de conteudo
- Precisa de roteiros de reels ou scripts de video
- Precisa de planejamento de campanha
- Precisa de briefing de criativos

**Exemplo:**
```
@criacao-agent Cria 5 copys de anuncio de conversao pra essa loja de cosmeticos.
O publico e mulheres 25-40, tom descontraido, foco em resultados rapidos.
```

---

### 3. Revisao Agent (`revisao-agent.md`)
**O que faz:** Revisa qualquer conteudo com olho critico.

**Quando usar:**
- Antes de enviar qualquer entrega pro cliente
- Pra verificar ortografia, tom de voz e consistencia
- Pra comparar o conteudo com o briefing original

**Exemplo:**
```
@revisao-agent Revisa essas copys antes de eu mandar pro cliente.
O tom precisa ser profissional mas acessivel. [cola as copys]
```

---

### 4. Entrega Agent (`entrega-agent.md`)
**O que faz:** Organiza tudo em pacote profissional de entrega.

**Quando usar:**
- Conteudo revisado e pronto, precisa organizar
- Precisa montar estrutura de pastas
- Precisa escrever a mensagem de entrega pro cliente

**Exemplo:**
```
@entrega-agent Organiza tudo que criei pro cliente Casa Verde
num pacote de entrega de social media pra abril.
```

---

### 5. Relatorio Agent (`relatorio-agent.md`)
**O que faz:** Monta relatorios de performance com analise e recomendacoes.

**Quando usar:**
- Precisa do relatorio semanal/mensal do cliente
- Tem dados e quer analise rapida
- Precisa de template de relatorio por segmento

**Exemplo:**
```
@relatorio-agent Monta o relatorio semanal da campanha.
Gastei R$2.500, gerei 87 leads, 3 vendas de R$1.200 cada.
Meta de CPL era R$35.
```

---

## Fluxo Completo (usar todos juntos)

Para uma entrega completa, a ordem recomendada e:

```
1. Briefing Agent   → Coleta escopo e gera briefing
2. Criacao Agent    → Usa o briefing pra criar conteudo
3. Revisao Agent    → Revisa o conteudo gerado
4. Entrega Agent    → Organiza e prepara pra enviar
5. Relatorio Agent  → Analisa resultados depois da execucao
```

Voce NAO precisa usar todos. Cada um funciona sozinho. Use o que precisar.

---

## Segmentos Suportados

| Segmento | Briefing | Criacao | Revisao | Entrega | Relatorio |
|----------|----------|---------|---------|---------|-----------|
| Gestor de Trafego | sim | sim | sim | sim | sim |
| Social Media | sim | sim | sim | sim | sim |
| Designer | sim | sim | sim | sim | sim |
| Videomaker | sim | sim | sim | sim | sim |

---

## Dicas

1. **Comece pelo Briefing Agent** mesmo que ja tenha as informacoes — ele organiza tudo num formato padrao que os outros agentes entendem melhor.

2. **Copie o briefing gerado** e cole quando chamar o Criacao Agent. Quanto mais contexto, melhor o output.

3. **Sempre passe pelo Revisao Agent** antes de enviar pro cliente. Ele pega coisas que voce nao percebe.

4. **Use o Relatorio Agent toda semana.** Mesmo um relatorio simples mostra profissionalismo e justifica o servico.

5. **Personalize os agentes.** Edite os arquivos .md pra adicionar informacoes especificas do seu negocio, seus templates preferidos ou regras da sua agencia.

---

## Problemas Comuns

| Problema | Solucao |
|----------|---------|
| Agente nao aparece no /agents | Verifique se os arquivos estao em `.claude/agents/` (com ponto antes de claude) |
| Output generico demais | De mais contexto — cole o briefing, descreva o nicho, especifique o tom |
| Tom de voz errado | Adicione no prompt: "o tom do cliente e [descreva]" |
| Formato errado | Especifique: "formato de post de Instagram" ou "formato de anuncio Meta" |

---

## Suporte

Qualquer duvida, entre no grupo da Tropa do Choque ou mande mensagem no suporte.
