# Categoria 1: Briefing

> Prompts para extrair informacoes do cliente e montar escopo de trabalho.

---

### 1. Extrator de Briefing Completo

**Quando usar:** No primeiro contato com um cliente novo, para coletar todas as informacoes essenciais de uma vez.

**Prompt:**
```
Voce e um especialista em briefing para projetos de marketing digital. Preciso que voce me ajude a montar um briefing completo para o seguinte cliente:

DADOS DO CLIENTE:
- Nome da empresa: [NOME DA EMPRESA]
- Segmento/nicho: [NICHO]
- Site ou Instagram: [URL OU @]
- Servico contratado: [TRAFEGO PAGO / SOCIAL MEDIA / DESIGN / VIDEO]

Com base nessas informacoes, me faca exatamente 5 perguntas estrategicas que eu preciso enviar ao cliente para montar o briefing completo. As perguntas devem cobrir:
1. Objetivo principal (vendas, leads, seguidores, branding)
2. Publico-alvo (quem compra, idade, localizacao, comportamento)
3. Diferenciais e posicionamento (por que escolher essa empresa)
4. Historico de marketing (o que ja foi feito, o que funcionou)
5. Orcamento e expectativa de prazo

Depois de listar as 5 perguntas, simule respostas realistas baseadas no nicho informado e monte o BRIEFING ESTRUTURADO no seguinte formato:

## BRIEFING — [NOME DA EMPRESA]
**Data:** [DATA]
**Responsavel:** [SEU NOME]

### Objetivo
### Publico-Alvo
### Diferenciais
### Historico
### Orcamento e Prazo
### Proximos Passos
```

**Exemplo de resultado esperado:** Um documento de briefing com 6 secoes preenchidas, pronto para compartilhar com o cliente para validacao antes de comecar o projeto.

---

### 2. Mapeamento de Publico-Alvo do Cliente

**Quando usar:** Quando o cliente nao sabe descrever o publico dele ou quando voce precisa refinar a segmentacao para campanhas.

**Prompt:**
```
Preciso mapear o publico-alvo de um cliente para direcionar campanhas e conteudo. Me ajude com uma analise completa.

INFORMACOES DO CLIENTE:
- Empresa: [NOME DA EMPRESA]
- Produto/servico principal: [PRODUTO OU SERVICO]
- Faixa de preco: [PRECO MEDIO]
- Cidade/regiao de atuacao: [LOCAL]
- Ja tem clientes? [SIM/NAO — se sim, descreva o perfil dos 3 melhores clientes]

Com base nisso, me entregue:

1. PERFIL DEMOGRAFICO
   - Faixa etaria, genero predominante, localizacao, renda estimada

2. PERFIL COMPORTAMENTAL
   - Onde consome conteudo (Instagram, YouTube, TikTok, LinkedIn)
   - Como pesquisa antes de comprar
   - O que valoriza na hora da decisao

3. DORES PRINCIPAIS (top 5)
   - O que tira o sono desse publico em relacao ao problema que o cliente resolve

4. DESEJOS PRINCIPAIS (top 5)
   - O que esse publico quer alcançar

5. SEGMENTACAO PARA ANUNCIOS
   - Interesses para Meta Ads (minimo 10 sugestoes)
   - Palavras-chave para Google Ads (minimo 10 sugestoes)
   - Sugestao de publicos lookalike e remarketing

Formate tudo como um documento que eu possa anexar ao briefing do cliente.
```

**Exemplo de resultado esperado:** Documento com 5 blocos detalhados incluindo perfil demografico, comportamental, lista de dores/desejos e segmentacoes prontas para configurar em plataformas de anuncios.

---

### 3. Definicao de Tom de Voz da Marca

**Quando usar:** Ao iniciar o trabalho de social media ou copy para um cliente, para garantir consistencia em todas as comunicacoes.

