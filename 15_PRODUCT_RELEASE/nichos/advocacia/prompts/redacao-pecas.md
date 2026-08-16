# Prompts: Redacao de Pecas Processuais

## Instrucao de Uso

Estes prompts auxiliam na redacao e estruturacao de pecas processuais. A IA gera rascunhos estruturados que devem ser revisados, complementados e validados pelo advogado antes de qualquer uso.

A IA nao tem acesso a bases de dados em tempo real. Numeros de processos, datas de julgamento e teores de decisoes devem ser conferidos pelo advogado.

---

## Prompt 1: Rascunho de Peticao Inicial

**Quando usar:** Para gerar a primeira versao estruturada de uma peticao inicial.

**Prompt:**

```
Atue como assistente de redacao juridica. Com base nas informacoes abaixo, elabore um rascunho de peticao inicial:

TIPO DE ACAO: [Ex: Acao de cobranca]
JUIZO COMPETENTE: [Ex: Vara Civel da Comarca de Sao Paulo/SP]

AUTOR:
- Nome: [NOME]
- Qualificacao: [NACIONALIDADE, ESTADO CIVIL, PROFISSAO, CPF, RG, ENDERECO]

REU:
- Nome: [NOME/RAZAO SOCIAL]
- Qualificacao: [CNPJ, ENDERECO]

FATOS (em ordem cronologica):
1. [FATO 1]
2. [FATO 2]
3. [FATO 3]

FUNDAMENTOS JURIDICOS:
- [ARTIGO/LEI 1 e como se aplica]
- [ARTIGO/LEI 2 e como se aplica]

PEDIDOS:
1. [PEDIDO 1]
2. [PEDIDO 2]
3. [PEDIDO 3]

VALOR DA CAUSA: R$ [VALOR]

DOCUMENTOS QUE SERAO ANEXADOS:
- [DOC 1]
- [DOC 2]

Instrucoes de redacao:
- Linguagem formal e tecnica
- Paragrafos curtos e objetivos
- Fundamentacao com citacao dos dispositivos legais
- Pedidos claros e determinados
- Formato completo de peticao (cabecalho, qualificacao, fatos, direito, pedidos, fechamento)
```

**Resultado esperado:** Rascunho completo de peticao inicial, formatado e pronto para revisao do advogado.

---

## Prompt 2: Elaboracao de Contestacao

**Quando usar:** Quando representar o reu e precisar estruturar a defesa.

**Prompt:**

```
Atue como assistente de redacao juridica para a defesa. Elabore uma contestacao com base nas seguintes informacoes:

ACAO: [TIPO DA ACAO]
PROCESSO N.: [NUMERO]
JUIZO: [VARA/COMARCA]

PEDIDOS DO AUTOR (resumo):
1. [PEDIDO 1]
2. [PEDIDO 2]
3. [PEDIDO 3]

FATOS NARRADOS PELO AUTOR (resumo):
[RESUMIR OS PRINCIPAIS FATOS DA PETICAO INICIAL]

VERSAO DO REU (nosso cliente):
[DESCREVER A VERSAO DOS FATOS SEGUNDO O REU]

PRELIMINARES (se houver):
- [Ex: Inepcia da inicial / Falta de interesse de agir / Incompetencia]

ARGUMENTOS DE DEFESA (merito):
1. [ARGUMENTO 1 + fundamento legal]
2. [ARGUMENTO 2 + fundamento legal]
3. [ARGUMENTO 3 + fundamento legal]

PROVAS QUE O REU PRETENDE PRODUZIR:
- [TIPO DE PROVA]

Instrucoes:
- Impugnar especificamente cada fato e pedido do autor
- Apresentar preliminares antes do merito
- Fundamentar cada argumento com dispositivo legal
- Requerer a improcedencia total dos pedidos
- Linguagem formal, tecnica e objetiva
```

**Resultado esperado:** Rascunho de contestacao estruturada com preliminares, merito e pedidos, pronta para revisao.

---

## Prompt 3: Redacao de Recurso (Apelacao/Agravo)

**Quando usar:** Quando precisar recorrer de decisao desfavoravel.

**Prompt:**

