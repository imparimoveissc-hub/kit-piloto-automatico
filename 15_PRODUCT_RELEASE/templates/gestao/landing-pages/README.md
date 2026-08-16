# Templates de Landing Pages

Estruturas de copy + secoes pra montar landing pages. Sao templates de TEXTO + ARQUITETURA, nao templates de design. Servem como base do que voce vai colar no Lovable, Vercel, Elementor, Webflow, Framer ou Lovable.

## O que tem aqui

| Arquivo | Objetivo | Quando usar |
|---|---|---|
| `lp-servico-b2b.md` | LP de servico recorrente (B2B, agencia, consultoria, contabilidade) | Quem vende servico continuo |
| `lp-captura-isca-digital.md` | LP pra capturar lead com isca (ebook, planilha, mini curso) | Topo de funil, lista propria |
| `lp-vendas-direto.md` | LP de venda direta de produto/curso/oferta DTC | Tres camadas de awareness |
| `checklist-pre-publicacao.md` | QA gate antes de publicar | OBRIGATORIO antes de soltar |

## Filosofia

LP que converte NAO e LP bonita. E LP que:

1. **Diz pra quem e** (avatar reconhece em 3 segundos)
2. **Mostra o problema** que ele ja sente (ressonancia)
3. **Promete um resultado especifico** (numero + prazo)
4. **Prova que voce entrega** (cases, depoimentos, garantia)
5. **Tira a friccao** (CTA grande, formulario curto, garantia)

Beleza vem em segundo lugar. Copy primeiro.

## Voz dos templates

pt-BR humano profissional. Ver rule global `~/.claude/rules/voz-humana-pt-br.md`. Aplicar especialmente:

- Mistura "voce" + "tu" naturalmente
- Vocativos humanos (cara, meu querido, pessoal — dependendo do avatar)
- Reticencias respiram a copy
- Reframes em vez de dramatizacao
- Zero "em milissegundos", "paradigma", "transformacao"
- Acentos UTF-8 obrigatorios (cuidado se usar em payload externo)

## Stack tecnica recomendada (no V30)

| Volume | Stack |
|---|---|
| LP unica, decisao rapida | Lovable.dev → Vercel |
| Multiplas LPs com mesma identidade | Next.js no Vercel + componentes reutilizaveis |
| Cliente final pediu WordPress | Elementor (CUIDADO com VTurb — ver rule `~/.claude/rules/vturb-embed.md`) |
| Pagina simples com formulario | Tally.so ou Typeform direto |

## Antes de comecar QUALQUER LP

Preencher 1 vez:

```yaml
oferta:
  produto_ou_servico: "[Nome curto]"
  promessa_principal: "[Resultado especifico + prazo + para quem]"
  publico_alvo: "[Avatar em 1 linha: profissao + idade + situacao + dor principal]"
  awareness_level: "[Unaware / Problem-aware / Solution-aware / Product-aware / Most-aware]"
  oferta_irresistivel: "[Bonus + escassez + garantia + parcelamento]"
mecanismo:
  mup: "[Mecanismo unico do PROBLEMA - 1 linha]"
  mus: "[Mecanismo unico da SOLUCAO - 1 linha]"
  gimmick_name: "[Nome bonito da solucao]"
provas:
  numeros: ["[X clientes atendidos]", "[Y resultado X em Z tempo]"]
  cases: ["[Nome + resultado]"]
  depoimentos: ["[1 frase + nome + empresa]"]
  midia: ["[Onde foi citado]"]
restricoes:
  proibido_dizer: ["[claim X]"]
  obrigatorio_dizer: ["[disclaimer Y]"]
  nicho_compliance: "[saude / financeiro / juridico / regulado / livre]"
```

Esse bloco e seu input pra qualquer LP. Sem isso preenchido, NAO comeca.

## Como usar os templates

1. Le o `README.md` da pasta (este)
2. Escolhe a estrutura do template (servico B2B / captura / vendas direto)
3. Copia o template pro seu projeto
4. Substitui `[A PREENCHER]` pelos seus dados
5. Substitui `{{VARIAVEIS}}` no momento do build
6. Roda `checklist-pre-publicacao.md` antes de subir
7. Publica e testa

## Erros tipicos pra evitar

- **Comecar pela home page que fala da empresa** (errado: home corporativa converte mal). LP de oferta foca em UMA acao.
- **Headline generica** ("Sua melhor agencia de X"). Headline precisa NUMERO + PRAZO + AVATAR.
- **CTA repetido com texto generico** ("Saiba mais"). CTA = verbo + beneficio + urgencia.
- **Depoimento sem nome+foto+contexto**. Generico nao convence.
- **Garantia escondida**. Garantia e o final de objeçao. Bota em destaque.
- **Formulario com 8 campos**. Maximo 3 campos em topo de funil. Resto pergunta depois.

## Anti-padrao banidos

- Em-dash `—` ou `–` (banidos em LP por rule global, ver `lp-antitravessao`)
- H3 com fonte serifada (banido — so H1 e H2 sao serif; H3 vai sans medium)
- LP toda fundo branco chapado (banido — alternar BG dark/light por secao, ver rule `lp-relevo-widgets`)
- Sem widgets reais (banido — incluir mock de WhatsApp / dashboard / logo wall / depoimento)
- VSL no topo sem cuidado de anti-loop (se for VTurb / Converteai, ver rule `~/.claude/rules/vturb-embed.md`)
