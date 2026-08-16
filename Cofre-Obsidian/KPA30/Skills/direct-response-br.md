# Skill: Direct Response Brasileiro 2026 — Operação Tática

```yaml
skill:
  id: direct-response-br
  version: "1.0.0"
  updated: "2026-05-04"
  category: paid-traffic
  agents: ["meta-dr-specialist", "scaling-strategist", "creative-analyst", "traffic-diagnostician"]
  description: "Conhecimento operacional Direct Response no contexto brasileiro: ABO/CBO, Oxigênio, kill criteria, lateralização, multi-account, tetos por nicho"
  complementa: ["meta-andromeda", "metricas-trafego-2026"]
```

---

## Posicionamento desta skill

`meta-andromeda` é técnica Meta Ads moderna (Andrômeda, GUIDED_CREATION, audience expansion). `metricas-trafego-2026` é multi-plataforma (KPIs, atribuição). **Esta skill é DR brasileiro puro** — práticas de mercado pt-BR pra ofertas DR (info-produto, nutraceutico, e-commerce DR).

Não substitui as duas — adiciona camada de contexto local.

---

## 1. Anatomia da operação DR brasileira (2026)

### Ciclo de validação

```
Briefing (oferta + criativo) → Subir ABO teste (R$80-150/dia × 3-5 dias)
  → Identificar 1-2 vencedores (ROAS estável >7 dias)
  → Migrar pra CBO de escala (R$500-2000/dia)
  → Lateralização Oxigênio (5-10 variações vencedor)
  → Horizontal (novos formatos/audiences) quando saturar
  → Multi-account quando bater teto da conta
```

**Tempo médio de validação a escala:** 14-30 dias.

### Estrutura padrão de campanha DR pt-BR

```
[Cliente]_[Funil]_[Objetivo]_[Tipo]_[Data]
Exemplo: <CLIENTE>_VSL_VENDAS_CBO_ABERTO_05-2026
```

**Naming cobre:** quem, qual funil, qual KPI, ABO ou CBO, "Aberto" ou "Remarketing", data.

---

## 2. ABO vs CBO — Decisão prática DR

| Estágio | Recomendação | Justificativa |
|---------|--------------|---------------|
| **Teste de criativo (3-5 dias)** | ABO R$80-150/dia | Cada criativo precisa orçamento próprio pra estatística |
| **Validação de audience** | ABO | Adset com budget próprio = teste limpo |
| **Escala (depois de validar)** | CBO R$500-2000/dia | Meta otimiza distribuição entre adsets |
| **Multi-criativos vencedores** | CBO | Andrômeda escolhe melhor automaticamente |

**Anti-padrão:** começar direto em CBO sem validar (Andrômeda alimenta o que tem mais sinal — pode descartar criativo bom prematuramente).

---

## 3. Kill Criteria DR — Padrão BR

Decididos **ANTES** de subir, não no calor da batalha.

### Por criativo individual

| Sintoma | Critério | Ação |
|---------|----------|------|
| Sem view assistida >25% | R$50 gasto sem | Mata em 24h |
| Sem 1 conversão | R$100 gasto sem | Mata em 24h |
| Hook rate <15% | 24h consecutivas | Mata |
| CPA 2x acima alvo | 48h consecutivas | Mata |
| Frequência >5 sem nova venda | Última semana | Mata ou expandir audience |

### Por adset

| Sintoma | Critério | Ação |
|---------|----------|------|
| Sem 1 venda + R$300+ gasto | 3 dias | Mata |
| Frequência >7 sem nova venda | 7 dias | Mata |
| ROAS <50% alvo | 7 dias | Mata |

### Por campanha

| Sintoma | Critério | Ação |
|---------|----------|------|
| ROAS <1x | 7 dias com volume | Mata + post-mortem |
| CPM 2x+ acima do nicho | 5 dias | Investigar antes de matar |

---

## 4. Lateralização Oxigênio — Conceito brasileiro

> Origem: comunidade pt-BR de tráfego (Lucas Maihach, V4 Company, comunidades de DR). Inspirado mas adaptado da "creative testing matrix" americana.

### Princípio

