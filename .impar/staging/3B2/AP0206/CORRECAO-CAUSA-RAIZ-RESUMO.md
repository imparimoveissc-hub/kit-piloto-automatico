# CORREÇÃO DE CAUSA RAIZ — AP0206 MAPEAMENTO

**Data:** 2026-07-23  
**Status:** ✅ RAIZ CORRIGIDA, PRONTO PARA REEXECUÇÃO FASE A  
**Severidade:** CRÍTICA (erro de mapeamento bloqueia toda a coleta)

---

## 📋 Diagnóstico

### Problema Identificado
AP0206 estava resolvendo para **Urban Orquídeas** (Joinville, na planta, Pirabeiraba) quando deveria resolver para um **apartamento de LOCAÇÃO em São Francisco do Sul**.

### Onde Estava o Erro
**Arquivo:** `05_WORKSPACE/clientes/impar-imoveis/automacoes/cadastro-imoveis/fontes/AP0206/listing.json`  
**Tipo:** Mapeamento incorreto na fonte de cadastro  
**Causa:** Data entrada original apontava URL errada de projeto (Rogga)

### URL Incorreta
```
https://www.rogga.com.br/empreendimentos/joinville/urban-orquideas
```

---

## ✅ Correção Executada

### Arquivo Corrigido
`listing.json` do AP0206 foi **completamente reescrito** com:
- URL corrigida
- ID numérico extraído (4298360)
- Operação identificada (locacao)
- Tipo identificado (apartamento)
- Localização atualizada (São Francisco do Sul, SC, Ubatuba)
- Todos os campos de dados marcados como "A COLETAR" (não reutilizar dados incorretos de Urban Orquídeas)

### URL Corrigida
```
https://www.imparimoveis.com/imovel/4298360/apartamento-locacao-sao-francisco-do-sul-sc-ubatuba
```

---

## 🔐 Nova Regra de Validação de Mapeamento

Implementada **regra de 5 etapas obrigatórias** (arquivo: `mapping-validation.json`):

1. **Extração de Componentes URL**  
   - Validar padrão imparimoveis.com/imovel/{ID_NUMERICO}/...
   - Extrair ID, operação, tipo, localização

2. **Validação URL↔ID↔Página**  
   - Acessar página public
   - Confirmar ID numérico em HTML
   - Confirmar operação, tipo, localização

3. **Coleta de Dados Estruturados**  
   - Dormitórios, suítes, banheiros, vagas
   - Áreas (total, privativa, construída)
   - Preço, condomínio, IPTU, adicionais
   - Descrição, características

4. **Validação de Galeria Completa**  
   - Todas as imagens da página
   - Verificar pertencimento ao imóvel correto

5. **Verificação de Integridade no CRM**  
   - Confirmar código livre em painel1.imobibrasil.app.br
   - Escalate se já usado

---

## 📊 Validação da Correção

✅ **Raiz identificada:** listing.json  
✅ **Arquivo corrigido:** Sim  
✅ **URL mapeada:** https://www.imparimoveis.com/imovel/4298360/apartamento-locacao-sao-francisco-do-sul-sc-ubatuba  
✅ **ID numérico:** 4298360  
✅ **Operação:** locacao  
✅ **Tipo:** apartamento  
✅ **Localização:** São Francisco do Sul, SC, Ubatuba  
✅ **Regra de validação:** Implementada em mapping-validation.json

---

## 🚀 Próximos Passos — Pronto para REEXECUÇÃO FASE A

**COM AUTORIZAÇÃO DO USUÁRIO:**

1. Acessar página pública da URL corrigida
2. Aplicar 5-etapas de validação de mapeamento
3. Coletar dados estruturados:
   - Operação: LOCAÇÃO
   - Preço aluguel: [A COLETAR]
   - Dormitórios: [A COLETAR]
   - Suítes: [A COLETAR]
   - Banheiros: [A COLETAR]
   - Vagas: [A COLETAR]
   - Áreas: [A COLETAR]
   - Condomínio: [A COLETAR]
   - IPTU: [A COLETAR]
   - Adicionais: [A COLETAR]
   - Descrição: [A COLETAR]
   - Características: [A COLETAR]
   - Galeria: [A COLETAR]

4. Gerar arquivos FASE A:
   - `property-payload.json` (dados completos)
   - `source-comparison.json` (validação de sources)
   - `image-gallery-audit.json` (validação de imagens)
   - `fees-audit.json` (validação de taxas)
   - `property-status.json` (marcado READY_FOR_COLLECTION)
   - `FASE-A-RESUMO.json` (resumo para aprovação)

---

## 🎯 Resumo para Aprovação

**Erro:** AP0206 mapeado para projeto errado (Urban Orquídeas)  
**Correção:** listing.json atualizado com URL correta de São Francisco do Sul  
**Validação:** Nova regra de 5-etapas implementada e documentada  
**Status:** ✅ PRONTO PARA REEXECUÇÃO FASE A COM URL CORRIGIDA

**Aguardando:** Autorização do usuário para iniciar coleta de dados com URL corrigida.
