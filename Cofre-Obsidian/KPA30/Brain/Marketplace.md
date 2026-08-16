---
module: Marketplace
lastModified: 2026-07-26
status: ativo
---

## Objetivo

Publicar imóveis da Impar Imóveis no Facebook Marketplace e em 96 grupos aprovados.
Pipeline 100% automático: geração de fila → publicação diária → crosspost em grupos (3 turnos).

---

## Arquivos principais

| Arquivo | Propósito |
|---------|-----------|
| `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/publish_groups_playwright.py` | Crosspost nos 96 grupos (Playwright) |
| `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/MECANICO-IMPAR-PROCEDIMENTOS.md` | Procedimentos técnicos, erros comuns, contatos |
| `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/deploy/` | Scripts de deploy e configuração |
| `05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/grupos-aprovados.csv` | 96 grupos aprovados (não editar sem validar) |
| `~/.local/impar-automation/marketplace/queue.json` | Fila de publicações (estado ativo) |

---

## Tarefas agendadas

| Task ID | Frequência | Mecanismo | O que faz |
|---------|-----------|-----------|-----------|
| `impar-marketplace-grupos-manha` | 11:30 diário | LaunchAgent (plist) | Crosspost turno manhã nos 96 grupos |
| `impar-marketplace-grupos-tarde` | 17:00 diário | LaunchAgent (plist) | Crosspost turno tarde nos 96 grupos |
| `impar-marketplace-grupos-noite` | 21:30 diário | LaunchAgent (plist) | Crosspost turno noite nos 96 grupos |
| `impar-marketplace-daily-publish` | a cada 30 min | LaunchAgent (StartInterval) | Publisher contínuo da fila diária |
| `impar-reativador-marketplace` | a cada 2h (8h-20h) | MCP scheduled-tasks | Verifica anúncios pausados/rejeitados e republica |

---

## LaunchAgents (~/Library/LaunchAgents/)

```
com.impar.marketplace-crosspost-manha.plist   → 11:30
com.impar.marketplace-crosspost-tarde.plist   → 17:00
com.impar.marketplace-crosspost-noite.plist   → 21:30
com.impar.marketplace-daily-publish.plist     → a cada 30 min
com.impar.marketplace-gerar-fila.plist        → geração semanal da fila
```

---

## Estado e logs

| Item | Localização |
|------|-------------|
| Fila ativa | `~/.local/impar-automation/marketplace/queue.json` |
| Log reativador | `07_LOGS/marketplace-reativador.log` |
| Log crosspost | `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/logs/` |
| Checkpoint publicações | `~/.local/impar-automation/marketplace/` |

---

## Fluxo de execução

```
Fila gerada (semanal)
    ↓
Publisher (a cada 30 min) → publica imóvel da fila no Marketplace
    ↓
Crosspost (11:30 / 17:00 / 21:30) → expande imóvel mais recente nos 96 grupos
    ↓
Reativador (a cada 2h) → identifica pausados/rejeitados e republica
```

---

## Como diagnosticar sem abrir código

1. **Publicações pararam?** Checar `07_LOGS/marketplace-reativador.log` — última linha.
2. **Grupos falhando?** Checar `18_AUTOMATION_STACK/.../logs/` — buscar "ERRO" ou "blocked".
3. **Fila vazia?** Checar `~/.local/impar-automation/marketplace/queue.json` — campo `items`.
4. **Playwright quebrado?** Reinstalar: ver seção "Playwright" em MECANICO-IMPAR-PROCEDIMENTOS.md.
5. **Login Facebook expirado?** Executar login manual: ver "Login" em MECANICO-IMPAR-PROCEDIMENTOS.md.

---

## Problemas conhecidos

- Login do Facebook expira periodicamente → executar `login-facebook.log` manualmente.
- Playwright pode quebrar após update do macOS → reinstalar via brew.
- Checkpoint pode ficar desatualizado (bug benigno) → verificar log CSV para confirmar publicações.
- Facebook pode bloquear temporariamente → aguardar 1-2h e reativar.
- 96 grupos: não editar `grupos-aprovados.csv` sem validar que o grupo ainda existe.