**Prompt:**
```
Preciso definir o tom de voz de uma marca para garantir consistencia em todos os conteudos e comunicacoes. Me ajude a construir esse guia.

INFORMACOES DA MARCA:
- Nome: [NOME DA EMPRESA]
- Segmento: [NICHO]
- Publico-alvo resumido: [DESCRICAO BREVE DO PUBLICO]
- Como o dono da empresa fala? [FORMAL / INFORMAL / TECNICO / DESCONTRAIDO]
- Marcas que admira (referencias): [LISTA DE 2-3 MARCAS]
- Palavras que a marca NUNCA usaria: [LISTA]

Me entregue um GUIA DE TOM DE VOZ com:

1. PERSONALIDADE DA MARCA
   - Se a marca fosse uma pessoa, como ela seria? (3 adjetivos + descricao)

2. TOM DE COMUNICACAO
   - Escala: formal <-> informal (de 1 a 5, onde esta)
   - Escala: serio <-> divertido (de 1 a 5)
   - Escala: tecnico <-> acessivel (de 1 a 5)

3. VOCABULARIO
   - 10 palavras/expressoes que a marca DEVE usar
   - 10 palavras/expressoes que a marca NUNCA deve usar

4. EXEMPLOS PRATICOS
   - Como a marca responderia a um elogio no Instagram
   - Como a marca responderia a uma reclamacao
   - Como a marca faria um post de venda
   - Como a marca faria um post educativo

5. REGRAS DE COMUNICACAO
   - Uso de emojis (sim/nao, quais)
   - Uso de girias (sim/nao, quais)
   - Tratamento (voce, tu, senhor)
   - Hashtags padrao

Formate como um guia que eu possa entregar ao cliente para aprovacao.
```

**Exemplo de resultado esperado:** Guia de 2-3 paginas com personalidade, escalas visuais, vocabulario permitido/proibido e exemplos praticos de comunicacao em diferentes contextos.

---

### 4. Analise de Concorrentes do Cliente

**Quando usar:** No inicio do projeto para entender o cenario competitivo e encontrar oportunidades de diferenciacao.

**Prompt:**
```
Preciso fazer uma analise competitiva rapida para um cliente. Me ajude a estruturar.

INFORMACOES:
- Empresa do cliente: [NOME DA EMPRESA]
- Segmento: [NICHO]
- Cidade/regiao: [LOCAL]
- Concorrentes conhecidos: [LISTA DE 3-5 CONCORRENTES — pode ser Instagram, site ou nome]
- Se nao souber concorrentes, descreva: [O QUE O CLIENTE VENDE E PRA QUEM]

Para cada concorrente, analise:

1. PRESENCA DIGITAL
   - Redes sociais ativas e numero aproximado de seguidores
   - Frequencia de postagem
   - Tipo de conteudo predominante

2. POSICIONAMENTO
   - Como se posiciona (premium, popular, tecnico, acessivel)
   - Proposta de valor principal
   - Tom de comunicacao

3. PONTOS FORTES
   - O que fazem bem (conteudo, design, atendimento, ofertas)

4. PONTOS FRACOS
   - Onde deixam a desejar (gaps que o meu cliente pode explorar)

5. ESTRATEGIA DE ANUNCIOS
   - Se usam anuncios pagos (verificar na Biblioteca de Anuncios da Meta)
   - Tipo de criativo predominante (imagem, video, carrossel)
   - Tipo de oferta (desconto, frete gratis, conteudo gratuito)

Ao final, me entregue:
- QUADRO COMPARATIVO (tabela) com todos os concorrentes
- TOP 3 OPORTUNIDADES que o meu cliente pode explorar
- RECOMENDACAO de posicionamento diferenciado
```

**Exemplo de resultado esperado:** Tabela comparativa entre 3-5 concorrentes com notas em cada criterio, seguida de 3 oportunidades concretas e uma recomendacao de posicionamento.

---

### 5. Mapeamento de Dores e Desejos do Publico

**Quando usar:** Para alimentar copies de anuncios, landing pages e conteudo com linguagem que realmente conecta com o publico.

