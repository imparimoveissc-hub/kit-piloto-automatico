# Checklist Pre-Publicacao - Landing Page

> Aplicar ANTES de subir LP em producao. Cada item bloqueador (marcado [B]) precisa estar OK ou nao publica.
> Tempo medio: 30-45 min pra LP grande, 15 min pra LP de captura.

---

## Cabecalho

```yaml
projeto: "{{NOME_LP}}"
url_alvo: "{{URL_PRODUCAO}}"
url_staging: "{{URL_PREVIEW}}"
data_revisao: "[AAAA-MM-DD]"
revisor: "[Nome]"
```

---

## 1. COPY (revisor le linha por linha)

### Voz e tom

- [ ] Voz humana pt-BR (sem "em milissegundos", "paradigma", "transformacao", "voce merece")
- [ ] Vocativos coerentes com avatar (cara/mano/galera nao mistura com prezado/caro)
- [ ] Mistura "voce/tu" natural quando cabe
- [ ] Marcadores coloquiais Tier 1 presentes (po, tipo, basicamente, simples, na real)
- [ ] Frases curtas / paragrafos de 2-4 linhas
- [ ] Reticencias presentes em copy longa (minimo 3 por 500 palavras em VSL/presell)
- [ ] Perguntas retoricas pra puxar leitura
- [B] Zero em-dash `—` ou en-dash `–` (proibido em LP por rule global)
- [B] Zero frases banidas: "amigao", "te vejo do outro lado", "imagine so", "presta atencao agora"

### Estrutura

- [ ] Headline > Subheadline > CTA em hero (acima da dobra)
- [ ] Pelo menos 3 elementos de prova social
- [ ] CTA repetido a cada 2-3 secoes (minimo 3 CTAs na pagina)
- [ ] Garantia visivel e explicita (se aplicavel)
- [ ] FAQ cobrindo 5-10 objecoes principais

### Headline

- [ ] Promessa especifica (numero + prazo + para quem)
- [ ] Avatar reconhece "isso e pra mim" em 5 segundos
- [ ] Sem clickbait vazio ("Isso vai mudar sua vida")
- [B] Compreensivel em 1 leitura

### CTA

- [ ] Verbo + beneficio (nao "saiba mais")
- [ ] Texto consistente em todos os botoes principais
- [ ] Botao destaca visualmente (cor / tamanho)
- [B] Botao primario clicavel e visivel sem rolar

---

## 2. ELEMENTOS VISUAIS

### Imagens

- [ ] Todas as imagens otimizadas (WebP ou JPG comprimido)
- [ ] Imagens carregam < 200kb cada
- [ ] Alt text em todas as imagens (acessibilidade + SEO)
- [ ] Sem foto generica estoque obvio (mulher sorrindo no escritorio com headset)
- [ ] Foto autoral do criador/dono (se aplicavel)

### Logos

- [ ] Logo da empresa visivel no topo
- [ ] Logo wall (se aplicavel) tem 6+ logos REAIS (nao usar se tem menos)
- [ ] Logos com aspect ratio uniforme

### Mockups do produto

- [ ] Pelo menos 1 mockup visual do produto/entregavel
- [ ] Mockup em 3D ou em contexto (mao segurando, laptop aberto)

### Cores e tipografia

- [ ] Paleta consistente (max 3 cores principais + neutros)
- [ ] Hierarquia tipografica clara (h1 > h2 > h3 > body)
- [B] H3 NAO usa fonte serifada (so h1 e h2 sao serif - rule global lp-antitravessao)
- [ ] Tamanho minimo do corpo de texto: 16px desktop, 15px mobile
- [ ] Contraste WCAG AA minimo (texto escuro em fundo claro ou inverso)

### Layout

- [ ] LP nao e chapa de uma cor so (alternar BG dark/light por secao - rule lp-relevo-widgets)
- [ ] Inclui widgets reais: mock de WhatsApp / dashboard / depoimento card / logo wall
- [ ] Espacamento generoso (nao denso demais)
- [ ] Maximo de 1 fonte serifada + 1 sans (nao misturar 4 fontes)

---

## 3. TECNICO (DESKTOP)

### Performance

- [ ] LP carrega em menos de 3 segundos no Lighthouse mobile (4G)
- [ ] Score Lighthouse: Performance > 70, Best Practices > 90, SEO > 90
- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] CLS (Cumulative Layout Shift) < 0.1

### HTML / Meta tags

- [ ] `<title>` correto e descritivo (< 60 caracteres)
- [ ] Meta description preenchida (< 160 caracteres)
- [ ] OG tags (og:title, og:description, og:image) preenchidas
- [ ] Twitter card meta tags preenchidas
- [ ] Favicon presente

### Funcionalidade

