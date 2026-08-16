# KOS — Kernel Optimization System
## Roadmap de Implementação V30

**Objetivo:** reduzir consumo de tokens em 10× via arquitetura em camadas que prioriza conhecimento pré-compilado (Brain, Registry, Index) sobre leitura de código.

**Princípio central:** o custo de uma sessão Claude é dominado por quanto código ela lê, não pelo tamanho do prompt. Cada camada do KOS ataca isso de um ângulo diferente.

---

## Status por fase

| Fase | Status | Economia estimada |
|------|--------|-------------------|
| Fase 1 — Token Policy + Brain | ✅ 100% COMPLETA (2026-07-26) | ~3,25M tok/dia (fixes) + qualitativo |
| Fase 2 — Registry + Índice | ✅ 100% COMPLETA (2026-07-26) | ~2-3× adicional em tasks de manutenção |
| Fase 3 — Summaries + Self-learning | ✅ 100% COMPLETA (2026-07-26) | ganhos compostos ao longo do tempo |

---

## ✅ FASE 1 — Token Policy + Brain (COMPLETA)

### O que foi entregue

**Fixes imediatos (redução de execuções):**
- `impar-notificar-leads-planilha` (288 Claude runs/dia) → substituída por `leads_watcher.py` (Python, zero tokens sem lead novo)
- `impar-manutencao-horaria` (24 runs/dia) → fundida em `impar-gerente-digital`
- `impar-reativador-marketplace` → de 26 runs/dia para 7 runs/dia (a cada 2h)
- `status-tudo-certo-whatsapp` → já era órfã, confirmada desativada

**Arquivos criados:**
```
00_OS/kos/token-policy.md              — protocolo de leitura imposto em toda sessão
00_OS/kos/brain/_INDEX.md              — entrada única do Brain
00_OS/kos/brain/Marketplace.md         — Marketplace + grupos Facebook
00_OS/kos/brain/Leads.md               — Chaves na Mão + CSV watcher
00_OS/kos/brain/Sistema.md             — Gerente Digital + saúde horária
00_OS/kos/brain/NFS-e.md               — Emissão de notas fiscais
00_OS/kos/brain/Contratos.md           — Locação, reajustes, plugin imobiliario
18_AUTOMATION_STACK/impar-leads-planilha-watcher/leads_watcher.py
18_AUTOMATION_STACK/impar-leads-planilha-watcher/*.plist.template
kos-install.sh                         — instalador portável (um comando, qualquer Mac)
```

**CLAUDE.md atualizado:**
- Inicialização: passo 8 → `00_OS/kos/token-policy.md`
- Knowledge Layer: Brain como primeira camada de consulta

### Pendente da Fase 1

- [x] **Brain no Obsidian** — `Cofre-Obsidian/KPA30/Brain/` criado em 2026-07-26
  - 6 notas: `00 - Índice Brain.md` + Marketplace, Leads, Sistema, NFS-e, Contratos
  - Formato humano (callouts, wikilinks, seção "Como acionar")
  - `00 - Índice KPA30.md` atualizado com seção Brain

### Regra de sincronização Brain (kit ↔ Obsidian)

Existem dois tipos de Brain note:
- **Kit** (`00_OS/kos/brain/`): para Claude — denso, técnico, com caminhos de arquivo, diagnóstico
- **Obsidian** (`Cofre-Obsidian/KPA30/Brain/`): para Jonata — visual, callouts, seção "Como acionar"

Quando atualizar após uma mudança:
1. Atualize a note do **kit** primeiro (Claude lê dali)
2. Atualize a note do **Obsidian** em seguida (Jonata navega dali)
3. As duas evoluem juntas mas não são cópias — são perspectivas diferentes do mesmo módulo
4. Se mudar só uma, marque `status: desatualizado` na outra para não gerar confiança falsa

---

## ⬜ FASE 2 — Registry Enriquecido + Índice Invertido

**Objetivo:** fazer o Claude responder 80% das perguntas operacionais sem abrir código.

### Camada 3 — Registry enriquecido

**O que é:** um arquivo YAML que descreve cada módulo/automação com metadados suficientes para diagnóstico sem leitura de código.

**Arquivo a criar:** `00_OS/kos/registry.yaml`

