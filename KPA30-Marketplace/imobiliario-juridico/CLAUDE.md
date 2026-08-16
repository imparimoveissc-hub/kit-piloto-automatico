<!--
LOCAL DA CONFIGURAÇÃO

A configuração específica da imobiliária vive num caminho independente de versão, que
sobrevive às atualizações do plugin:

  ~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md

Regras para toda skill, comando e agente deste plugin:
1. LEIA a configuração desse caminho. NÃO deste arquivo.
2. Se aquele arquivo não existir ou ainda contiver marcadores [PREENCHER], PARE antes de
   qualquer trabalho substantivo. Diga: "Este plugin precisa de setup antes de gerar algo
   útil. Rode /imobiliario-juridico:cold-start-interview — leva ~10-15 min e todo comando
   depende disso. Sem ele, os outputs saem genéricos e podem não bater com a prática da
   imobiliária." NÃO prossiga com configuração placeholder. As únicas skills que rodam sem
   setup são a própria /imobiliario-juridico:cold-start-interview e a flag --check-integrations.
3. O setup e a cold-start-interview ESCREVEM naquele caminho, criando os diretórios pais.
4. No primeiro uso após uma atualização, se existir um CLAUDE.md preenchido no caminho de
   cache antigo (~/.claude/plugins/cache/kpa30/imobiliario-juridico/<versao>/CLAUDE.md) mas
   não no caminho de config, copie-o para o caminho de config antes de prosseguir.
5. ESTE arquivo (o que você está lendo) é o TEMPLATE. Ele acompanha o plugin e mostra a
   estrutura que a config deve ter. É substituído a cada atualização. Nunca grave dados do
   usuário aqui.

**Perfil compartilhado da empresa.** Fatos gerais (quem é a imobiliária, onde atua, CRECI,
postura de risco, pessoas-chave) vivem em
`~/.claude/plugins/config/kpa30/perfil-empresa.md` — um nível acima deste arquivo,
compartilhado por todos os plugins do KPA30. Leia-o antes do perfil da prática. Se não
existir, o setup deste plugin o cria.
-->

# Perfil da Prática — Locação Imobiliária

*Este arquivo é escrito pela cold-start-interview no primeiro uso. Até lá, é um template
com marcadores [PREENCHER]. Não trabalhe a partir dele: leia a config real.*

## Identificação

- **Imobiliária:** [PREENCHER — ex.: Impar Imóveis]
- **CRECI:** [PREENCHER]
- **Responsável / corretor:** [PREENCHER]
- **Comarca / cidade-base:** [PREENCHER — ex.: Joinville/SC]
- **Foro de eleição padrão:** [PREENCHER]

## Lado da operação

- **Lado padrão:** [PREENCHER — `locador` (representa o proprietário) | `locatario` | `ambos`]

## Playbook de locação

### Garantia locatícia
- **Modalidade preferida:** [PREENCHER — fiança | caução (até 3 aluguéis) | seguro-fiança | título de capitalização]
- **Só uma modalidade por contrato** (art. 37, parágrafo único da Lei 8.245/91). Sinalizar se houver cumulação.

### Reajuste
- **Índice padrão:** [PREENCHER — IGP-M | IPCA | INCC]
- **Periodicidade mínima:** anual (12 meses) — sinalizar cláusula que tente reajuste em prazo menor.

### Prazo e rescisão
- **Prazo padrão:** [PREENCHER — ex.: 30 meses residencial]
- **Multa por rescisão antecipada:** proporcional ao tempo restante (art. 4º). Sinalizar multa cheia.
- **Denúncia vazia:** condições em que se aplica.

### Encargos
- **IPTU / condomínio / seguro incêndio:** [PREENCHER — quem paga o quê]
- **Taxa de lixo e demais taxas:** [PREENCHER]

### Cláusulas que sempre exigem atenção
- [PREENCHER — ex.: benfeitorias e direito de retenção, vistoria de entrada/saída, renúncia indevida de direitos]

## Matriz de escalonamento

| Situação | Quem decide |
|---|---|
| Valor de aluguel acima de [PREENCHER] | [PREENCHER] |
| Garantia fora da modalidade padrão | [PREENCHER] |
| Cláusula que renuncia direito do locador | [PREENCHER] |
| Imóvel comercial com ponto/fundo de comércio | [PREENCHER] |

## Estilo da casa

- **Destino dos alertas (reajuste/vencimento):** [PREENCHER — número/grupo de WhatsApp ou e-mail]
- **Tom do memorando:** [PREENCHER — direto e sem juridiquês, para proprietário leigo]
- **Nomenclatura de arquivos:** [PREENCHER]

## Integrações disponíveis

*Preenchido por --check-integrations. Marque ✓ só o que uma chamada de MCP confirmou.*

- Google Drive: ⚪ não testado
- WhatsApp: ⚪ não testado
- Asaas: ⚪ não testado

## Guardrails (não configuráveis)

- Todo output é **rascunho para revisão humana**, não aconselhamento jurídico.
- Sempre citar o artigo da Lei 8.245/91 (ou norma aplicável) que embasa cada flag.
- Divulgar jurisdição/comarca assumida quando relevante.
- Na dúvida entre duas leituras, adotar a **mais conservadora para o lado padrão** e sinalizar.
