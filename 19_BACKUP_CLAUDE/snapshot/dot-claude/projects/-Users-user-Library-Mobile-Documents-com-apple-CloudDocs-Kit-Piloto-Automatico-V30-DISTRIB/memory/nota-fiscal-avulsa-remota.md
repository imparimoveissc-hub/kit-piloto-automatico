---
name: nota-fiscal-avulsa-remota
description: Emissão de nota fiscal avulsa (manual) e disparo remoto por WhatsApp — skill emitir-nota-avulsa + listener
metadata: 
  node_type: memory
  type: project
  originSessionId: dfc37476-8885-4147-a829-a6dad04553b0
---

Rotina de emissão de UMA nota fiscal avulsa no NF-em Joinville (fora do lote do Asaas de [[impar-crm-chatwoot]]), criada em 2026-07-06.

- **Skill:** `emitir-nota-avulsa` (em `~/.claude/skills/`, espelhada no Cofre — ver [[cofre-obsidian-kpa30]]). Fluxo: pergunta CNPJ/CPF, tipo (venda→item 1005 / aluguel→item 1712), descrição, valor; natureza sempre 107; emite e manda o PDF no WhatsApp do Jonata.
- **CLI:** `18_AUTOMATION_STACK/nfem-joinville/src/cli.py` → `emitir-manual` (+`--usar-sessao` p/ remoto) e `login-manual`.
- **Uso remoto pelo celular:** listener `src/whatsapp_listener.py` faz polling do banco da ponte whatsapp-mcp e emite ao receber `nota venda|aluguel; CNPJ; descrição; valor`. Guia em `README_EMISSAO_REMOTA.md`. **Draft** — ativar com `login-manual` + `run_listener.sh` no Mac.
- **Captcha:** contornado por sessão "quente" (`data/nfem_session.json`); quando expira, refazer `login-manual` (fallback humano combinado com o usuário).

**Gotchas não óbvios:**
- WhatsApp do Jonata: número é 5547996876631, mas o **JID guardado é `554796876631@s.whatsapp.net`** (sem o 9 extra). Enviar pelo JID.
- O comando remoto emite direto, **sem** o passo "confirma?" do fluxo local.
- Mac desligado = não emite (não foi portado pra VM Oracle).
- Bug latente relacionado: `emitir-mes` (lote) provavelmente só faz prévia por timing de DRY_RUN — o fluxo manual já contorna passando dry_run explícito.
