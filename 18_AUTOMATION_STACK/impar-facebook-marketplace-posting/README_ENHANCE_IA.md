# 🤖 Marketplace Enhancement com IA (ChatGPT)

## O que foi implementado

Sistema automático que melhora **títulos e descrições** de publicações do marketplace usando a API OpenAI (ChatGPT), mantendo total factualidade.

### ✅ NOVO: Extração de preço com 100% de precisão
- Copia valores diretamente do site imparimoveis.com
- Mantém **todas as casas decimais** (centavos, reais, etc)
- Sem arredondamento
- Sem perda de formatação
- Exemplo: `R$ 1.500,50` → copiado exatamente assim

### Regras aplicadas:
- ✅ **SEM inventar nada** — usa apenas dados reais do imóvel
- ✅ **Mais atrativo** — deixa o conteúdo mais impactante
- ✅ **Emojis estratégicos** — chama atenção visualmente
- ✅ **Sem repetição** — cache inteligente evita reprocessar
- ✅ **Tags intactas** — mantém as 20 tags originais

## Exemplo de transformação

**Antes (original):**
```
Título: Apartamento para locacao no Centro - Joinville SC
Descrição: Excelente opcao para quem busca alugar um imovel...
```

**Depois (com IA):**
```
Título: 🛋️ Apartamento para Locação no Centro de Joinville SC - Apenas R$ 1.500,00! 🏙️ REF: IMPAR-001

Descrição: 🏢 **Apartamento para Locação no Centro de Joinville!** 🌟

🔑 **Referência:** IMPAR-001  
💰 **Preço:** R$ 1.500,00
📍 **Localização:** Centro, Joinville SC

[conteúdo mais estruturado e atrativo]
```

## Configuração

### 1. Arquivo `.env` (já criado)

```bash
# OpenAI Configuration for Marketplace Enhancement
OPENAI_API_KEY=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
OPENAI_MODEL=gpt-4o-mini
ENHANCE_MARKETPLACE_ENABLED=true
ENHANCE_VERBOSE=false
```

**Variáveis:**
- `OPENAI_API_KEY` — sua chave da API OpenAI
- `OPENAI_MODEL` — modelo a usar (gpt-4o-mini é rápido e barato)
- `ENHANCE_MARKETPLACE_ENABLED` — ativa/desativa enhancement (true/false)
- `ENHANCE_VERBOSE` — mostra logs detalhados de enhancement (true/false)

### 2. Dependência Python

```bash
pip install openai
```

## Como funciona

### Fluxo automático:

1. **Quando roda `generate_queue.py`**, o módulo `openai_enhance.py`:
   - ✅ Verifica se enhancement está habilitado (`.env`)
   - ✅ Valida chave API OpenAI
   - ✅ Carrega cache local para evitar chamadas desnecessárias
   - ✅ Chama ChatGPT apenas para imóveis novos
   - ✅ Retorna versão enhancida ou fallback para original

2. **Título é melhorado:**
   - Mantém tipo, bairro, cidade, preço, referência
   - Adiciona emojis relevantes
   - Máximo 120 caracteres

3. **Descrição é melhorada:**
   - Mantém estrutura factual
   - Reorganiza com emojis e markdown
   - Melhor legibilidade e impacto

4. **Tags permanecem intactas:**
   - As 20 tags originais são preservadas
   - Nenhuma alteração no `make_tags()`

## Cache e desempenho

- **Pasta `.enhance_cache/`** — armazena respostas para evitar chamadas repetidas
- **Hash MD5** — cada prompt unique tem seu cache
- **Fallback automático** — se IA falhar, usa versão original

### Para limpar cache:
```bash
rm -rf .enhance_cache/
```

## Ativar/desativar

### Desabilitar temporariamente:
Edite `.env`:
```bash
ENHANCE_MARKETPLACE_ENABLED=false
```
Roda com fallback (títulos e descrições originais).

### Reabilitar:
```bash
ENHANCE_MARKETPLACE_ENABLED=true
```

## Teste de extração de preço com precisão

```bash
python3 test_price_extraction.py
```

Resultado esperado:
```
✅ Preço com centavos         → R$ 1.500,50 ✓
✅ Preço inteiro               → R$ 2.500.000,00 ✓
✅ Preço com formatação        → R$ 3.200,75 ✓
✅ Preço com espaços           → R$ 1.200,30 ✓
✅ Preço com quebra de linha   → R$ 4.500, 99 ✓
```

## Teste rápido de enhancement IA

```bash
python3 test_enhance.py
```

Resultado esperado:
```
🧪 Testing Marketplace Enhancement Module
📌 Status: Enabled ✅

Testing title enhancement...
  Original: Apartamento para locacao no Centro - Joinville SC
  Enhanced: 🛋️ Apartamento para Locação no Centro...
  ✅ Title enhancement working!

Testing description enhancement...
  Enhanced length: 314 chars
  Preview: 🏢 **Apartamento para Locação no Centro de Joinville!**...
  ✅ Description enhancement working!

✨ All tests complete!
```

## Integração no pipeline

A integração é **100% automática**:

1. ✅ `generate_queue.py` importa `openai_enhance`
2. ✅ `marketplace_title()` chama `enhance_title()`
3. ✅ `make_description()` chama `enhance_description()`
4. ✅ Tags (20) permanecem inalteradas
5. ✅ Rascunhos salvos com títulos/descrições melhores

## Segurança

- ✅ **Chave API em `.env`** (não versionada no git)
- ✅ `.gitignore` criado para proteger credenciais
- ✅ Cache local, sem dados no OpenAI além da prompt
- ✅ Timeout de 30s para evitar travamentos

## Costs estimado

- **Modelo:** gpt-4o-mini (barato)
- **Por título:** ~0.0005 USD
- **Por descrição:** ~0.001 USD
- **Total por imóvel:** ~0.0015 USD (~R$ 0.008)

Exemplo: 100 imóveis = ~R$ 0.80

## Troubleshooting

### "Enhancement disabled"
- ✅ Verificar se `.env` existe
- ✅ Verificar se `OPENAI_API_KEY` está preenchida
- ✅ Executar: `python3 -c "import openai; print('OK')"`

### "INVALID_API_KEY"
- ✅ Copiar chave novamente do OpenAI dashboard
- ✅ Verificar se não tem espaços em branco

### Muito lento
- ✅ Cache pode ter ficado grande — rodar `rm -rf .enhance_cache/`
- ✅ Revisar se `VERBOSE=false` em `.env`

## Próximos passos (opcional)

- [ ] Integrar com Meta Ads (boostar performance)
- [ ] A/B testing: versão original vs enhanced
- [ ] Personalizacao por tipo de imóvel
- [ ] Logs de performance no Slack/WhatsApp

---

**Status:** ✅ Operacional  
**Última atualização:** 2026-07-17  
**Contato:** jonatasoft@gmail.com