Criativo vencedor é ouro. Em vez de buscar próximo vencedor do zero, EXPANDIR vencedor com variações genuínas mantendo DNA, trocando elementos secundários.

### 5 métodos de variação genuína

| Método | Exemplo (pt-BR) |
|--------|-----------------|
| Mesmo HOOK, BODY diferente | Hook "Cara, perdi 800 reais ontem..." → muda body de problema/solução pra storytelling 1ª pessoa |
| Mesmo BODY, HOOK diferente | Mesma estrutura "Tutorial 5 passos" → muda hook de pergunta pra autoridade |
| Mesma COPY, ATOR diferente | Dono falando → cliente falando → especialista falando |
| Mesma ESTRUTURA, ÂNGULO diferente | Storytelling de medo → de desejo → de curiosidade |
| Mesmo CONCEITO, FORMATO diferente | Vídeo cru → carrossel ilustrado → slideshow + voz |

### Variação fake (NÃO funciona — Andrômeda detecta como 1 criativo)

- Mesmo vídeo em ratios 1:1, 9:16, 4:5 ❌
- Mesma imagem com botão azul vs vermelho ❌
- Mesma copy com 2 emojis diferentes ❌

### Métrica de sucesso da lateralização

- 30-40% das lateralizações batem >70% do CPA do original = saudável
- <20% batem = lateralização superficial (refazer com variação mais profunda)

---

## 5. Tetos de escala — Realidade BR

Mercado brasileiro tem audiência menor que EUA. Tetos saudáveis típicos:

| Tipo de oferta | Teto saudável (Meta + outras) |
|---|---|
| Info-produto baixo ticket (R$47-297) | R$3k-10k/dia |
| Info-produto médio ticket (R$497-997) | R$5k-15k/dia |
| Info-produto alto ticket (R$1.997+) | R$10k-30k/dia |
| Nutraceutico DR (R$197-497/kit) | R$5k-25k/dia |
| E-commerce geral | R$10k-50k/dia |
| E-commerce premium nicho | R$5k-20k/dia |
| Mentoria/Coaching alto ticket | R$2k-10k/dia |

**Sinais de teto atingido:**
- Lateralização não baixa CPA
- CPM crescendo sem aumentar audience
- Frequência alta em TODAS audiences (não só uma)
- ROAS Incremental cai mais que Standard

**Após teto:** multi-account, novo geo, novo produto/oferta, novo idioma.

---

## 6. Multi-account — Quando e como

### Quando usar

1. Esgotou Oxigênio (lateralização)
2. Esgotou horizontal (novas audiences/formatos)
3. CPM saturado mesmo com criativos novos
4. Cliente quer escalar além do teto

### Como (com segurança política Meta)

1. **NÃO duplicar conta no mesmo BM** (= ban)
2. Abrir novo BM (cliente final ou parceiro com BM próprio)
3. Replicar Pixel + CAPI (eventos isolados)
4. Replicar campanhas vencedoras manualmente (não usar API copy)
5. Variação mínima de criativos entre contas (pra não parecer spam)
6. Cuidado com payment method duplicado (red flag)

### Multi-account complexity

Útil pra escalar **acima de R$30k/dia**. Abaixo disso, custo operacional não compensa.

---

## 7. Naming convention DR brasileiro

Padrão consolidado por agências top BR:

```
[CLIENTE]_[FUNIL]_[OBJETIVO]_[TIPO]_[ABERTO/RMKT]_[VARIANTE]_[DATA]
```

Exemplos genéricos (substitua pelos seus):
- `[CA-<CLIENTE>] <PRODUTO>_PV-MINIVSL_VENDAS_ABO_ABERTO - novos estaticos`
- `bidcap-[CA-<CLIENTE>] <PRODUTO>_PV-MINIVSL_VENDAS_ABO_ABERTO - ad 04 e variações - DD/MM - Copy`

Padrão funciona. Mantém legibilidade pra escala (50+ campanhas).

---

## 8. Checkout brasileiro — Stack típica

