# Prompts: Pesquisa de Jurisprudencia

## Instrucao de Uso

Estes prompts ajudam a estruturar pesquisas juridicas usando IA. A IA nao substitui bases de dados oficiais (JusBrasil, TJSP, STJ, STF), mas ajuda a organizar a pesquisa, identificar teses e estruturar argumentos.

Use estes prompts com ChatGPT, Claude ou outra IA de sua preferencia. Sempre valide as informacoes em fontes oficiais antes de citar em pecas processuais.

---

## Prompt 1: Mapeamento de Teses Aplicaveis

**Quando usar:** No inicio do caso, para identificar quais teses juridicas podem fundamentar a demanda.

**Prompt:**

```
Atue como um assistente de pesquisa juridica. Preciso mapear as teses aplicaveis ao seguinte caso:

AREA DO DIREITO: [Ex: Direito do Trabalho]
SITUACAO FATICA: [Descrever os fatos principais do caso em 3-5 linhas]
PRETENSAO: [O que o cliente quer]

Para cada tese aplicavel, apresente:
1. Nome da tese
2. Fundamento legal (artigos de lei)
3. Resumo do argumento em 2-3 linhas
4. Se ha sumula ou jurisprudencia dominante sobre o tema (indicar o tribunal)
5. Nivel de consolidacao: pacificado / majoritario / controverso

Organize da tese mais forte para a mais fraca.
Inclua tambem possiveis contra-argumentos da parte contraria para cada tese.
```

**Resultado esperado:** Lista organizada de teses com fundamentacao, nivel de risco e contra-argumentos previstos.

---

## Prompt 2: Busca de Jurisprudencia por Tema

**Quando usar:** Quando ja sabe a tese e precisa encontrar decisoes de apoio.

**Prompt:**

```
Preciso encontrar jurisprudencia sobre o seguinte tema:

TEMA: [Ex: Horas extras habituais nao registradas no ponto eletronico]
TRIBUNAIS DE INTERESSE: [Ex: TST, TRT-2, TRT-15]
PERIODO: [Ex: Ultimos 3 anos]
RESULTADO DESEJADO: [Favoravel ao empregado / Favoravel ao empregador / Ambos]

Para cada decisao encontrada, apresente:
1. Tribunal e orgao julgador
2. Numero do processo/recurso
3. Data do julgamento
4. Ementa resumida (3-4 linhas)
5. Tese firmada
6. Relevancia para o meu caso (alta/media/baixa)

Sugira tambem termos de busca que eu possa usar nos sites oficiais dos tribunais para encontrar decisoes similares.
```

**Resultado esperado:** Lista de decisoes organizadas por relevancia + termos de busca para validacao em fontes oficiais.

---

## Prompt 3: Analise de Sumulas e Enunciados

**Quando usar:** Para verificar se existem sumulas, OJs ou enunciados aplicaveis ao caso.

**Prompt:**

```
Analise se existem sumulas, orientacoes jurisprudenciais (OJs) ou enunciados aplicaveis ao seguinte contexto:

AREA: [Ex: Direito do Trabalho]
TEMA ESPECIFICO: [Ex: Desvio de funcao sem alteracao contratual]
TRIBUNAIS: [Ex: TST, STJ, STF]

Para cada sumula/OJ/enunciado encontrado, apresente:
1. Numero e tribunal de origem
2. Texto integral (ou o mais proximo possivel)
3. Data de publicacao/atualizacao
4. Se esta vigente, cancelada ou revisada
5. Como se aplica ao meu caso
6. Se ha divergencia entre tribunais sobre o tema

Separe em: FAVORAVEIS ao meu cliente | DESFAVORAVEIS | NEUTRAS (dependem da interpretacao).
```

**Resultado esperado:** Mapa completo de sumulas aplicaveis, organizadas por posicionamento.

---

## Prompt 4: Construcao de Argumentacao Juridica

**Quando usar:** Depois de ter as teses e jurisprudencia, para montar a estrutura do argumento.

**Prompt:**

```
Com base nas seguintes informacoes, construa uma estrutura de argumentacao juridica:

TESE PRINCIPAL: [Descrever a tese]
FUNDAMENTO LEGAL: [Artigos de lei aplicaveis]
JURISPRUDENCIA DE APOIO: [Listar 2-3 decisoes]
FATOS DO CASO: [Resumo dos fatos que sustentam a tese]

Estruture o argumento seguindo esta logica:
1. PREMISSA NORMATIVA: Qual a norma aplicavel e o que ela determina
2. PREMISSA FATICA: Quais fatos do caso se enquadram na norma
3. CONCLUSAO: Por que o direito deve ser reconhecido
4. REFORCO JURISPRUDENCIAL: Decisoes que confirmam o entendimento
5. ANTECIPACAO DE CONTRA-ARGUMENTO: Qual a provavel objecao e por que ela nao procede

Use linguagem formal e tecnica, propria de pecas processuais.
Nao invente decisoes ou numeros de processo. Use apenas as informacoes que eu forneci.
```

**Resultado esperado:** Argumento estruturado pronto para ser incorporado em peca processual (apos revisao do advogado).

---

## Prompt 5: Comparativo de Posicionamentos entre Tribunais

**Quando usar:** Quando o tema e controverso e os tribunais divergem.

**Prompt:**

```
Preciso de um comparativo de posicionamento entre tribunais sobre o seguinte tema:

TEMA: [Ex: Validade de acordo extrajudicial com quitacao geral]
TRIBUNAIS PARA COMPARAR: [Ex: TST vs TRT-2 vs TRT-15]

Para cada tribunal, apresente:
1. Posicionamento predominante (favoravel/desfavoravel/dividido)
2. Fundamento utilizado
3. Decisoes representativas (se possiveis)
4. Tendencia recente (esta mudando? esta se consolidando?)

Ao final, faca uma analise:
- Qual tribunal e mais favoravel a minha tese?
- Existe risco de reforma em instancia superior?
- Qual a estrategia mais segura considerando a divergencia?

Apresente em formato de tabela comparativa seguida de analise.
```

**Resultado esperado:** Tabela comparativa de posicionamentos + analise estrategica sobre onde e como sustentar a tese.
