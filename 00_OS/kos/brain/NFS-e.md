---
module: NFS-e
lastModified: 2026-07-26
status: ativo
---

## Objetivo

Emitir notas fiscais de serviço (NFS-e) para a Impar Imóveis automaticamente nos dias de pagamento,
buscando cobranças confirmadas no Asaas e emitindo no Portal Nacional do Simples Nacional.

---

## Portais e endpoints

| Sistema | URL / Endpoint |
|---------|---------------|
| Portal Nacional NFS-e | https://www.nfse.gov.br/EmissorNacional |
| Asaas API | Credenciais em `.env` — campo `ASAAS_API_KEY` |

**Atenção:** Portal Nacional é obrigatório desde 20/07/2026. Portais municipais anteriores não são mais aceitos.

---

## Arquivos principais

| Arquivo | Propósito |
|---------|-----------|
| `18_AUTOMATION_STACK/nfem-joinville/.env` | Credenciais: Asaas API Key, login Portal Nacional |
| `18_AUTOMATION_STACK/nfem-joinville/src/` | Código da automação de emissão |
| `18_AUTOMATION_STACK/nfem-joinville/config/` | Configurações de CNPJ, natureza, itens |
| `18_AUTOMATION_STACK/nfem-joinville/data/` | Dados de emissões anteriores |
| `18_AUTOMATION_STACK/nfem-joinville/logs/` | Logs locais da automação |

---

## Tarefas agendadas

| Task ID | Schedule | Mecanismo | O que faz |
|---------|---------|-----------|-----------|
| `emissao-notas-fiscais` | Dias 20, 25, 29, 30 às 8h | MCP scheduled-tasks (disabled) | Pipeline completo via SKILL.md |
| `emitir-notas-fiscais-asaas` | Dias 20, 25, 29, 30 às 6h | CronCreate durable (scheduled_tasks.json) | Versão alternativa |

**Skills manuais:**
- `emitir-notas-fiscais` — emissão em lote (todos os pagamentos do dia)
- `emitir-nota-avulsa` — uma nota por vez com dados informados interativamente

---

## Parâmetros de emissão

| Campo | Valor |
|-------|-------|
| Natureza da operação | 107 (sempre) |
| Item — venda/serviço | 1005 |
| Item — aluguel | 1712 |
| Prestador | CNPJ da Impar Imóveis |
| Tomador | CNPJ/CPF do cliente (extraído do Asaas) |

---

## Fluxo de emissão automática

```
Dia 20/25/29/30 às 6h-8h → task dispara
    ↓
Busca pagamentos confirmados no Asaas (últimas 24h)
    ↓
Para cada pagamento: extrai CNPJ/CPF, valor, tipo (aluguel ou venda)
    ↓
Acessa Portal Nacional (https://www.nfse.gov.br/EmissorNacional)
    ↓
Preenche formulário: natureza 107, item 1005 ou 1712, tomador, valor
    ↓
Emite nota → baixa PDF
    ↓
Envia PDF via WhatsApp ao Jonata (554796876631)
    ↓
Registra em 07_LOGS/nfem-emissoes.log
```

---

## Emissão manual (avulsa)

Skill: `emitir-nota-avulsa`
Disparo: "emitir nota avulsa", "emitir uma nota", "nota de aluguel avulsa"
Fluxo interativo: CNPJ/CPF → tipo (venda/aluguel) → descrição → valor → emite → envia PDF no WhatsApp.

---

## Como diagnosticar sem abrir código

1. **Notas não emitidas?** Checar `.env` — credenciais válidas?
2. **Asaas sem retorno?** Testar API key em `.env` com `curl`.
3. **Portal Nacional com erro?** Pode ser manutenção — verificar status do portal.
4. **Log de emissões:** `07_LOGS/nfem-emissoes.log` — buscar "ERRO" ou "OK".

---

## Problemas conhecidos

- Portal Nacional pode apresentar captcha ou timeout em horários de pico.
- Sessão do portal expira — a automação usa Chrome headless com login fresh.
- CPF de pessoa física precisa estar no formato correto (sem pontuação) no Asaas.
