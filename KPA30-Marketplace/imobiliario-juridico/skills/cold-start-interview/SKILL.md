---
name: cold-start-interview
description: >
  Roda a entrevista de partida para aprender a prática de locação da imobiliária e
  escrever o perfil da prática. Use no primeiro uso do plugin, quando
  `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md` estiver ausente ou ainda
  contiver marcadores [PREENCHER], ou quando o usuário disser "configurar plugin",
  "configurar locação", "fazer o onboarding", "vamos começar". É a única skill que deve
  rodar numa instalação nova.
argument-hint: "[--redo para re-rodar num plugin já configurado] [--check-integrations para só reprovar integrações] [--lado locador|locatario para re-rodar só o playbook de um lado]"
---

# /cold-start-interview

Roda a entrevista de partida. A primeira execução escreve
`~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`; execuções com `--redo`
reentrevistam e mostram um diff antes de sobrescrever.

## Instruções

1. **Cheque o estado atual:** Leia `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`.
   Se contiver `[PREENCHER]` ou `[Nome da Imobiliária]`, prossiga com entrevista nova. Se estiver
   preenchido e `--redo` não foi passado, pergunte: "Parece que você já está configurado. Quer
   re-rodar a entrevista? Isso sobrescreve o CLAUDE.md da config (mostro um diff antes)."

2. **Cheque o perfil compartilhado da empresa** em `~/.claude/plugins/config/kpa30/perfil-empresa.md`.
   Se não existir, colete os fatos gerais (nome, CRECI, comarca-base, postura de risco, pessoas-chave)
   e crie-o antes do perfil da prática. Ele é compartilhado por todos os plugins do KPA30.

3. **Siga o roteiro de entrevista abaixo.**

4. **Peça documentos-semente:** 5-10 contratos de locação recentes já assinados (mais é melhor;
   20 dão um padrão mais claro) e, se existir, a tabela de garantias/encargos padrão da casa.
   Aceite caminhos de arquivo, links do Google Drive ou textos colados.

5. **Leia os documentos-semente** e extraia as posições reais do playbook: índice de reajuste usado,
   modalidade de garantia, prazo, quem paga cada encargo, cláusulas recorrentes. Anote deltas entre
   a posição declarada e o que de fato foi assinado.

6. **Migração:** Se existir um CLAUDE.md preenchido (sem `[PREENCHER]`) em
   `~/.claude/plugins/cache/kpa30/imobiliario-juridico/*/CLAUDE.md` mas não no caminho de config,
   copie-o para o caminho de config e mostre o que foi migrado.

7. **Escreva `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`** (criando os diretórios
   pais) seguindo a estrutura do template. Use as palavras do próprio corretor onde possível.

8. **Mostre resumo + próximos passos:**
   - "Foi isso que eu entendi — o CLAUDE.md está escrito. O que ficou errado?"
   - Ofereça uma revisão de teste: "Quer jogar um contrato pra eu revisar?"
   - Se o Asaas estiver conectado: ofereça carregar o registro de reajustes em lote.

## Roteiro de entrevista

1. **Cenário:** imobiliária, administradora, corretor autônomo ou proprietário direto?
2. **Lado padrão:** você representa o **locador** (proprietário), o **locatário**, ou **ambos**?
3. **Garantia:** modalidade preferida (fiança, caução, seguro-fiança, capitalização)?
4. **Reajuste:** índice padrão (IGP-M, IPCA, INCC) e periodicidade?
5. **Prazo e multa:** prazo padrão e como calcula multa por rescisão antecipada?
6. **Encargos:** quem paga IPTU, condomínio, seguro incêndio, taxa de lixo?
7. **Escalonamento:** que situações precisam de aprovação e de quem?
8. **Estilo da casa:** destino dos alertas (WhatsApp/e-mail), tom do memorando, nomenclatura.

## `--check-integrations`

Re-roda a checagem de disponibilidade das integrações (Google Drive, WhatsApp, Asaas) e atualiza
`## Integrações disponíveis` no CLAUDE.md da config. Não reentrevista. Ao provar, só reporte ✓ se uma
chamada de MCP de fato teve sucesso. Conectores configurados-mas-não-testados ficam ⚪ com uma linha de
como confirmar. Nunca reporte ✓ com base apenas nas declarações do `.mcp.json`.

## `--lado locador` / `--lado locatario`

Re-roda só a seção de playbook da entrevista, calibrada para o lado indicado, e grava na subseção
correspondente. NÃO re-pergunta cenário, integrações, dados da equipe ou matriz de escalonamento —
esses são agnósticos ao lado. Atualiza o marcador `**Lado padrão:**` para refletir os lados preenchidos.

## Exemplos

```
/imobiliario-juridico:cold-start-interview
```

```
/imobiliario-juridico:cold-start-interview --redo
```

```
/imobiliario-juridico:cold-start-interview --check-integrations
```
