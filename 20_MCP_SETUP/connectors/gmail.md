# Gmail — via Composio Rube

## Setup

Gmail **via Rube** (`connectors/composio-rube.md`).

Cobre:
- Enviar email
- Ler caixa de entrada
- Buscar
- Marcar como lido/lido
- Adicionar label
- Criar rascunho

## Casos de uso

### Follow-up automatico

```text
Pega leads no HubSpot que receberam proposta ha +5 dias sem resposta.
Pra cada um, monta email de follow-up usando template
`15_PRODUCT_RELEASE/prompts/05-whatsapp.md` (adaptado pra email).
Salva como rascunho no Gmail pra eu revisar.
```

### Triagem de inbox

```text
Le todos emails nao lidos das ultimas 24h.
Classifica em: cliente / lead / spam / interno / outros.
Me lista os de cliente com resumo.
```

### Newsletter / sequencia

```text
Cria 5 rascunhos no Gmail pra sequencia de onboarding de novo cliente.
Cada um com 2-3 dias de intervalo. Tom acolhedor profissional.
```

## Seguranca

- **Sempre rascunho antes de enviar.** Confirmacao humana.
- **Nunca enviar em massa sem permissao explicita.**
- **Cuidado com filtros.** Email mal-formatado vai pra spam.
