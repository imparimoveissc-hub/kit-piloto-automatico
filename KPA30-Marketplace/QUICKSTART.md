# Quick Start — Marketplace KPA30 (Jurídico Imobiliário)

Instalação do plugin **`imobiliario-juridico`** seguindo o mesmo fluxo do `claude-for-legal`,
adaptado ao KPA30. Dois caminhos: Claude Code (terminal) ou Claude Desktop (Cowork).

> Todo output é **rascunho para revisão humana**, não aconselhamento jurídico.

## Claude Code (terminal)

1. **Adicione o marketplace** (aponte para a pasta que contém `.claude-plugin/marketplace.json`):

   ```
   /plugin marketplace add "/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/KPA30-Marketplace"
   ```

   Dica: dá pra arrastar a pasta `KPA30-Marketplace` para o terminal para preencher o caminho.

2. **Instale o plugin** (formato `plugin@marketplace`):

   ```
   /plugin install imobiliario-juridico@kpa30-marketplace
   ```

3. **Reinicie o Claude Code** — obrigatório antes de o plugin ficar ativo.

4. **Escolha o escopo `user` (não `project`)** quando perguntado. Isso deixa o plugin acessar
   arquivos pelo sistema (Downloads, Documentos, iCloud) sem permissões extras — útil para ler
   minutas e vistorias.

5. **Rode a entrevista de setup** (leva ~10-15 min; escreve a config da imobiliária):

   ```
   /imobiliario-juridico:cold-start-interview
   ```

6. **Conecte os conectores** quando solicitado (Google Drive, WhatsApp, Asaas). Depois valide com:

   ```
   /imobiliario-juridico:cold-start-interview --check-integrations
   ```

## Claude Desktop (Cowork)

1. Configurações → Plugins → **Adicionar marketplace** → aponte para a pasta `KPA30-Marketplace`.
2. Instale **Jurídico Imobiliário** na lista.
3. Reinicie o Desktop.
4. Rode `/imobiliario-juridico:cold-start-interview` no chat.

## Depois do setup

| Comando | Para quê |
|---|---|
| `/imobiliario-juridico:revisar-contrato-locacao <arquivo>` | Revisa uma minuta contra o playbook + Lei 8.245/91 |
| `/imobiliario-juridico:gerar-contrato-locacao` | Preenche contrato + termo de vistoria |
| `/imobiliario-juridico:acompanhar-reajuste` | Reajustes anuais e fins de vigência chegando |
| `/imobiliario-juridico:customize <ajuste>` | Ajusta o perfil sem re-entrevistar |

## Onde ficam os arquivos de config

- Perfil da prática: `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`
- Perfil compartilhado da empresa: `~/.claude/plugins/config/kpa30/perfil-empresa.md`
- Registro de reajustes: `~/.claude/plugins/config/kpa30/imobiliario-juridico/registro-reajustes.yaml`

Esses caminhos são independentes de versão — sobrevivem às atualizações do plugin.

## Observações

- Sem a cold-start-interview, as skills param e pedem o setup — os outputs seriam genéricos.
- Citações se baseiam na Lei 8.245/91 e no playbook; conecte pesquisa/fontes atualizadas quando precisar.
- Validação do pacote: `python3 KPA30-Marketplace/validar.py`.
