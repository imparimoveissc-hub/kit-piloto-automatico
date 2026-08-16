# Audit Checklist — MCPs

> Rodar mensalmente. Garante higiene da stack de MCPs.

## Inventario

- [ ] Listar todos MCPs ativos: `claude mcp list`
- [ ] Pra cada um, perguntar: foi usado nos ultimos 30 dias?
- [ ] MCP nao usado em 30+ dias → remover ou justificar.

## Tokens

- [ ] Pra cada token, conferir validade.
- [ ] Tokens expirados ou expirando em 7 dias → rotacionar.
- [ ] Tokens com escopo excessivo → reduzir.

## Permissoes

- [ ] Auditar log de acessos de cada MCP:
  - Composio: https://app.composio.dev/audit-logs
  - Meta: Business Manager → Configuracoes → Eventos
  - Google: https://myaccount.google.com/security
  - GitHub: Settings → Security log
  - Slack: Workspace Settings → Authentication
- [ ] Acessos suspeitos (horario incomum, IP estranho) → investigar.

## Conexoes

- [ ] Conta MCP com aplicacao desautorizada na origem? Remove a conexao no MCP.
- [ ] Conta MCP que voce nao usa mais? Desconecta.

## Conformidade

- [ ] Tem dados de cliente em MCPs? LGPD compliance:
  - Consentimento documentado?
  - Direito a exclusao funciona?
  - Audit log disponivel?
- [ ] WhatsApp MCP: numero comercial dedicado (nao pessoal)?
- [ ] Clinica/juridico: dados sensiveis nao passam por MCPs sem necessidade?

## Backup

- [ ] Sessao WhatsApp salva e com backup?
- [ ] `.env` local com backup criptografado?
- [ ] Lista de tokens ativos documentada em gerenciador de senhas?

## Documento

Salvar resultado da auditoria em `_DONO_PRODUTO/07_LOGS/mcp-audits/YYYY-MM-DD-audit.md` com:

- Data
- MCPs ativos
- Acoes tomadas (rotacao, remocao, ajuste)
- Pendencias
- Proxima auditoria

## Sinais de alerta

| Sinal | Acao |
|---|---|
| Conta com login fora do horario esperado | Trocar senha + 2FA + revogar tokens |
| MCP autorizado que voce nao reconhece | Revogar imediatamente |
| Notificacao "novo dispositivo conectou" | Conferir, se nao for voce, revogar |
| Uso anormal de quota/API | Pode indicar vazamento de token |
