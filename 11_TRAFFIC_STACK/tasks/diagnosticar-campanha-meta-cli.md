# Task: Diagnosticar Campanhas Meta via CLI Nativo

> Task usada por `@meta-dr-specialist` e `@traffic-orchestrator` quando o usuário pede análise/diagnóstico de campanhas vivas em Meta Ads. Conecta o CLI `meta` nativo ao framework de análise da Traffic Stack.

## Quando esta task é executada

- `*diagnostico [janela]` em `@traffic-orchestrator`
- `*list` ou `*insights` em `@meta-dr-specialist`
- Qualquer comando da stack que precise de **dados reais de campanha**

## Pré-requisitos (validar antes de executar)

1. **Cliente carregado** — `05_WORKSPACE/clientes/<cliente>/CLAUDE.md` lido
2. **`act_id` resolvido** — via `05_WORKSPACE/clientes/<cliente>/act-mapping.yaml` ou flag explícita
3. **CLI `meta` funcionando** — `meta auth status` retorna `Authenticated`. No Windows, o comando `meta` é resolvido pelo wrapper criado por `/meta-cli-install` em `<HOME>\bin\meta.cmd` que roteia pro WSL. No macOS/Linux, é nativo.
4. **Janela definida** — default `last_7d`, override pelo usuário

Se algum falhar, ABORTAR com mensagem clara. Não inventar dados.

## Pipeline de execução

### Etapa 1 — Listar campanhas ativas

```powershell
meta ads campaign list `
  --ad-account-id act_<ID> `
  --filter "effective_status=ACTIVE" `
  -o json
```

**Parsear:** lista de campanhas com `id`, `name`, `objective`, `daily_budget`, `lifetime_budget`, `start_time`.

**Validação:** se 0 campanhas ativas, reportar e parar.

### Etapa 2 — Insights por campanha (janela definida)

```powershell
meta ads insights get `
  --ad-account-id act_<ID> `
  --date-preset last_<N>d `
  --level campaign `
  --fields spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,actions,action_values,purchase_roas,cost_per_action_type `
  -o json
```

**Parsear:** tabela com KPIs por campanha. Cruzar com lista da Etapa 1 (join por `campaign_id`).

### Etapa 3 — Insights por adset (top campanhas)

Para as 3 campanhas com maior gasto:

```powershell
meta ads insights get `
  --ad-account-id act_<ID> `
  --date-preset last_<N>d `
  --level adset `
  --filtering "[{'field':'campaign.id','operator':'EQUAL','value':'<CAMPAIGN_ID>'}]" `
  -o json
```

### Etapa 4 — Top 10 ads (por ROAS desc, depois CPA asc)

```powershell
meta ads insights get `
  --ad-account-id act_<ID> `
  --date-preset last_<N>d `
  --level ad `
  --fields spend,impressions,clicks,ctr,actions,action_values,purchase_roas,video_thruplay_watched_actions `
  -o json
```

**Filtrar:** ads com `impressions >= 1000` (significância estatística). **Sortear:** ROAS desc, CPA asc.

### Etapa 5 — Cruzar com baseline do cliente

Carregar `05_WORKSPACE/clientes/<cliente>/baseline-kpis.md`. Comparar:

- Spend atual vs target/baseline
- ROAS atual vs alvo do cliente
- CPA atual vs alvo do cliente
- CTR vs benchmark do cliente (não genérico)
- Frequência (alerta se >5)

### Etapa 6 — Aplicar framework "Onde Quebrou?"

Do agente `@funnel-analyst` framework 6. Identificar em qual estágio o gargalo aparece.

### Etapa 7 — Gerar relatório

Estrutura padrão:

```markdown
## Diagnóstico Meta Ads — {Cliente} | {Data} | Janela: last_{N}d

### Resumo executivo (semáforo)
- 🟢 / 🟡 / 🔴 — {1 frase}
- Spend: R$ X (vs baseline R$ Y)
- ROAS: Z x (vs alvo W x)
- CPA: R$ V (vs alvo R$ U)

### Campanhas ativas — Performance

| # | Campanha | Spend | Impr | CTR | CPM | Conv | CPA | ROAS | Status |
|---|----------|-------|------|-----|-----|------|-----|------|--------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... | 🟢 |

### Top 3 vencedores (ads)
1. **{nome ad}** — ROAS X, CPA Y, hook rate Z%, formato W
2. ...

### Top 3 perdedores (kill list — CONFIRMAR ANTES DE PAUSAR)
1. **{nome ad}** — ROAS X, gasto Y, CPA Z (acima alvo) — recomendação: PAUSAR
2. ...

### Análise "Onde Quebrou?"
{Aplicar framework 6 do @funnel-analyst}

### Hipóteses ranqueadas (causa-raiz)
1. {hipótese 1} (probabilidade XX%) — evidência: {dado}
2. {hipótese 2} (XX%) — evidência: {dado}
3. {hipótese 3} (XX%) — evidência: {dado}

### Próximas ações (24h)
- [ ] {ação} — quem: {agente}
- [ ] {ação}

### Próximas ações (7d)
- [ ] {ação}

### Métricas pra acompanhar
- {KPI} — alvo {valor} em {dias}

---
Salvo em: 05_WORKSPACE/clientes/{cliente}/_relatorios/{data}-diagnostico.md
```

### Etapa 8 — Salvar artefatos

- Markdown: `05_WORKSPACE/clientes/<cliente>/_relatorios/<YYYY-MM-DD>-diagnostico.md`
- JSON cru (pra histórico): `05_WORKSPACE/clientes/<cliente>/_relatorios/_raw/<YYYY-MM-DD>-insights.json`

## Tratamento de erros

| Erro CLI | Causa provável | Ação |
|----------|----------------|------|
| `Invalid OAuth access token` | Token expirou no `~/.profile` WSL | Pedir novo token ao usuário; orientar `meta auth login` |
| `(#100) Unsupported get request` | act_id errado ou sem permissão | Validar contra `act-mapping.yaml`; verificar Business Manager |
| `Empty response` | Sem dados na janela (campanha pausada antes) | Reportar; sugerir janela maior |
| WSL não responde | WSL caiu ou config quebrada | `wsl --shutdown` + retry |

**NUNCA** continuar com dados parciais sem reportar lacuna.

## Confirmação antes de ações destrutivas

Se o relatório recomendar **pause** ou **mudança de budget >20%**:

1. NÃO executar automaticamente
2. Listar ações propostas
3. Pedir confirmação explícita: `Confirma pausar [N] ads? (s/n)`
4. Só executar após confirmação

Comando de pause (após confirmação):

```powershell
meta ads ad update <AD_ID> --status PAUSED
```

## Logs

Apêndice em todo relatório:
```
Comandos executados:
- meta ads campaign list --ad-account-id act_X --filter ACTIVE -o json
- meta ads insights get --ad-account-id act_X --date-preset last_7d --level campaign -o json
- ...
Tempo total: X segundos
Registros retornados: N campanhas, M adsets, K ads
```

Permite auditoria e reprodução.
