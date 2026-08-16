# 🔁 Regra de Deduplicação — Imóveis Repetidos

**Data:** 2026-07-24  
**Status:** ✅ ATIVA E DOCUMENTADA  
**Aplicável a:** Todas as publicações do Marketplace (rotina horária, grupos, Messenger)

---

## 📌 Regra Principal

> **NUNCA publicar o mesmo imóvel (código) duas vezes.**  
> Circula a fila inteira UMA VEZ antes de repetir.

### Como funciona:

1. **Registro de publicados**: Cada imóvel publicado com sucesso entra em `marketplace-publicados-log.csv` com status `ok`
2. **Checagem antes de publicar**: O script `publish_daily_from_fila.py` (linha 123) filtra:
   ```python
   rows = [r for r in rows if r["codigo_imovel"] not in feitos]
   ```
   onde `feitos` = todos os códigos já publicados com status `ok`
3. **Resultado**: O imóvel é **pular na fila** automaticamente e nunca é publicado novamente

---

## 📊 Monitoramento

Para visualizar o histórico de publicados:
```bash
tail -20 05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv
```

Campos:
- `data`: timestamp da publicação
- `codigo`: referência do imóvel (ex: CS0104, GM0137)
- `titulo`: título publicado
- `status`: `ok` = publicado com sucesso (outros valores = falha)
- `detalhe`: mensagem de erro se houver

---

## ⚡ EXCEÇÃO MANUAL — Publicar um Repetido

Se Jonata quer **re-publicar um imóvel específico** que já foi publicado:

### Opção A: Remover do log (recomendado)
```bash
# Remover a linha do imóvel do log
grep -v "^.*,CODIGO_AQUI," 05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv > /tmp/temp.csv && mv /tmp/temp.csv 05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv

# Exemplo real:
grep -v "^.*,CS0104," 05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv > /tmp/temp.csv && mv /tmp/temp.csv 05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv
```

Depois:
1. Readicionar o imóvel à fila `fila-postagens-venda.csv` com data de hoje
2. Rodar a publicação normal
3. ✅ Imóvel será publicado novamente

### Opção B: Publicar manualmente via UI
Se quer publicar algo fora da fila:
1. Usar o script `fb_interactive.py` (modo manual)
2. Clicar nos campos e preencher dados do imóvel
3. Publicar direto no Facebook

---

## 🛡️ Segurança

- **Sem sobreposição**: O sistema nunca vai ficar em loop publicando o mesmo imóvel
- **Auditável**: Todo publicado fica registrado com data/hora
- **Reversível**: Qualquer exceção manual é explícita e rastreável via grep no CSV

---

## 📋 Checklist de Qualidade

Antes de pedir uma re-publicação, considere:

- [ ] Imóvel foi publicado com sucesso? (verifica `status: ok` no log)
- [ ] Já faz quantos dias? (analisa coluna `data` do log)
- [ ] Razão? (vendido, alteração de preço, seasonal, etc.)
- [ ] Retirar do log ou pedir novo procedimento?

---

**Última atualização:** 2026-07-24 20:30 UTC