| Plataforma | Características | Quando usar |
|------------|-----------------|-------------|
| **Hotmart** | Ecossistema info-produto, afiliados, recorrência fácil | Padrão pra info-produto |
| **Eduzz** | Similar Hotmart, taxa menor em alguns casos | Alternativa Hotmart |
| **Kiwify** | Foco UX moderno, integração Meta | Crescente em DR moderno |
| **Stripe + Pagar.me** | Customizável, ideal pra ofertas únicas | Quando precisa controle total |
| **PerfectPay** | Foco mentorias/alto ticket | Tickets >R$2k |
| **Cartpanda** | Foco e-commerce DR, otimizado checkout | E-commerce DR |
| **Shopify + Yampi/Cielo** | E-commerce tradicional | E-commerce escala |

**Compliance LGPD:** todos os principais já oferecem. Validar Consent Mode v2 (jun/2026).

---

## 9. Funis típicos DR pt-BR

### Funil VSL (info-produto / nutraceutico)
```
Ad → LP com VSL (15-25min) → Pitch (CTA aparece) → Checkout → (Upsell 1) → (Upsell 2) → Thank you
```
**Conversion rate típica:** 0.5-2.5% visitante→comprador.

### Funil Quiz
```
Ad → Quiz (5-10 perguntas) → Página resultado personalizada → Pitch + Oferta → Checkout
```
**Conversion rate típica:** 1.5-4% (mais alta que VSL pura).
**Vantagem:** segmentação automática + dados qualificados.

### Funil Direto (low ticket)
```
Ad → LP curta (problema-solução-CTA) → Checkout
```
**Conversion rate típica:** 2-5% (depende do ticket).
**Quando:** ticket baixo (R$47-197), oferta autoexplicativa.

### Funil Webinar (alto ticket)
```
Ad → LP captação → Webinar ao vivo OU evergreen → Pitch → WhatsApp/Aplicação
```
**Conversion rate típica:** 1-3% lead→comprador (mas ticket alto compensa).

---

## 10. Sazonalidade BR — Calendário DR

| Período | Comportamento | Estratégia |
|---------|---------------|-----------|
| Jan (pós-NY) | Resoluções (saúde, finanças, educação) | Captação alta |
| Fev-Mar (Carnaval) | Atenção dispersa | Reduzir budget durante Carnaval |
| Abr-Jun | Estável | Janela boa pra teste/escala |
| Jul (férias) | Atenção dispersa | Cuidado |
| Ago-Out | Crescente (volta às aulas + Black Friday warming) | Escala |
| Nov (Black Friday) | Pico | Promoção agressiva ou pausar (CPM dispara) |
| Dez | Misto (compras + 13º) | Depende do nicho |

---

## 11. Paused-First Protocol — Regra de Ouro

Toda criação de recurso novo no Meta Ads (campanha, adset, ad) **DEVE iniciar com `status: "PAUSED"`**. Validar no Gerenciador, corrigir, depois ativar.

### Por que

1. **Gasto durante validação:** ACTIVE direto = dinheiro queimado em config errado (mesmo que pequeno)
2. **`url_tags` não é editável:** se subir creative com UTM errado e ativar, tem que criar novo creative + atualizar ad (workaround). Em PAUSED, conserta antes
3. **Budget sharing:** `is_adset_budget_sharing_enabled` afeta distribuição entre adsets. Validação visual precisa de tempo
4. **Pixel + CAPI:** confirmar Test Events ANTES de qualquer impressão real
5. **Targeting:** placements específicos, exclusions, idioma — fácil errar, fácil consertar em PAUSED

### Como aplicar

```python
# Graph API:
campaign_payload = {
    "name": "...",
    "status": "PAUSED",  # ← obrigatório
    # ...
}
adset_payload = {"...", "status": "PAUSED"}
ad_payload = {"...", "status": "PAUSED"}

# CLI:
meta ads campaign create --status PAUSED ...
```

### Protocolo de validação (depois de criar PAUSED)

- [ ] Estrutura no Gerenciador (campaign + adset + ad visíveis)
- [ ] Targeting correto (geo, age, placement, device)
- [ ] Pixel + CAPI eventos disparando (Test Events do Pixel + Test Events do CAPI)
- [ ] UTMs no AdCreative (visíveis em Preview do Ad)
- [ ] Budget sharing flag conforme intenção
- [ ] Promoted object (pixel_id + custom_event_type)
- [ ] Attribution_spec correto (7d Click + 1d View + 1d Engaged padrão Meta 2026)
- [ ] Schedule (start_time + end_time se aplicável)

