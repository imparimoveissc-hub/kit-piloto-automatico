---
name: retirar-notas-fiscais
description: >
  Skill para retirar (buscar, baixar ou listar) notas fiscais automaticamente com cálculo
  inteligente de período. Use esta skill sempre que o usuário mencionar: "retirar notas",
  "baixar NFs", "pegar notas fiscais", "exportar NFe", "notas do período", "notas fiscais
  automáticas", "NFS-e do mês", "XML das notas", "buscar notas", "relatório de notas fiscais",
  "notas fiscais de serviço", "notas do corte", ou qualquer variação. Acione também quando o
  usuário mencionar períodos de faturamento nos dias 20, 25, 29 ou 30 do mês em conjunto com
  notas fiscais, ou quando pedir para automatizar a coleta de NFs.
---

# Skill: Retirar Notas Fiscais

## Objetivo

Automatizar a retirada de notas fiscais calculando automaticamente o período vigente com base
nos dias de corte configurados: **20, 25, 29 e 30** de cada mês.

---

## Passo 1 — Calcular o período vigente

**Sempre execute este script primeiro**, antes de qualquer outra ação:

```bash
python3 ~/.claude/skills/retirar-notas-fiscais/scripts/calcular_periodo.py
```

O script retorna um JSON com:
- `periodo_inicio` — data de início do período vigente
- `periodo_fim` — data de fim do período vigente  
- `proximo_corte` — próxima data de corte
- `dias_ate_proximo_corte` — urgência: quantos dias faltam para o próximo corte
- `descricao` — texto legível para confirmar com o usuário

**Apresente o resultado ao usuário** antes de prosseguir, por exemplo:
> "Período identificado: 30/06/2026 a 19/07/2026. Posso retirar as notas desse período?"

Se o usuário quiser um período diferente, use a data informada como argumento:
```bash
python3 ~/.claude/skills/retirar-notas-fiscais/scripts/calcular_periodo.py 2026-06-25
```

---

## Passo 2 — Identificar o sistema de origem

Pergunte (ou identifique pelo contexto) de onde as notas devem ser retiradas:

| Sistema | Como identificar |
|---|---|
| **SEFAZ / NFe federal** | XML de produtos, CNPJ emitente, menção a "DANFE" ou "chave de acesso" |
| **Prefeitura (NFS-e)** | Nota de serviço, RPS, ISS, menção ao município |
| **ERP (Omie, Bling, Tiny, Conta Azul)** | Menção direta ao sistema |
| **E-mail / pasta local** | Usuário menciona que as notas chegam por e-mail ou estão em pasta |

Se não for possível identificar, pergunte: "As notas estão em qual sistema ou portal?"

---

## Passo 3 — Retirar as notas

### Via portal/browser (SEFAZ, Prefeitura, ERP web)

Use as ferramentas de browser disponíveis (`mcp__Claude_in_Chrome__*`) para:
1. Navegar até o portal
2. Fazer login (use credenciais do `.env` ou peça ao usuário)
3. Filtrar pelo período calculado no Passo 1
4. Baixar os XMLs, PDFs ou relatório

### Via API do ERP (se disponível)

Se houver MCP ou conector configurado para o ERP, use-o diretamente com o período:
```
data_inicio: {periodo_inicio}
data_fim: {periodo_fim}
```

### Via pasta/e-mail local

Se as notas chegam por e-mail ou estão em pasta local:
1. Localize a pasta ou use o MCP de WhatsApp/e-mail configurado
2. Filtre arquivos com data de emissão dentro do período
3. Liste os arquivos encontrados para o usuário

---

## Passo 4 — Resumo e entrega

Ao finalizar, apresente um resumo:

```
Notas fiscais retiradas — Período: {periodo_inicio} a {periodo_fim}

• Total de notas: X
• Valor total: R$ X.XXX,XX (se disponível)
• Arquivos salvos em: [caminho ou sistema]
• Próximo corte: {proximo_corte} ({dias_ate_proximo_corte} dias)
```

Salve qualquer relatório gerado em `06_OUTPUTS/notas-fiscais/` (se o projeto V30 estiver ativo).

---

## Configuração dos dias de corte

Os dias de corte estão definidos no script `scripts/calcular_periodo.py`:

```python
DIAS_CORTE = [20, 25, 29, 30]
```

Para alterar, edite diretamente essa linha. O script ajusta automaticamente meses que não
têm dia 29 ou 30 (como fevereiro).

---

## Regras de operação

- **Nunca emita ou cancele** notas sem confirmação explícita do usuário — apenas leia/baixe.
- **Confirme o período** com o usuário antes de baixar em volume.
- **Credenciais ausentes**: se login for necessário e não houver credenciais, peça ao usuário
  antes de prosseguir.
- **Erros de acesso**: documente em `07_LOGS/decisions.md` se houver falha de autenticação
  ou sistema indisponível.
