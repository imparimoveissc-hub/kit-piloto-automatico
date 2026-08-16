# Template — Proposta de Compra de Imóvel (Impar Imóveis)

Padrão **A4** com identidade visual Impar (laranja `#E8721C` + preto), certificado pela CRECI 8359 J.

## Como Usar

### 1. Copiar para novo projeto
```bash
cp -r 10_TEMPLATES_OPERACIONAIS/proposta-compra-imovel/ Desktop/Impar\ Imóveis/Proposta_[ENDERECO]_[DATA]/
```

### 2. Editar dados no HTML
Abra `template.html` e substitua:
- **Seção 1 (Imóvel):** tipo, endereço, matrícula, dimensões, área construída/terreno
- **Seção 2 (Vendedor):** nome, CPF, RG, data nasc., naturalidade, CNH
- **Seção 3 (Comprador):** deixar em branco ou preencher depois
- **Seção 4 (Financeiro):** valor total, percentual entrada/saldo, comissão
- **Datas:** data de emissão (cabeçalho + rodapé de assinaturas)

### 3. Render to PDF
```bash
cd Desktop/Impar\ Imóveis/Proposta_[ENDERECO]_[DATA]/
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="Proposta_[ENDERECO]_[DATA].pdf" \
  "template.html"
```

## Estrutura do Template

| Seção | Campo | Tipo |
|-------|-------|------|
| 1 | Identificação do Imóvel | Tabela (tipo, endereço, matrícula, dimensões, áreas) |
| 2 | Dados do(a) Vendedor(a) | Tabela (ID, RG, CNH, naturalidade, filiação) |
| 3 | Dados do(a) Comprador(a) | Tabela em branco (preencher depois) |
| 4 | Condições Financeiras | Tabela + barra laranja/preto (entrada, saldo, comissão) |
| 5 | Disposições Jurídicas | 8 cláusulas + base legal (CC + Lei 6.530/78) |
| — | Assinaturas | 3 campos (Comprador, Vendedor, Impar) |

## Variáveis Críticas

- **Cor laranja Impar:** `#E8721C`
- **Cor preto Impar:** `#111111`
- **CRECI:** 8359 J
- **CNPJ Impar:** 50.886.299/0001-00
- **Responsável:** Jonata de Oliveira
- **Endereço Impar:** Rua Princesa Izabel, 238 — Sala 315, Edif. Príncipe, Centro — Joinville/SC — CEP 89.201-904

## Regras de Preenchimento

1. **Arras confirmatórias (Cláusula 2):** sempre em % do valor total, pago no ato do contrato
2. **Comissão de intermediação (Cláusula 4):** valor em % sobre o total (padrão: 5%)
3. **Saldo restante:** 100% - Entrada %
4. **Validade da proposta:** 5 dias úteis (Cláusula 1)
5. **ITBI e escritura:** responsabilidade do comprador (Cláusula 5)
6. **Ônus anteriores:** responsabilidade do vendedor (Cláusula 6)

## Exemplo Recente

**Proposta_Boehmerwald_3713** (07/2026):
- Valor: R$ 290.000,00
- Entrada: 20% (R$ 58.000,00)
- Saldo: 80% (R$ 232.000,00)
- Arras: 20% (R$ 58.000,00)
- Comissão: 5% (R$ 14.500,00)
- Vendedor: Fabricio Eduardo Henriques
- Imóvel: Casa mista, 81 m² (42 madeira + 39 alvenaria), terreno 468 m²

## Customizações Futuras

- Adicionar seção de "Financiamento" (se aplicável)
- Adicionar "Termo de Vistoria" como anexo (A5)
- Implementar merge dinâmico de dados via JSON (para batch de múltiplas propostas)

---

**Template Version:** 1.0  
**Última atualização:** 2026-07-10  
**Mantém:** Jonata de Oliveira (Impar Imóveis)