- [B] Todos os CTAs levam ao destino correto (testar clicando)
- [B] Formularios submetem e geram lead na ferramenta de CRM/email
- [B] Pagina /obrigado aparece apos submit (se houver)
- [ ] Links externos abrem em nova aba (target="_blank")
- [ ] Anchor links (#secao) funcionam
- [ ] Botao WhatsApp tem link `wa.me/55...` correto

### Tracking

- [ ] Pixel do Meta instalado e disparando PageView
- [ ] Pixel do Google Ads (se rodar Google) instalado
- [ ] Eventos customizados configurados (Lead no submit, ViewContent na hero)
- [ ] Conversion API configurada (server-side) pra perda de cookie iOS 14+
- [ ] UTM source/medium/campaign preservada em formularios

---

## 4. TECNICO (MOBILE)

> 70%+ do trafego e mobile. Mobile NAO e "depois ajusta", e prioridade.

- [B] Layout responsivo funciona em iPhone (Safari) e Android (Chrome)
- [B] Botoes clicaveis com dedao (minimo 44x44px)
- [B] Texto legivel sem zoom (minimo 15px)
- [ ] Formulario funciona em teclado mobile (tipo correto: email/tel/text)
- [ ] Imagens nao quebram layout em mobile
- [ ] Video / VSL funciona em iOS Safari (player carrega + autoplay nao quebra)
- [ ] Hover states tem fallback pra touch (mobile nao tem hover)
- [ ] Sticky CTA mobile (botao fixo no rodape) se LP for longa

---

## 5. VTURB / VSL EMBED (se aplicavel)

> Critico se a LP tem VSL VTurb / Panda / Vimeo / YouTube

- [B] Container do iframe NAO tem `transform`, `opacity transition`, `filter`, ou animation
- [B] Nenhum pseudo-element com `mix-blend-mode` cobrindo o iframe
- [B] Iframe tem `border: 0`, ZERO `border-radius` (radius vai so no pai com overflow:hidden)
- [B] Nenhum sibling proximo com `animation` em `box-shadow`, `background-position`, `filter`
- [ ] Script SDK tem guard `window.__vturbSdkLoaded`
- [ ] Snippet oficial copiado literal (`this.onload=null, this.src=...`)
- [ ] Preloads oficiais VTurb colados no head
- [ ] `.vsl-wrap` tem `contain: layout paint style` + `isolation: isolate`
- [ ] Se Elementor: motion effects DESATIVADOS na section, column e widget HTML
- [ ] Cloudflare Rocket Loader DESATIVADO

> Ver rule `~/.claude/rules/vturb-embed.md` se VSL ainda reinicia.

---

## 6. LEGAL E COMPLIANCE

- [ ] Politica de privacidade linkada no rodape
- [ ] Termos de uso linkados no rodape
- [ ] Politica de reembolso linkada (se aplicavel)
- [ ] LGPD: campo de consentimento ANTES do submit (checkbox marcavel)
- [ ] CNPJ visivel no rodape
- [ ] Endereco fisico ou caixa postal no rodape
- [ ] Disclaimer de resultados (se aplicavel ao nicho - financeiro, saude, emagrecimento)

### Por nicho

| Nicho | Claims proibidos |
|---|---|
| Financeiro | "Garantia de retorno", "Lucro X%", "Sem risco" |
| Saude | "Cura", "Trata doenca X", claims medicos sem CRM |
| Emagrecimento | "Perda de X kg garantido", antes/depois enganoso |
| Educacao financeira | "Voce sera milionario", projecoes especificas |

---

## 7. EXPERIMENTACAO / A/B

- [ ] Variavel principal de teste definida (headline / CTA / preco / oferta)
- [ ] Ferramenta de teste configurada (Optimizely / VWO / Google Optimize / proprio)
- [ ] Sample size minimo calculado pra significancia
- [ ] Hipotese escrita: "Se mudar X, espero impacto Y, porque Z"

---

## 8. PRE-LANCAMENTO (24h ANTES)

- [B] LP staging revisada por minimo 2 pessoas (criador + pelo menos 1 fora)
- [B] Pixel disparando em modo Preview Mode (Facebook Events Manager)
- [B] Email automatico de boas-vindas testado (envio real pra email de teste)
- [B] Checkout / pagamento testado com cartao real (R$ 1) e estornado
- [B] Pagina /obrigado testada e linkada corretamente
- [ ] Equipe de suporte avisada do lancamento (vai vir pergunta no whatsapp)
- [ ] Capacidade de servidor / Vercel suporta volume esperado de trafego
- [ ] Backup do site atual feito (se substituindo outra LP)

---

## 9. POS-PUBLICACAO (PRIMEIRAS 24h)

- [ ] Lighthouse rodado em producao - score mantido
- [ ] Pixel disparando em producao (Events Manager mostrando real time)
- [ ] Formulario testado em producao (envio real)
- [ ] Cliquei em todos os CTAs em producao (mobile + desktop)
- [ ] WhatsApp do CTA testado (mensagem chega correta)
- [ ] Erro 404 / 500 monitorado nas primeiras 4h
- [ ] Trafego inicial vindo pela campanha confere com previsao
- [ ] CPL inicial dos ads dentro da meta (apos 100+ leads)

---

## 10. ITEMS POR TIPO DE LP

### LP de Captura
- [B] Formulario funcionando
- [B] Email automatico configurado e disparando
- [ ] Volume de campos minimo (3 ou menos)
- [ ] Pagina /obrigado com proxima etapa (NAO so "obrigado")

### LP de Vendas Direto
- [B] Botao de checkout testado e funcionando
- [B] Pagamento (cartao + boleto + pix) processando
- [ ] Order bump / upsell configurado (se aplicavel)
- [ ] Email de confirmacao de compra disparando

### LP de Servico B2B
- [B] Link de agenda (cal.com / calendly) funcionando
- [B] Notificacao de novo agendamento chega no email/slack
- [ ] Formulario de qualificacao curto (3-5 campos)

---

## 11. APROVACAO FINAL

| Quem | Aprovou? | Data |
|---|---|---|
| Copywriter / autor | [ ] | [DD/MM] |
| Designer / dev frontend | [ ] | [DD/MM] |
| Analista de trafego | [ ] | [DD/MM] |
| Cliente / socio (se aplicavel) | [ ] | [DD/MM] |

---

## Em caso de problema no go-live

1. **Bug bloqueante (formulario nao envia, checkout falha)**: tirar do ar, voltar staging
2. **Bug visual (algo desalinhado, imagem quebrada)**: corrigir no live em paralelo
3. **CPL/CPA pessimos primeira hora**: deixar rodar 24h pra ter sample, depois decide
4. **Erro 500 / pagina off**: alertar dev / Vercel, restaurar backup ate resolver

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Checklist inicial - 11 secoes |
