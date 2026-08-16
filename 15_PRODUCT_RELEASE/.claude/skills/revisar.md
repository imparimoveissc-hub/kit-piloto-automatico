---
name: revisar
description: Revisa materiais com checklist de qualidade
---

# /revisar — Revisao de Qualidade

## Processo

### 1. Receber material
Pergunte: "Cole o material ou indique o arquivo pra revisar."

### 2. Aplicar checklist

| Criterio | O que verificar |
|----------|----------------|
| Ortografia | Erros de portugues, acentuacao, concordancia |
| Clareza | Frases confusas, ambiguas ou longas demais |
| Tom de voz | Consistente com o config.md e briefing do cliente |
| Adequacao | Atende o que foi pedido no briefing? |
| CTA | Tem chamada pra acao clara? |
| Dados | Numeros estao corretos? Fontes citadas? |
| Formato | Estrutura visual adequada pro canal? |

### 3. Classificar problemas

- **CRITICO:** Erro que compromete a entrega (dado errado, fora do escopo, erro grave)
- **MELHORIA:** Pode melhorar (tom inconsistente, CTA fraco, frase confusa)
- **OPCIONAL:** Sugestao (sinonimo melhor, formatacao alternativa)

### 4. Entregar revisao

```markdown
## Revisao — [titulo do material]

### Resumo
[X] criticos | [X] melhorias | [X] opcionais

### Problemas encontrados

**CRITICO:**
- [problema] → [correcao]

**MELHORIA:**
- [problema] → [sugestao]

**OPCIONAL:**
- [sugestao]

### Versao revisada
[material completo corrigido]

### Changelog
| Item | Antes | Depois | Motivo |
|------|-------|--------|--------|
| [trecho] | [original] | [corrigido] | [por que] |
```

### 5. Proximo passo
Pergunte: "Revisado. Quer formatar pra entrega? (/entregar)"