**Formato de cada entrada:**
```yaml
modules:
  marketplace:
    name: Marketplace
    description: Publicação de imóveis no Facebook Marketplace + 96 grupos
    status: ativo          # ativo | pausado | desenvolvimento | desativado
    criticidade: alta      # alta | media | baixa
    brain: 00_OS/kos/brain/Marketplace.md
    arquivos_principais:
      - 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/publish_groups_playwright.py
      - 18_AUTOMATION_STACK/impar-facebook-marketplace-posting/MECANICO-IMPAR-PROCEDIMENTOS.md
    estado:
      - ~/.local/impar-automation/marketplace/queue.json
    logs:
      - 07_LOGS/marketplace-reativador.log
    launchagents:
      - com.impar.marketplace-crosspost-manha
      - com.impar.marketplace-crosspost-tarde
      - com.impar.marketplace-crosspost-noite
      - com.impar.marketplace-daily-publish
    tasks_agendadas:
      - id: impar-reativador-marketplace
        mecanismo: MCP
        frequencia: "a cada 2h (8h-20h)"
    dependencias:
      - playwright
      - facebook_login
    entradas:
      - "queue.json (fila gerada semanalmente)"
    saidas:
      - "posts no Marketplace"
      - "posts nos 96 grupos"
    ultima_alteracao: 2026-07-26
    problemas_conhecidos:
      - "Login Facebook expira periodicamente"
      - "Playwright pode quebrar após update macOS"

  leads:
    name: Leads Chaves na Mão + CSV
    # ... mesmo formato
```

**Módulos a registrar:** marketplace, leads, sistema, nfse, contratos, followup

**Uso pelo Claude:**
```
Antes de abrir qualquer arquivo de automação:
  1. Leia registry.yaml — encontre o módulo
  2. Veja o campo `brain` — leia o Brain module
  3. Só então abra código se necessário
```

---

### Camada 4 — Índice invertido

**O que é:** um `index.json` gerado automaticamente que mapeia funções, conceitos e entidades para os arquivos onde vivem, sem o Claude ter que fazer grep.

**Script a criar:** `00_OS/kos/build-index.py`

**O que o script faz:**
1. Percorre os arquivos Python em `18_AUTOMATION_STACK/` e `~/.local/impar-automation/`
2. Extrai definições de função via AST (`ast.parse`)
3. Percorre arquivos Markdown chave e extrai headings e conceitos
4. Percorre `~/.claude/scheduled-tasks/*/SKILL.md` e extrai task IDs + descrições
5. Gera `00_OS/kos/index.json`

**Formato do index.json:**
```json
{
  "generated_at": "2026-07-26T16:00:00",
  "functions": {
    "main": [
      {"file": "~/.local/impar-automation/leads-planilha/leads_watcher.py", "line": 85, "module": "leads"}
    ],
    "send_whatsapp": [
      {"file": "~/.local/impar-automation/leads-planilha/leads_watcher.py", "line": 71, "module": "leads"}
    ]
  },
  "concepts": {
    "checkpoint.json": [
      {"path": "~/.local/impar-automation/chaves-na-mao/checkpoint.json", "context": "deduplicação 24h leads", "module": "leads"},
      {"path": "~/.local/impar-automation/marketplace/", "context": "estado publisher marketplace", "module": "marketplace"}
    ],
    "queue.json": [
      {"path": "~/.local/impar-automation/marketplace/queue.json", "context": "fila de publicações", "module": "marketplace"}
    ]
  },
  "tasks": {
    "impar-gerente-digital": {
      "cron": "13 * * * *",
      "skill": "~/.claude/scheduled-tasks/impar-gerente-digital/SKILL.md",
      "module": "sistema",
      "enabled": true
    },
    "impar-reativador-marketplace": {
      "cron": "0 8-20/2 * * *",
      "skill": "~/.claude/scheduled-tasks/impar-reativador-marketplace/SKILL.md",
      "module": "marketplace",
      "enabled": true
    }
  },
  "launchagents": {
    "com.impar.marketplace-crosspost-manha": {
      "plist": "~/Library/LaunchAgents/com.impar.marketplace-crosspost-manha.plist",
      "schedule": "11:30 diário",
      "module": "marketplace"
    }
  }
}
```

**Uso pelo Claude:**
```
Antes de fazer grep ou find para localizar uma função:
  1. Leia 00_OS/kos/index.json
  2. Busque o conceito/função
  3. Abra diretamente o arquivo + linha indicados
```

**Como manter atualizado:**
- Rodar `python3 00_OS/kos/build-index.py` após qualquer alteração estrutural
- Adicionar ao `kos-install.sh` como passo 5

---

### Checklist de entrega da Fase 2

- [x] Criar `00_OS/kos/registry.yaml` com 6 módulos completos (2026-07-26)
- [x] Criar `00_OS/kos/build-index.py` (AST parser + markdown parser + task scanner) (2026-07-26)
- [x] Rodar `build-index.py` e gerar `00_OS/kos/index.json` inicial — 85 funções, 82 conceitos, 18 tasks, 6 LaunchAgents
- [x] Atualizar `kos-install.sh` — passo [4/5] Obsidian + passo [5/5] build-index.py
- [x] Atualizar `CLAUDE.md` — Knowledge Layer: index.json (passo 2) + registry.yaml (passo 3)
- [x] Atualizar `00_OS/kos/token-policy.md` — hierarquia atualizada + comandos jq
- [x] Criar `00_OS/kos/OBSIDIAN-NOVA-MAQUINA.md` — guia 4 etapas para nova máquina