```
Atue como assistente de redacao juridica recursal. Elabore a estrutura de um [APELACAO / AGRAVO DE INSTRUMENTO] com base nas informacoes:

DECISAO RECORRIDA:
- Tipo: [SENTENCA / DECISAO INTERLOCUTORIA]
- Data: [DATA]
- Resumo do que foi decidido: [RESUMIR A DECISAO]
- Ponto especifico que sera impugnado: [O QUE ESTA ERRADO NA DECISAO]

FUNDAMENTOS DO RECURSO:
1. [ERRO 1: Ex: Erro na valoracao da prova -- o juiz desconsiderou documento X]
2. [ERRO 2: Ex: Violacao do art. Y da lei Z]
3. [ERRO 3: Ex: Divergencia com jurisprudencia do tribunal]

PEDIDO RECURSAL:
[O QUE SE PEDE AO TRIBUNAL -- Ex: Reforma da sentenca para julgar procedente / Concessao da tutela negada]

JURISPRUDENCIA DE APOIO (se disponivel):
- [DECISAO 1]
- [DECISAO 2]

Instrucoes:
- Demonstrar o cabimento do recurso
- Narrar os fatos apenas na medida necessaria ao recurso
- Focar nos erros da decisao recorrida (error in judicando ou error in procedendo)
- Fundamentar cada ponto com legislacao e jurisprudencia
- Pedido claro de reforma ou anulacao
```

**Resultado esperado:** Estrutura completa do recurso com razoes fundamentadas, pronta para complementacao e revisao.

---

## Prompt 4: Manifestacao/Peticao Intermediaria

**Quando usar:** Para peticoes de andamento (juntada de documentos, impugnacao, manifestacao sobre calculo, etc.).

**Prompt:**

```
Elabore uma peticao intermediaria para o seguinte caso:

PROCESSO N.: [NUMERO]
JUIZO: [VARA/COMARCA]
PARTES: [AUTOR] vs [REU]
REPRESENTAMOS: [AUTOR/REU]

FINALIDADE DA PETICAO: [Ex: Impugnacao ao calculo de liquidacao / Juntada de novos documentos / Manifestacao sobre laudo pericial / Pedido de dilacao de prazo]

CONTEXTO:
[DESCREVER BREVEMENTE O MOMENTO PROCESSUAL E O QUE MOTIVOU ESTA PETICAO]

ARGUMENTOS/RAZOES:
1. [ARGUMENTO 1]
2. [ARGUMENTO 2]

PEDIDO ESPECIFICO:
[O QUE SE PEDE AO JUIZ]

DOCUMENTOS ANEXOS (se houver):
- [DOC 1]
- [DOC 2]

Instrucoes:
- Peticao objetiva e direta (sem necessidade de grande fundamentacao como em inicial)
- Referenciar o momento processual
- Fazer pedido claro
- Linguagem formal
```

**Resultado esperado:** Peticao intermediaria concisa, pronta para protocolo apos revisao.

---

## Prompt 5: Revisao e Melhoria de Peca Existente

**Quando usar:** Quando ja tem um rascunho e quer que a IA revise e sugira melhorias.

**Prompt:**

```
Revise a seguinte peca processual e sugira melhorias:

TIPO DA PECA: [Ex: Peticao inicial / Contestacao / Recurso]
AREA DO DIREITO: [Ex: Civel / Trabalhista / Tributario]

[COLAR O TEXTO DA PECA AQUI]

Analise os seguintes aspectos e apresente sugestoes:

1. ESTRUTURA: A peca segue a ordem logica adequada? Falta alguma secao?
2. CLAREZA: Os argumentos estao claros e bem encadeados?
3. FUNDAMENTACAO: Os dispositivos legais estao corretamente citados? Falta algum fundamento importante?
4. PEDIDOS: Os pedidos sao claros, determinados e coerentes com a fundamentacao?
5. LINGUAGEM: Ha erros de portugues, repeticoes ou termos inadequados?
6. PERSUASAO: O texto e convincente? Onde pode ser mais forte?
7. RISCOS: Ha algum ponto fraco que a parte contraria pode explorar?

Para cada ponto, apresente:
- O que esta bom (manter)
- O que precisa melhorar (com sugestao especifica de nova redacao)
- O que esta faltando (com sugestao do que incluir)
```

**Resultado esperado:** Analise critica da peca com sugestoes concretas de melhoria por topico.