Só depois: `update --status ACTIVE` (ou via Gerenciador) — e SEMPRE com confirmação humana.

---

## 12. Graph API Quirks (quando CLI não basta)

CLI cobre 80% — pra setup avançado, Graph API direto via Python no venv do `meta-ads-cli` (criado pelo `/meta-cli-install`). No Windows o venv vive dentro do WSL Ubuntu; no macOS/Linux fica nativo. Path típico: `$HOME/.local/share/pipx/venvs/meta-ads-cli/bin/python`. Token vem de variável de ambiente carregada do `.env` (NUNCA hardcoded).

### Quando ir pra Graph API
- Placements específicos (Stories-only, Feed-only)
- `is_adset_budget_sharing_enabled` (declarar `false` em ABO — agora obrigatório 2026)
- `promoted_object` completo (pixel + custom_event_type)
- `url_tags` em AdCreative
- `attribution_spec` customizado
- Upload de imagem direto (`/adimages` → `image_hash`)

### Armadilhas conhecidas

1. **`url_tags` no AdCreative, NÃO no Ad** — fácil errar nível
2. **`url_tags` não é editável depois** — criar novo creative + atualizar ad
3. **Upload de imagem ANTES do creative** — `/adimages` retorna `image_hash`, usar em `object_story_spec`
4. **Stories-only = 4 campos juntos:**
   ```python
   targeting["device_platforms"] = ["mobile"]
   targeting["publisher_platforms"] = ["facebook", "instagram"]
   targeting["facebook_positions"] = ["story"]
   targeting["instagram_positions"] = ["story"]
   ```
5. **`is_adset_budget_sharing_enabled`** obrigatório declarar (geralmente `false` em ABO)

Detalhes técnicos completos: `~/.claude/.../memory/reference_meta_ads_cli_vs_graphapi.md`

---

## 13. Anti-Patterns BR (erros comuns)

1. **Targeting de interesse 5+ camadas** — mata Andrômeda
2. **Restringir placement (só feed, sem Reels)** — -40-60% performance
3. **Edit-loop dentro de learning phase** — reseta tudo
4. **Tracking sem CAPI** — ROAS é fantasma (-30% accuracy)
5. **Pixel mal instalado em GTM** — eventos disparando errado
6. **Naming inconsistente** — vira caos com 50+ campanhas
7. **CBO antes de validar criativo** — alimenta o pior, descarta o bom
8. **Subir <5 criativos** — Andrômeda precisa volume pra otimizar
9. **Lateralização fake** — ratios diferentes ≠ variação genuína
10. **Ignorar baseline do cliente** — usar benchmark genérico mascara problema

---

## 12. Glossário BR específico

| Termo | Significado |
|-------|-------------|
| **Oxigênio** | Lateralização de criativo vencedor (origem: comunidade pt-BR) |
| **Lateralização** | Variação genuína de criativo (mantém DNA, troca elementos) |
| **Aberto** | Campanha cold (audiência fria) |
| **RMKT** | Remarketing (warm/hot) |
| **Sangue novo** | Criativo recém-subido pra refresh |
| **Mata** | Pausar criativo/adset/campanha |
| **Bate** | Performa bem (criativo "que bate" = funciona) |
| **CA** | Custom Audience (lista de compradores, engajadores) |
| **CBO/ABO** | Campaign/Adset Budget Optimization |
| **Bid cap** | Limite máximo de bid (controle de CPA) |
| **Funil aberto** | Campanha pra audiência cold (não retargeting) |

---

## Fontes e referências (pt-BR DR)

- Referencias externas de chamadas/comunidade de trafego podem ser anexadas ao workspace do cliente quando existirem; no V30 canonico, use `04_DIRETRIZES/traffic-diretrizes.md` e os arquivos de `11_TRAFFIC_STACK/`.
- Comunidade V4 Company / GD / Klickpages
- Jon Loomer Digital (referência internacional adaptada)
- Hotmart Stats (interno)
- AppsFlyer Industry Reports

---

**STATUS:** ✅ Inteligência atualizada Mai/2026 | Próxima revisão: Ago/2026