**Prompt:**
```
Preciso mapear as dores e desejos do publico-alvo de um cliente para usar em copies, anuncios e conteudo. Faca uma analise profunda.

CONTEXTO:
- Empresa: [NOME DA EMPRESA]
- Produto/servico: [PRODUTO OU SERVICO]
- Publico-alvo: [DESCRICAO DO PUBLICO]
- Problema principal que resolve: [PROBLEMA]

Me entregue:

1. DORES (minimo 10)
   Para cada dor, inclua:
   - A dor em uma frase
   - Frase que o publico diria em voz alta sobre essa dor (linguagem real, nao corporativa)
   - Nivel de urgencia (alta/media/baixa)

2. DESEJOS (minimo 10)
   Para cada desejo, inclua:
   - O desejo em uma frase
   - Frase que o publico diria ao amigo sobre esse desejo
   - Tipo (funcional / emocional / social)

3. OBJECOES DE COMPRA (minimo 7)
   Para cada objecao:
   - A objecao
   - Resposta/argumento para quebrar a objecao

4. GATILHOS DE DECISAO
   - O que faz esse publico comprar AGORA (top 5 gatilhos)
   - O que faz esse publico DESISTIR da compra (top 5 barreiras)

5. BANCO DE FRASES PRONTAS
   - 10 headlines baseadas nas dores
   - 10 headlines baseadas nos desejos

Formate de forma que eu consiga copiar e colar as frases diretamente nas copies.
```

**Exemplo de resultado esperado:** Documento com 10 dores detalhadas, 10 desejos, 7 objecoes com respostas, gatilhos de decisao e 20 headlines prontas para uso em anuncios e landing pages.

---

### 6. Criacao de Persona do Cliente Ideal do Cliente

**Quando usar:** Para criar uma persona detalhada que orienta todas as decisoes de comunicacao e campanha.

**Prompt:**
```
Preciso criar uma persona detalhada do cliente ideal para um projeto de marketing. Construa uma persona realista e util.

INFORMACOES:
- Empresa: [NOME DA EMPRESA]
- Produto/servico: [PRODUTO OU SERVICO]
- Faixa de preco: [PRECO]
- Regiao de atuacao: [LOCAL]
- Perfil dos melhores clientes atuais (se houver): [DESCRICAO]

Crie UMA persona completa com:

1. DADOS BASICOS
   - Nome ficticio, idade, profissao, renda mensal, cidade, estado civil

2. ROTINA
   - Como e o dia a dia dessa pessoa (manha, tarde, noite)
   - Onde passa tempo online
   - Que tipo de conteudo consome

3. MOTIVACOES
   - O que essa pessoa quer alcançar profissional e pessoalmente
   - O que a faz levantar da cama de manha
   - Qual o sonho grande

4. FRUSTRACOES
   - O que nao esta funcionando na vida/negocio
   - O que ja tentou e nao deu certo
   - O que a impede de avancar

5. COMPORTAMENTO DE COMPRA
   - Como pesquisa antes de comprar
   - O que a convence (prova social, garantia, autoridade)
   - Onde prefere comprar (online, presencial, WhatsApp)

6. FRASE QUE DEFINE ESSA PERSONA
   - Uma frase que essa pessoa diria ao amigo descrevendo o problema que o produto resolve

7. COMO ALCANÇAR ESSA PERSONA
   - Melhores canais para atingi-la
   - Tipo de conteudo que chama atencao
   - Melhor horario para anuncios
   - Tom de comunicacao ideal

Formato: documento visual com secoes claras, pronto para apresentar ao cliente.
```

**Exemplo de resultado esperado:** Perfil completo de persona com nome, foto descritiva, rotina, motivacoes, frustracoes e guia de como alcanca-la, pronto para compartilhar com a equipe.

---

### 7. Definicao de KPIs e Metas

**Quando usar:** Ao fechar escopo com o cliente, para alinhar expectativas e definir como o sucesso sera medido.