---

## ⬜ FASE 3 — Resumos Pós-Task + Autoaprendizado (ongoing)

**Objetivo:** fazer o Brain, Registry e Index se atualizarem automaticamente após cada task relevante, tornando o sistema progressivamente mais inteligente.

### Camada 5 — Resumos permanentes pós-task

**Conceito:** após qualquer alteração em automação, scripts ou configuração, Claude gera um resumo e atualiza o Brain module correspondente.

**Protocolo a adicionar ao CLAUDE.md (Fase 3):**
```
## Protocolo pós-task (KOS)

Ao concluir qualquer task que altere uma automação, script, configuração ou scheduled task:

1. Identifique o módulo Brain afetado em 00_OS/kos/brain/_INDEX.md
2. Atualize o Brain module:
   - Campo `lastModified`
   - Seção afetada (Arquivos, Tarefas, Problemas conhecidos, etc.)
   - Máx 3 linhas de alteração por atualização
3. Se a alteração for estrutural (novos arquivos, novas tasks, nova dependência):
   - Atualize também registry.yaml
   - Rode build-index.py ou marque como `index_desatualizado: true` no registry
4. Registre em 07_LOGS/decisions.md se for decisão irreversível
```

**Trigger:** parte do handoff curto que todo especialista já entrega.
Não requer automação nova — é disciplina operacional integrada ao fluxo existente.

---

### Camada 9 — Autoaprendizado

**Conceito:** após cada task concluída, o sistema atualiza automaticamente o Brain, Registry e Index. Reduz dependência de disciplina manual.

**Implementação proposta:**

**Hook pós-task** (`00_OS/kos/post-task-hook.sh`):
```bash
#!/bin/bash
# Executado pelo Claude ao final de tasks que afetam automações
# Argumento: módulo afetado (marketplace | leads | sistema | nfse | contratos)
MODULE="$1"
KIT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# 1. Regenera o índice invertido
python3 "$KIT_DIR/00_OS/kos/build-index.py"

# 2. Atualiza lastModified no Brain module
BRAIN="$KIT_DIR/00_OS/kos/brain/${MODULE^}.md"
if [ -f "$BRAIN" ]; then
    sed -i '' "s/lastModified: .*/lastModified: $(date +%Y-%m-%d)/" "$BRAIN"
fi

# 3. Log da atualização
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] KOS update: módulo=$MODULE" >> "$KIT_DIR/07_LOGS/kos-updates.log"
```

**Quando o hook é chamado:**
- Pelo próprio Claude ao final de tasks de automação (disciplina do Protocolo pós-task)
- Pelo `kos-install.sh` após instalação
- Manualmente quando necessário

**Risco a gerenciar:** Brain desatualizado é pior que Brain ausente.
Se o autoaprendizado falhar silenciosamente, os módulos ficam com dados errados.
Mitigação: campo `status: desatualizado` + verificação periódica pelo `impar-gerente-digital`.

---

## Arquitetura final (referência)

```
KOS (Kernel Optimization System)
│
├── Camada 1 — Token Policy          00_OS/kos/token-policy.md          ✅ ATIVA
├── Camada 3 — Registry              00_OS/kos/registry.yaml             ⬜ FASE 2
├── Camada 4 — Índice invertido      00_OS/kos/index.json (gerado)       ⬜ FASE 2
│                                    00_OS/kos/build-index.py
├── Camada 5 — Summaries pós-task    Protocolo no CLAUDE.md              ⬜ FASE 3
├── Camada 6 — Prioridade de leitura 00_OS/kos/token-policy.md          ✅ ATIVA
├── Camada 7 — One-File Protocol     00_OS/kos/token-policy.md          ✅ ATIVA
├── Camada 8 — Brain (L2 Cache)      00_OS/kos/brain/*.md               ✅ ATIVA
│                                    Cofre-Obsidian/KPA30/Brain/         ⬜ pendente sync
└── Camada 9 — Autoaprendizado       00_OS/kos/post-task-hook.sh         ⬜ FASE 3

Instalação em nova máquina: bash kos-install.sh
```

---

## Como iniciar a Fase 2

Em uma nova sessão, diga:

> "Vamos continuar o KOS — implementar a Fase 2: registry.yaml e build-index.py"

O Claude lê este roadmap e retoma exatamente daqui.

**Sequência recomendada:**
1. Criar `00_OS/kos/registry.yaml` (começar pelos 3 módulos mais ativos: marketplace, leads, sistema)
2. Criar `00_OS/kos/build-index.py` e gerar index.json
3. Testar: fazer uma pergunta operacional e verificar se o index responde sem abrir código
4. Atualizar CLAUDE.md + token-policy.md para referenciar registry e index
5. Atualizar kos-install.sh para incluir build-index como passo 5
