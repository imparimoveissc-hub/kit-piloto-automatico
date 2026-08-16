# Jurídico Imobiliário (`imobiliario-juridico`)

Plugin do Kit Piloto Automático V30 para a prática de **locação imobiliária**, seguindo o padrão
`claude-for-legal` da Anthropic, adaptado ao pt-BR e à Lei 8.245/91 (Lei do Inquilinato).

> Todo output é **rascunho para revisão humana**, não aconselhamento jurídico.

## O que faz

| Skill | Para quê |
|---|---|
| `/imobiliario-juridico:cold-start-interview` | Aprende a prática da imobiliária e escreve o perfil. **Rode primeiro.** |
| `/imobiliario-juridico:revisar-contrato-locacao` | Revisa uma minuta contra o playbook + Lei 8.245/91, com flags citando artigo. |
| `/imobiliario-juridico:gerar-contrato-locacao` | Preenche contrato + termo de vistoria (reaproveita o gerador do kit). |
| `/imobiliario-juridico:acompanhar-reajuste` | Mostra reajustes anuais e fins de vigência chegando. |
| `/imobiliario-juridico:customize` | Ajusta pontualmente o perfil já configurado. |

**Agente:** `vigia-reajustes` — semanal, posta o que reajusta/vence no destino configurado.

## Como se usa

1. Instale o marketplace `kpa30-marketplace` e o plugin.
2. Rode `/imobiliario-juridico:cold-start-interview` (~10-15 min). Ele escreve a config em
   `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md` (sobrevive a atualizações).
3. Use os slash commands ou deixe as skills dispararem sozinhas.

## Arquitetura

- Sem build: tudo é markdown + JSON/YAML.
- **Template vs config:** o `CLAUDE.md` do plugin é template; os dados da imobiliária ficam no
  diretório de config, um nível abaixo de `perfil-empresa.md` (compartilhado por todos os plugins KPA30).
- Skills param se a config ainda tiver `[PREENCHER]` e direcionam para a cold-start-interview.

## Conectores (`.mcp.json`)

Google Drive (documentos), WhatsApp (alertas), Asaas (cobranças/reajuste). Marque ✓ só o que
`--check-integrations` confirmar.

## Licença

Baseado no padrão `claude-for-legal` (Apache 2.0, © 2026 Anthropic PBC).
