---
module: Contratos
lastModified: 2026-07-26
status: ativo
---

## Objetivo

Gerenciar contratos de locação da Impar Imóveis: geração, revisão, acompanhamento de reajustes anuais
e alertas de vencimento de vigência antes dos prazos fecharem.

---

## Plugin e configuração

| Item | Localização |
|------|-------------|
| Plugin | `imobiliario-juridico` (KPA30-Marketplace) |
| Config da prática | `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md` |
| Perfil da imobiliária | Preenchido durante cold-start-interview |

---

## Skills disponíveis

| Skill | Disparo | O que faz |
|-------|---------|-----------|
| `imobiliario-juridico:gerar-contrato-locacao` | "gerar contrato", "novo contrato" | Gera contrato completo com dados do locatário/imóvel |
| `imobiliario-juridico:revisar-contrato-locacao` | "revisar contrato", colar texto | Revisão jurídica e de completude |
| `imobiliario-juridico:acompanhar-reajuste` | "quais contratos reajustam", "o que vence" | Lista eventos próximos de reajuste/vencimento |
| `imobiliario-juridico:cold-start-interview` | "configurar plugin", primeira instalação | Onboarding do perfil da imobiliária |

---

## Tarefas agendadas

| Task ID | Schedule | Mecanismo | Status |
|---------|---------|-----------|--------|
| `vigia-reajustes-semanal` | Segunda-feira 8h | MCP scheduled-tasks | desativado (enabled: false) |

**Agente sob demanda:**
- `imobiliario-juridico:vigia-reajustes` — pode ser invocado manualmente ou agendado

---

## Dados de contratos

O registro de reajustes/vigências é mantido pelo plugin na config localizada em:
`~/.claude/plugins/config/kpa30/imobiliario-juridico/`

Consultar o plugin via skill antes de abrir qualquer arquivo de contrato.

---

## Fluxo de geração de contrato

```
Usuário informa: locatário, imóvel, valor, prazo, índice de reajuste
    ↓
Skill gerar-contrato-locacao monta documento
    ↓
Skill revisar-contrato-locacao valida cláusulas
    ↓
Output em 06_OUTPUTS/ (docx ou md)
    ↓
Registro no acompanhamento de reajuste (entrada automática via skill)
```

---

## Fluxo de alerta de reajuste

```
vigia-reajustes-semanal dispara (segunda 8h) ou manual
    ↓
Lê registro de contratos com eventos próximos
    ↓
Filtra: reajuste ≤ 30 dias | vencimento ≤ 60 dias
    ↓
Posta alertas no WhatsApp Jonata com prazos e ação necessária
```

---

## Como diagnosticar sem abrir código

1. **Quais contratos reajustam?** Invocar skill `imobiliario-juridico:acompanhar-reajuste`.
2. **Plugin não configurado?** Checar `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md` — se tiver `[PREENCHER]`, rodar cold-start-interview.
3. **Vigia desativada?** Habilitar via MCP: `update_scheduled_task(taskId: "vigia-reajustes-semanal", enabled: true)`.
4. **Contrato gerado com dados errados?** Verificar perfil da imobiliária na config do plugin.

---

## Problemas conhecidos

- `vigia-reajustes-semanal` está desativada (enabled: false) — reativar quando necessário.
- Plugin requer cold-start-interview na instalação em nova máquina (config não sincronizada via iCloud).
