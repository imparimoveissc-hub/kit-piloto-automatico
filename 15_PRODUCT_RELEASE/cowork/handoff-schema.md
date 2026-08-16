# Handoff Schema

Use este schema quando o agente precisar transferir para humano.

```yaml
handoff_status: required
reason:
client_name:
client_contact:
flow:
last_message:
summary:
known_data:
  need:
  urgency:
  offer_interest:
  objections:
  files_or_links:
risk_level: low | medium | high
recommended_next_action:
human_owner:
automation_pause_until:
```

## Regras

- O cliente nao deve repetir informacoes ja coletadas.
- Se risco for `high`, pausar automacao no assunto.
- Retomar apenas quando humano encerrar ou delegar.

