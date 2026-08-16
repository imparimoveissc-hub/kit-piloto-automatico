---
tipo: brain-index
status: ativo
atualizado: 2026-07-26
---

# 🧠 Brain — Automações Impar

Cada note aqui é um **resumo vivo** de uma automação. Quando algo mudar no sistema, o Claude atualiza a note correspondente.

> [!tip] Como usar
> Clique na automação que quer entender ou monitorar. Se quiser pedir algo ao Claude, cada note tem uma seção **"Como acionar"** com as frases exatas.

---

## Automações ativas

| Automação | Status | Note |
|-----------|--------|------|
| Facebook Marketplace + Grupos | ✅ Ativo | [[Marketplace]] |
| Leads Chaves na Mão + CSV | ⚠️ Composio down | [[Leads]] |
| Gerente Digital (saúde horária) | ✅ Ativo | [[Sistema]] |
| Emissão de Notas Fiscais | ✅ Ativo | [[NFS-e]] |
| Contratos de Locação | ✅ Ativo | [[Contratos]] |
| Messenger Bridge | ✅ Ativo (PID 51328) | [[Sistema]] |
| CRM / Rogga | ✅ Ativo (PID 724) | [[Sistema]] |

---

## Alertas em aberto (2026-07-26)

> [!warning] Atenção
> - **Composio MCP down** → Leads Chaves na Mão parados
> - **leads-planilha-watcher exit=256** → CSV watcher com erro (ver log)
> - **Full Disk Access pendente** → 2 LaunchAgents disabled aguardando

---

## Inventário completo

Para ver **todos** os LaunchAgents, Claude tasks e scripts (ativos, pausados e desativados):

→ [[Automacoes-Mapa]] — mapa completo gerado em 2026-07-26

---

## Como o Brain funciona

```
Você pergunta algo ao Claude
       ↓
Claude lê o Brain (esta pasta) antes de abrir qualquer arquivo
       ↓
Na maioria das vezes, o Brain já responde — sem gastar tokens lendo código
       ↓
Só abre código se precisar de algo que o Brain não cobre
```

Isso reduz em ~10× o consumo de tokens nas automações rotineiras.

## Ver também

- [[CLAUDE - Raiz]] — regras gerais do Kit
- [[00 - Índice KPA30]] — índice completo
