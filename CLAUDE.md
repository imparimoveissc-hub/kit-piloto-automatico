# Kit Piloto Automático V30

Sempre opere em pt-BR. Siga `00_OS/kos/token-policy.md` em TODA task — sem exceção.

## Gatilhos automáticos

| Gatilho (palavras-chave) | Ação imediata |
|--------------------------|---------------|
| "emitir notas", "notas pendentes", "NFS-e", "rodar emissão" / dias 20,25,29,30 | skill `emitir-notas-fiscais` — lote Asaas → Portal Nacional |
| "emitir nota de venda", "nota avulsa", "emitir uma nota", "nota de aluguel avulsa" | skill `emitir-nota-avulsa` — 1 nota manual, dados na hora |
| "incluir imóveis", "cadastrar imóveis novos", "automação incluir imóveis" | `00_OS/commands/cadastrar-imoveis.md` (CRM Impar via Chrome) |
| "instalar kpa30", "instalar kit", "primeira vez", "começar a usar o kit" | `00_OS/commands/instalar-kpa30.md` — wizard 7 etapas |
| "atualizar apartamentos na planta", "atualizar imóveis na planta", "tabela de apartamentos" / dias 2,3,15,20,25 | `00_OS/commands/atualizar-apartamentos-na-planta.md` — compara Rogga/JM/Maria Laura → CRM |

Credenciais NFS-e: `18_AUTOMATION_STACK/nfem-joinville/.env`. Portal: https://www.nfse.gov.br/EmissorNacional

## ⛔ Regra Messenger Marketplace (ordem 2026-08-09)

`varredura_inbox.py` deve processar e enviar mensagens SOMENTE para conversas do Facebook Marketplace.
Checar `is_marketplace` (presença de `a[href*="/marketplace/item/"]` ou URL com `/marketplace/`) **antes de qualquer envio**, em ambos os modos: normal (`marketplace/inbox/`) e fallback (`messages/`).
Se `is_marketplace == False` → pular com `stats['p'] += 1`, nunca enviar.

## ⛔ Regra WhatsApp — único caminho (ordem 2026-08-10)

**O ÚNICO caminho autorizado para WhatsApp é o app nativo do macOS.**
Método: `whatsapp://send?phone=` + AppleScript (ou CGEvent lclick para grupos).

NUNCA executar, instalar, agendar ou sugerir qualquer outro caminho:
- Bridge/MCP WhatsApp (`start-bridge.sh`, `install-launchd-macos.sh`, binário Go)
- WhatsApp Web / Puppeteer / Playwright apontando para web.whatsapp.com
- Qualquer API não-oficial (WPPConnect, Baileys, etc.)
- Qualquer script que abra ou reconecte sessão WhatsApp programaticamente
- whatsapp-mcp ou qualquer MCP que não seja o app nativo

Se o app nativo estiver fechado ou com problema → reportar ao Jonata. Não tentar reconectar automaticamente.

## Inicialização

Ao receber qualquer pedido: `00_INDEX.md` → `00_OS/cos.md`.
- Se autonomia envolvida → `00_OS/proactivity-policy.md`
- Se cliente/ferramenta/automação/WhatsApp/instalação → `00_OS/access-preflight.md`

## KOS — leitura obrigatória (nesta ordem, pare quando responder)

```
0. current-state.md  →  brain/<módulo>.current-state.md  (~200 bytes)
1. Brain             →  00_OS/kos/brain/_INDEX.md → <módulo>.md
2. KOS Index         →  00_OS/kos/index.json
3. Registry          →  00_OS/kos/registry.yaml
4. Index             →  00_INDEX.md
5. Memory            →  ~/.claude/projects/.../memory/MEMORY.md
6. Graphify          →  graphify query "<conceito>"
7. Código            →  último recurso
```

Nunca vá direto ao código. Nunca use `ls -R` ou `find .` sem alvo. Máximo 1 arquivo por vez sem dependência explícita.

## Protocolo pós-task (KOS Fase 3)

Após criar ou alterar skill, rotina, automação, script ou scheduled task:

```bash
bash 00_OS/kos/post-task-hook.sh <modulo> "descrição da mudança"
```

Módulos: `marketplace` | `leads` | `sistema` | `nfse` | `contratos` | `followup` | `geral`

Mudança estrutural (novo arquivo/task/LaunchAgent) → atualizar `registry.yaml` também.
Nova skill do zero → `bash kos-register-skill.sh`.
Decisão irreversível → registre em `07_LOGS/decisions.md`.

## Graphify

`graphify-out/graph.json` existe. Antes de grep/find/Read em source: `graphify query "<questão>"`. Após mudança estrutural: `graphify . && graphify cluster-only . && cp -R graphify-out/* Knowledge/Code/graphify/`.

## Diretórios

| Tipo | Pasta |
|------|-------|
| Saídas finais | `06_OUTPUTS/` |
| Estado vivo | `05_WORKSPACE/` |
| Logs operacionais | `07_LOGS/` |
| Templates | `10_TEMPLATES_OPERACIONAIS/` |
| Automações | `18_AUTOMATION_STACK/` + `05_WORKSPACE/clientes/<c>/automacoes/` |
| WhatsApp/Cowork | `12_WHATSAPP_STACK/` + `05_WORKSPACE/clientes/<c>/whatsapp/` |
| MCPs/conectores | `20_MCP_SETUP/` |
| Builder (novo agente/skill) | `21_BUILDER_KIT/` |

Não alterar pastas externas referenciadas (kits anteriores, `GOAT-copy`).

## Full-auto

- Decisão reversível → caminho conservador; registre premissa em `07_LOGS/decisions.md`.
- Dado faltante mas task pode avançar → use `[A PREENCHER]`.
- Pergunte só se: risco grande, decisão irreversível, credencial ausente ou ambiguidade que mude a rota.
- WhatsApp/automações → `draft` full-auto; ativação real, API write, CRM update, publicação → confirmação.

## Qualidade

Toda entrega relevante passa por gate (`00_OS/gate-matrix.md`). Copy/WhatsApp/automação sem os elementos obrigatórios fica como rascunho, não final.
