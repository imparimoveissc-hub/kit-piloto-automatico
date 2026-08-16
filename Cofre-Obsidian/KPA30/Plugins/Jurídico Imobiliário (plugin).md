# 🏠 Jurídico Imobiliário — Plugin

Plugin do KPA30 no padrão **claude-for-legal** (Anthropic), adaptado ao pt-BR e à **Lei 8.245/91** (Lei do Inquilinato). Vive em `KPA30-Marketplace/imobiliario-juridico/` no Kit.

> [!info] O que é
> Um bundle instalável (marketplace + plugin), diferente das skills nativas do Kit. Todo output é **rascunho para revisão humana**, não aconselhamento jurídico.

## Componentes espelhados

**Skills**
- [[Imob — cold-start-interview]] — aprende a prática da imobiliária e escreve o perfil (**rodar primeiro**)
- [[Imob — revisar-contrato-locacao]] — revisa minuta com checklist citando artigo
- [[Imob — gerar-contrato-locacao]] — preenche contrato + vistoria (reaproveita o gerador do Kit)
- [[Imob — acompanhar-reajuste]] — reajuste anual + fim de vigência
- [[Imob — customize]] — ajuste pontual do perfil

**Agente**
- [[Imob — vigia-reajustes (agente)]] — semanal, avisa reajustes/vencimentos no WhatsApp

**Config / docs**
- [[Imob — QUICKSTART]] — como instalar (comandos `/plugin marketplace add` e `/plugin install`)
- [[Imob — CLAUDE (template)]] — template do perfil da prática (dados reais ficam em `~/.claude/plugins/config/kpa30/…`)
- [[Imob — README]]

## Padrão herdado do claude-for-legal
- Template vs config: o `CLAUDE.md` do plugin é template; dados do usuário ficam em caminho versão-independente que sobrevive a updates.
- Gate de setup: skills substantivas param se a config tiver `[PREENCHER]` e mandam rodar a cold-start-interview.
- Conectores em `.mcp.json`: Google Drive, WhatsApp, Asaas.

## Validação
Suíte em `KPA30-Marketplace/validar.py` — estrutural (17 checks), YAML estrito e gate de setup: **100% verde**.

---
Relacionados no Kit: [[gerar-contrato-locacao]] · [[emitir-notas-fiscais]] · [[retirar-notas-fiscais]]