**Prompt:**
```
Preciso definir KPIs e metas realistas para um projeto de marketing digital. Me ajude a montar uma proposta de metricas.

CONTEXTO:
- Empresa: [NOME DA EMPRESA]
- Servico contratado: [TRAFEGO PAGO / SOCIAL MEDIA / DESIGN / COMPLETO]
- Orcamento mensal de midia: R$ [VALOR]
- Objetivo principal: [VENDAS / LEADS / SEGUIDORES / BRANDING]
- Nicho: [NICHO]
- Ja tem historico de dados? [SIM/NAO — se sim, compartilhe metricas anteriores]

Me entregue:

1. KPIs PRIMARIOS (metricas que definem sucesso)
   - Nome do KPI
   - Como e calculado
   - Meta para 30 dias
   - Meta para 90 dias

2. KPIs SECUNDARIOS (metricas de suporte)
   - Nome do KPI
   - Por que importa
   - Faixa saudavel para o nicho

3. METRICAS DE VAIDADE (o que NAO usar como KPI)
   - Lista de metricas que parecem importantes mas nao sao
   - Explicacao de por que nao devem ser foco

4. DASHBOARD PROPOSTO
   - Quais metricas mostrar no relatorio mensal
   - Frequencia de acompanhamento (diario, semanal, mensal)
   - Ferramentas sugeridas para monitorar

5. CRITERIOS DE SUCESSO
   - O que define "deu certo" em 30 dias
   - O que define "precisa ajustar"
   - O que define "estrategia errada, pivotar"

Formate como uma proposta que eu possa enviar ao cliente para aprovacao.
```

**Exemplo de resultado esperado:** Proposta com 3-4 KPIs primarios com metas numericas, KPIs secundarios, lista de metricas de vaidade e criterios claros de sucesso/fracasso.

---

### 8. Escopo de Projeto com Timeline

**Quando usar:** Ao fechar um contrato, para deixar claro o que sera entregue, quando e como.

**Prompt:**
```
Preciso montar um escopo de projeto com timeline detalhada para apresentar ao cliente. Me ajude a estruturar.

INFORMACOES:
- Empresa: [NOME DA EMPRESA]
- Servico: [TRAFEGO PAGO / SOCIAL MEDIA / DESIGN / VIDEO / COMPLETO]
- Duracao do contrato: [MESES]
- Inicio previsto: [DATA]
- Entregas combinadas: [LISTE O QUE FOI COMBINADO]
- Orcamento de midia (se aplicavel): R$ [VALOR]/mes

Me entregue:

1. ESCOPO DETALHADO
   - Lista completa de entregas mensais
   - O que esta INCLUIDO no escopo
   - O que NAO esta incluido (limites claros)
   - Numero de revisoes por entrega

2. TIMELINE — MES 1
   - Semana 1: [Atividades de setup]
   - Semana 2: [Atividades de implementacao]
   - Semana 3: [Atividades de otimizacao]
   - Semana 4: [Atividades de report]

3. TIMELINE — MESES SEGUINTES
   - Rotina mensal padrao (o que acontece cada semana)
   - Marcos importantes (datas de entrega, reviews)

4. PROCESSO DE TRABALHO
   - Como o cliente envia demandas
   - Prazo de resposta
   - Prazo de entrega por tipo de peca
   - Como funciona a aprovacao

5. CRONOGRAMA VISUAL
   - Tabela com semanas x entregas
   - Marcos destacados

Formate como um documento profissional que eu possa anexar ao contrato.
```

**Exemplo de resultado esperado:** Documento de 2 paginas com escopo claro, timeline semana a semana do primeiro mes, rotina dos meses seguintes e tabela visual de cronograma.

---

### 9. Diagnostico Rapido da Operacao do Cliente

**Quando usar:** Quando pegar um cliente que ja tem marketing rodando e voce precisa entender o que esta funcionando e o que nao esta.

