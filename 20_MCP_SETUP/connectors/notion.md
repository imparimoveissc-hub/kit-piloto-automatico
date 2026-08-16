# Notion — via Composio Rube

## Setup

Notion **via Rube** (`connectors/composio-rube.md`).

Cobre:
- Criar pagina
- Editar pagina
- Buscar database
- Adicionar linha em database
- Comentar
- Compartilhar

## Casos de uso

### CRM em Notion

```text
Toda vez que um lead novo aparecer no WhatsApp,
adiciona linha na database "Leads" do Notion com:
nome, telefone, origem, status: "Novo".
```

### Wiki da empresa

```text
Procura no meu Notion a pagina "Processos de Onboarding".
Resume e me manda.
```

### Documento colaborativo

```text
Cria pagina no Notion "Briefing Cliente X" com o template do
`10_TEMPLATES_OPERACIONAIS/cliente-template/context.md`.
Compartilha com [email do cliente] como editor.
```

## Seguranca

- **Permissao por workspace.** Nao da acesso a workspace pessoal se for usar pra cliente.
- **Read antes de write.** Validar permissao antes de criar/editar.
