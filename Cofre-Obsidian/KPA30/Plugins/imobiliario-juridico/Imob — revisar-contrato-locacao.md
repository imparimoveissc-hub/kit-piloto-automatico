---
name: revisar-contrato-locacao
description: >
  Revisa um contrato de locação (residencial ou comercial) contra o playbook da imobiliária
  e a Lei 8.245/91. Identifica o tipo pelo cabeçalho, roda o checklist de cláusulas de risco,
  calibra pelo lado padrão (locador/locatário) e devolve um memorando com flags citando o
  artigo aplicável. Use quando o usuário disser "revisa esse contrato", "checa essa locação",
  "esse contrato de aluguel tá ok?", ou anexar uma minuta de locação.
argument-hint: '[caminho do arquivo | link do Drive | texto colado]'
---

# /revisar-contrato-locacao

Revisa uma minuta de locação contra o playbook em
`~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`.

## Instruções

1. **Carregue `~/.claude/plugins/config/kpa30/imobiliario-juridico/CLAUDE.md`.** Se houver
   marcadores `[PREENCHER]`, pare e peça: "Rode `/imobiliario-juridico:cold-start-interview`
   primeiro — preciso aprender o playbook antes de revisar contra ele." Leia também o perfil
   compartilhado da empresa e o campo `**Lado padrão:**`.

2. **Obtenha o documento:** caminho de arquivo, link do Drive ou texto colado. Se nada vier, peça.

3. **Leia o cabeçalho primeiro.** Identifique:
   - Natureza: **residencial** ou **comercial** (muda direitos — ex.: ação renovatória, art. 51).
   - Modalidade de garantia declarada.
   - Prazo e índice de reajuste.

   Isso é o sinal de roteamento. Não confie só em palavras soltas do corpo.

4. **Rode o checklist contra a Lei 8.245/91**, marcando cada item ✅ ok / ⚠️ atenção / 🔴 crítico:

   | Item | Verificar | Base legal |
   |---|---|---|
   | Garantia | Só **uma** modalidade; caução ≤ 3 aluguéis | art. 37 e 38 |
   | Reajuste | Índice do playbook; periodicidade **anual** (não menor) | Lei 9.069/95 / prática |
   | Prazo | Bate com o padrão da casa; residencial ≥ 30 meses permite denúncia vazia ao fim | art. 46 |
   | Multa rescisória | **Proporcional** ao tempo restante, não cheia | art. 4º |
   | Benfeitorias | Necessárias indenizáveis; renúncia genérica é ponto de atenção | art. 35 / Súmula 335 STJ |
   | Vistoria | Existe termo de entrada descrevendo o estado do imóvel | art. 23, III |
   | Encargos | IPTU/condomínio/seguro atribuídos conforme playbook | art. 22 e 25 |
   | Comercial: renovatória | Se comercial, checar requisitos de renovação/ponto | art. 51 |
   | Foro | Comarca de eleição coerente com o imóvel | — |

5. **Calibre pelo lado padrão.** Para `locador`, sinalize renúncias que fragilizem o proprietário;
   para `locatario`, o inverso. Na dúvida entre duas leituras, adote a mais conservadora para o lado
   padrão e diga isso explicitamente.

6. **Aplique a matriz de escalonamento.** Se algum ponto cai numa linha da matriz (valor, garantia
   fora do padrão, cláusula de renúncia, imóvel comercial), marque **[ESCALAR → quem]**.

7. **Se for gerar uma minuta nova em vez de revisar uma existente,** encaminhe para
   `/imobiliario-juridico:gerar-contrato-locacao`.

## Formato do memorando

```
📄 Revisão — [tipo] — [imóvel / partes]
Lado: [locador|locatário] · Comarca assumida: [x]

🔴 Críticos
• [cláusula] — [problema] — [art.] — sugestão: [correção concreta]

⚠️ Atenção
• ...

✅ Conforme
• [itens ok, em uma linha]

[ESCALAR → pessoa] se aplicável

⚠️ Rascunho para revisão do responsável. Não é aconselhamento jurídico.
```

## Exemplos

```
/imobiliario-juridico:revisar-contrato-locacao ~/Desktop/minuta.pdf
```

```
/imobiliario-juridico:revisar-contrato-locacao
```