**Prompt:**
```
Preciso fazer um diagnostico rapido da operacao de marketing digital de um cliente. Me ajude a estruturar a analise.

INFORMACOES DISPONIVEIS:
- Empresa: [NOME DA EMPRESA]
- Nicho: [NICHO]
- Instagram: [@PERFIL]
- Site: [URL]
- Roda anuncios? [SIM/NAO]
- Ferramentas que usa: [LISTA — ex: RD Station, Hotmart, WhatsApp Business]
- Faturamento mensal aproximado: R$ [VALOR]
- Principal queixa do cliente: [O QUE ELE RECLAMA]

Faca o diagnostico nas seguintes areas:

1. PRESENCA DIGITAL (nota de 1 a 10)
   - Qualidade do perfil Instagram (bio, destaques, feed)
   - Qualidade do site (velocidade, design, conversao)
   - Presenca em outras plataformas

2. CONTEUDO (nota de 1 a 10)
   - Frequencia de postagem
   - Qualidade visual
   - Variedade de formatos
   - Engajamento medio

3. TRAFEGO PAGO (nota de 1 a 10)
   - Estrutura de campanhas
   - Qualidade dos criativos
   - Segmentacao
   - CPA/CPL estimado

4. FUNIL DE VENDAS (nota de 1 a 10)
   - Caminho do lead ate a venda
   - Follow-up pos-lead
   - Automacoes existentes

5. PONTOS CRITICOS
   - Top 3 problemas mais urgentes
   - Top 3 oportunidades rapidas (quick wins)

6. PLANO DE ACAO (primeiros 30 dias)
   - Semana 1-2: correcoes urgentes
   - Semana 3-4: implementacoes estrategicas

Formate como um relatorio de diagnostico profissional que impressione o cliente.
```

**Exemplo de resultado esperado:** Relatorio com notas por area, lista de problemas criticos, quick wins e plano de acao para os primeiros 30 dias.

---

### 10. Extrator de Identidade Visual

**Quando usar:** Quando o cliente nao tem manual de marca e voce precisa documentar a identidade visual para manter consistencia.

**Prompt:**
```
Preciso documentar a identidade visual de um cliente que nao tem manual de marca. Me ajude a extrair e organizar essas informacoes.

INFORMACOES DISPONIVEIS:
- Empresa: [NOME DA EMPRESA]
- Site: [URL]
- Instagram: [@PERFIL]
- Logotipo: [DESCREVA OU ENVIE]
- O cliente tem preferencias de cores? [SIM/NAO — se sim, quais]
- Referencia visual que o cliente gosta: [MARCAS OU PERFIS DE REFERENCIA]

Me entregue um MINI MANUAL DE IDENTIDADE VISUAL com:

1. PALETA DE CORES
   - Cor primaria (hex, RGB)
   - Cor secundaria (hex, RGB)
   - Cor de apoio (hex, RGB)
   - Cor de fundo (hex, RGB)
   - Cor de texto (hex, RGB)
   - Onde usar cada cor

2. TIPOGRAFIA
   - Fonte para titulos (sugestao gratuita compativel com a marca)
   - Fonte para textos (sugestao gratuita compativel)
   - Tamanhos recomendados para cada uso

3. ESTILO VISUAL
   - Tipo de fotografia (lifestyle, produto, minimalista, vibrante)
   - Filtros ou tratamento de imagem
   - Elementos graficos (icones, formas, patterns)
   - Estilo de ilustracao (se aplicavel)

4. APLICACOES
   - Como aplicar nos posts do Instagram (feed + stories)
   - Como aplicar em anuncios
   - Como aplicar em documentos/propostas
   - Como aplicar no site

5. O QUE EVITAR
   - Combinacoes de cores proibidas
   - Fontes que nao combinam com a marca
   - Estilos visuais que fogem do posicionamento

Formate como um guia visual rapido (mesmo em texto) que qualquer designer consiga seguir.
```

**Exemplo de resultado esperado:** Guia com paleta de cores em hex, sugestoes de fontes gratuitas, estilo visual definido e regras de aplicacao para diferentes materiais.

---

> Total: 10 prompts de Briefing prontos para uso.
