# Categoria 3: Revisao

> Prompts para revisar e melhorar outputs antes de entregar ao cliente.

---

### 1. Revisor de Copy (Ortografia + Tom + CTA)

**Quando usar:** Antes de entregar qualquer texto ao cliente ou publicar conteudo.

**Prompt:**
```
Voce e um revisor de copy profissional com experiencia em marketing digital. Revise o texto abaixo com rigor.

TEXTO PARA REVISAO:
"""
[COLE O TEXTO AQUI]
"""

CONTEXTO:
- Empresa: [NOME DA EMPRESA]
- Tipo de peca: [ANUNCIO / POST / EMAIL / LP / WHATSAPP]
- Tom de voz da marca: [FORMAL / INFORMAL / TECNICO / DESCONTRAIDO]
- Publico-alvo: [DESCRICAO]
- Objetivo do texto: [VENDER / EDUCAR / ENGAJAR / CONVERTER]

Faca a revisao nos seguintes niveis:

1. ORTOGRAFIA E GRAMATICA
   - Erros de portugues
   - Concordancia verbal e nominal
   - Pontuacao
   - Acentuacao

2. CLAREZA E FLUIDEZ
   - Frases confusas ou longas demais
   - Repeticoes desnecessarias
   - Palavras que podem ser simplificadas
   - Ordem das informacoes

3. TOM DE VOZ
   - O texto esta no tom correto para a marca?
   - Alguma frase soa fora do personagem?
   - Sugestoes de ajuste de tom

4. PERSUASAO E CTA
   - O argumento de venda e convincente?
   - O CTA e claro e direto?
   - Falta algum gatilho mental?
   - A copy conduz para a acao desejada?

5. FORMATO
   - O texto esta no tamanho ideal para a peca?
   - A formatacao esta adequada para a plataforma?

Me entregue:
- TEXTO ORIGINAL com marcacoes do que precisa mudar
- TEXTO REVISADO (versao final limpa)
- LISTA DE ALTERACOES com justificativa para cada uma
- NOTA GERAL de 1 a 10
```

**Exemplo de resultado esperado:** Texto revisado com lista de alteracoes justificadas, versao limpa pronta para uso e nota geral de qualidade.

---

### 2. Verificador de Consistencia de Marca

**Quando usar:** Ao revisar um lote de pecas para garantir que tudo esta alinhado com a identidade da marca.

**Prompt:**
```
Preciso verificar se um conjunto de pecas esta consistente com a identidade da marca. Faca uma auditoria rapida.

DIRETRIZES DA MARCA:
- Tom de voz: [FORMAL / INFORMAL / TECNICO / DESCONTRAIDO]
- Palavras que a marca USA: [LISTA]
- Palavras que a marca NUNCA usa: [LISTA]
- Cores: [LISTA DE CORES]
- Posicionamento: [COMO A MARCA SE POSICIONA]

PECAS PARA VERIFICAR:
"""
PECA 1 — [TIPO: post, anuncio, email, etc.]
[COLE O TEXTO]

PECA 2 — [TIPO]
[COLE O TEXTO]

PECA 3 — [TIPO]
[COLE O TEXTO]
"""

Para cada peca, verifique:

1. TOM DE VOZ
   - Esta dentro do tom definido? [SIM/NAO]
   - Trechos que desviam do tom

2. VOCABULARIO
   - Usa palavras aprovadas? [SIM/NAO]
   - Usa palavras proibidas? [SIM/NAO — quais]

3. MENSAGEM
   - A mensagem esta alinhada com o posicionamento? [SIM/NAO]
   - Contradiz algo que a marca defende? [SIM/NAO]

4. CONSISTENCIA ENTRE PECAS
   - As pecas conversam entre si? [SIM/NAO]
   - Ha contradicoes entre elas? [SIM/NAO — quais]

5. NOTA DE CONSISTENCIA (1 a 10)

Me entregue:
- Tabela resumo (peca x criterio x nota)
- Lista de ajustes necessarios por peca
- Versao corrigida de cada peca (se necessario)
```

**Exemplo de resultado esperado:** Tabela de auditoria com notas por peca, lista de inconsistencias encontradas e versoes corrigidas.

---

### 3. Revisor de Relatorio (Dados + Analise + Recomendacoes)

**Quando usar:** Antes de enviar qualquer relatorio de performance ao cliente.

**Prompt:**
```
Preciso que voce revise um relatorio de marketing digital antes de eu enviar ao cliente. Verifique dados, analise e recomendacoes.

RELATORIO PARA REVISAO:
"""
[COLE O RELATORIO AQUI]
"""

CONTEXTO:
- Periodo do relatorio: [MES/PERIODO]
- Tipo: [TRAFEGO / SOCIAL MEDIA / COMPLETO]
- KPIs combinados com o cliente: [LISTA]
- Orcamento investido: R$ [VALOR]

Revise nos seguintes aspectos:

1. DADOS E NUMEROS
   - Os numeros fazem sentido matematicamente? (somas, percentuais, comparacoes)
   - Ha dados contraditórios?
   - Faltam metricas importantes?
   - As comparacoes mes a mes estao corretas?

2. ANALISE
   - A analise explica o POR QUE dos resultados?
   - Falta contexto para algum dado?
   - A narrativa e clara para alguem nao tecnico?
   - Tem jargao tecnico sem explicacao?

3. RECOMENDACOES
   - As recomendacoes sao especificas e acionaveis?
   - Sao coerentes com os dados apresentados?
   - Tem prazo ou prioridade definidos?
   - O cliente consegue entender o que vai mudar?

4. APRESENTACAO
   - A estrutura esta logica? (resumo > dados > analise > recomendacoes)
   - O texto esta claro e objetivo?
   - Tem muita informacao desnecessaria?
   - O tom e profissional e confiante?

5. VERIFICACAO FINAL
   - Nome do cliente esta correto?
   - Periodo esta correto?
   - Logo/marca esta presente?
   - Tem erros de portugues?

Me entregue:
- Lista de problemas encontrados (organizados por gravidade)
- Versao revisada do relatorio
- Sugestoes de melhoria na apresentacao
```

**Exemplo de resultado esperado:** Lista de erros/inconsistencias por gravidade, relatorio corrigido e sugestoes de como melhorar a apresentacao.

---

### 4. Verificador de Briefing (Campos Faltando)

**Quando usar:** Depois de receber o briefing preenchido pelo cliente, para verificar se tem tudo que voce precisa.

**Prompt:**
```
Recebi um briefing de um cliente e preciso verificar se tem todas as informacoes necessarias para comecar o trabalho.

SERVICO CONTRATADO: [TRAFEGO PAGO / SOCIAL MEDIA / DESIGN / VIDEO / COMPLETO]

BRIEFING RECEBIDO:
"""
[COLE O BRIEFING DO CLIENTE AQUI]
"""

Verifique se o briefing contem TODAS as informacoes essenciais:

CHECKLIST OBRIGATORIO:
- [ ] Objetivo claro e mensuravel
- [ ] Descricao do publico-alvo
- [ ] Produto/servico que sera divulgado
- [ ] Diferencial competitivo
- [ ] Orcamento definido
- [ ] Prazo/timeline
- [ ] Tom de voz ou referencias
- [ ] Materiais existentes (logo, fotos, videos)
- [ ] Acessos necessarios (redes, plataformas, analytics)
- [ ] KPIs e como medir sucesso
- [ ] Concorrentes conhecidos
- [ ] Historico de acoes anteriores
- [ ] Restricoes ou limitacoes
- [ ] Contato do responsavel por aprovacoes

Me entregue:

1. CHECKLIST PREENCHIDO (marcando o que tem e o que falta)
2. CAMPOS FALTANTES — lista do que preciso pedir ao cliente
3. MENSAGEM PRONTA para enviar ao cliente pedindo as informacoes faltantes (tom profissional e direto)
4. CAMPOS AMBIGUOS — informacoes que estao no briefing mas nao estao claras o suficiente
5. NOTA DO BRIEFING (1 a 10) com justificativa
```

**Exemplo de resultado esperado:** Checklist marcado, lista de campos faltantes, mensagem pronta para enviar ao cliente e nota do briefing.

---

### 5. Revisor de Proposta Comercial

**Quando usar:** Antes de enviar uma proposta de servico para um potencial cliente.

**Prompt:**
```
Preciso que voce revise minha proposta comercial antes de enviar ao cliente. Verifique conteudo, persuasao e profissionalismo.

PROPOSTA PARA REVISAO:
"""
[COLE A PROPOSTA AQUI]
"""

CONTEXTO:
- Cliente potencial: [NOME DA EMPRESA]
- Servico oferecido: [TIPO DE SERVICO]
- Valor proposto: R$ [VALOR]/mes
- Concorrencia: [SABE SE O CLIENTE ESTA COTANDO COM OUTROS? SIM/NAO]

Revise nos seguintes aspectos:

1. ESTRUTURA
   - A proposta segue uma logica persuasiva? (problema > solucao > prova > oferta > CTA)
   - Tem todas as secoes essenciais?
   - A ordem das informacoes faz sentido?

2. CONTEUDO
   - Os servicos estao descritos de forma clara?
   - O escopo esta bem definido (o que inclui E o que nao inclui)?
   - Os prazos estao realistas?
   - Os resultados prometidos sao alcancaveis?

3. PERSUASAO
   - Tem prova social (cases, numeros, depoimentos)?
   - Os diferenciais estao claros?
   - A proposta justifica o valor cobrado?
   - O CTA e claro (o que o cliente precisa fazer para fechar)?

4. OBJECOES
   - A proposta antecipa e responde possiveis objecoes?
   - Tem garantia ou reducao de risco?
   - O cliente pode ter duvidas nao respondidas?

5. PROFISSIONALISMO
   - Formatacao esta limpa e profissional?
   - Erros de portugues?
   - Tom esta adequado para o perfil do cliente?
   - Informacoes de contato estao presentes?

Me entregue:
- Lista de melhorias organizadas por prioridade (critico / importante / nice to have)
- Proposta revisada (versao final)
- 3 sugestoes para aumentar a taxa de fechamento
```

**Exemplo de resultado esperado:** Lista de melhorias priorizadas, proposta revisada e dicas para aumentar conversao.

---

### 6. Verificador de SEO em Textos

**Quando usar:** Ao revisar textos para blog, site ou landing page do cliente que precisam de otimizacao para busca.

**Prompt:**
```
Preciso verificar a otimizacao SEO de um texto antes de publicar. Faca uma analise completa.

TEXTO PARA ANALISE:
"""
[COLE O TEXTO AQUI]
"""

INFORMACOES:
- Palavra-chave principal: [KEYWORD]
- Palavras-chave secundarias: [LISTA]
- Tipo de pagina: [BLOG / PAGINA DE SERVICO / LP / CATEGORIA]
- URL planejada: [URL]
- Publico-alvo: [DESCRICAO]

Verifique:

1. TITULO (Title Tag)
   - Contem a keyword principal?
   - Tem entre 50-60 caracteres?
   - E atrativo para clique?
   - Sugestao de titulo otimizado

2. META DESCRIPTION
   - Existe? Esta otimizada?
   - Tem entre 150-160 caracteres?
   - Contem keyword e CTA?
   - Sugestao de meta description

3. HEADINGS (H1, H2, H3)
   - H1 contem a keyword?
   - Hierarquia de headings esta correta?
   - H2s cobrem subtopicos relevantes?

4. CONTEUDO
   - Densidade da keyword (ideal: 1-2%)
   - Keywords secundarias estao distribuidas?
   - Texto tem tamanho adequado para o tipo de pagina?
   - Paragrafos estao curtos e escaneáveis?
   - Tem listas, bullets ou tabelas?

5. LINKS
   - Tem links internos para outras paginas do site?
   - Tem links externos para fontes confiaveis?
   - Textos ancora estao otimizados?

6. LEGIBILIDADE
   - Nivel de leitura adequado para o publico?
   - Frases curtas? Palavras simples?
   - Formatacao facilita leitura no mobile?

Me entregue:
- Score SEO estimado (1-100)
- Lista de otimizacoes obrigatorias
- Texto revisado com as otimizacoes aplicadas
- Sugestoes de titulo, meta description e headings
```

**Exemplo de resultado esperado:** Score SEO, lista de otimizacoes com prioridade e texto revisado com melhorias aplicadas.

---

### 7. Revisor de Apresentacao/Slides

**Quando usar:** Antes de entregar uma apresentacao ao cliente ou antes do cliente apresentar em uma reuniao.

**Prompt:**
```
Preciso revisar o conteudo de uma apresentacao/deck antes da entrega. Analise slide por slide.

CONTEUDO DOS SLIDES:
"""
SLIDE 1:
[TEXTO DO SLIDE]

SLIDE 2:
[TEXTO DO SLIDE]

(continue para todos os slides)
"""

CONTEXTO:
- Objetivo da apresentacao: [VENDA / RELATORIO / PITCH / TREINAMENTO]
- Audiencia: [QUEM VAI VER]
- Duracao planejada: [MINUTOS]
- Quem apresenta: [NOME — dono, vendedor, etc.]

Revise cada slide nos seguintes aspectos:

1. CONTEUDO
   - Informacao relevante e necessaria?
   - Texto excessivo? (regra: max 6 linhas por slide)
   - Dados estao corretos e atualizados?
   - Falta alguma informacao critica?

2. NARRATIVA
   - Os slides contam uma historia logica?
   - A sequencia faz sentido?
   - Ha transicoes suaves entre temas?
   - O final e forte (CTA claro)?

3. DESIGN (baseado no texto)
   - Sugestoes de layout para cada slide
   - Onde usar graficos em vez de texto
   - Onde usar imagens para reforcar a mensagem

4. APRESENTACAO ORAL
   - Notas do apresentador para cada slide (o que falar)
   - Quanto tempo gastar em cada slide
   - Momentos de pausar para perguntas

Me entregue:
- Feedback slide por slide
- Versao revisada dos textos
- Sugestao de slides adicionais ou para remover
- Script do apresentador (notas para cada slide)
```

**Exemplo de resultado esperado:** Revisao slide por slide com sugestoes de melhoria, textos revisados e script do apresentador.

---

### 8. Verificador de Acessibilidade de Conteudo

**Quando usar:** Ao publicar conteudo que precisa ser acessivel para o maior numero de pessoas possivel.

**Prompt:**
```
Preciso verificar a acessibilidade do conteudo que estou produzindo para o cliente. Analise e sugira melhorias.

CONTEUDO PARA ANALISE:
"""
[COLE O CONTEUDO — pode ser texto de site, post, email ou descricao de video]
"""

TIPO DE CONTEUDO: [SITE / POST / EMAIL / VIDEO / CARROSSEL]
PLATAFORMA: [INSTAGRAM / SITE / LINKEDIN / EMAIL / YOUTUBE]

Verifique:

1. TEXTO
   - Linguagem e simples e clara? (leitura nivel ensino medio)
   - Frases estao curtas? (max 20 palavras ideal)
   - Tem jargao tecnico sem explicacao?
   - Tem siglas sem explicar na primeira vez?

2. VISUAL (baseado na descricao)
   - Contraste de cores e suficiente?
   - Textos sobre imagem sao legiveis?
   - Tamanho de fonte esta adequado?
   - Informacao nao depende apenas de cor?

3. MIDIAS
   - Videos precisam de legenda? [SIM — sempre]
   - Imagens precisam de texto alternativo?
   - Audio precisa de transcricao?

4. ESTRUTURA
   - Headings estao em ordem logica?
   - Listas sao usadas em vez de paragrafos longos?
   - Links sao descritivos? (nao "clique aqui")
   - Formularios tem labels claros?

5. INCLUSAO
   - Linguagem e inclusiva?
   - Representatividade nas imagens?
   - Conteudo funciona em modo escuro?

Me entregue:
- Checklist de acessibilidade (marcado)
- Lista de melhorias necessarias por prioridade
- Versao revisada do texto com melhorias aplicadas
- Sugestoes de texto alternativo para imagens
```

**Exemplo de resultado esperado:** Checklist de acessibilidade, lista de melhorias e texto revisado com linguagem mais clara e acessivel.

---

### 9. Revisor de Email Profissional

**Quando usar:** Antes de enviar emails importantes para clientes, parceiros ou fornecedores.

**Prompt:**
```
Preciso revisar um email profissional antes de enviar. Verifique tom, clareza e efetividade.

EMAIL PARA REVISAO:
"""
PARA: [DESTINATARIO]
ASSUNTO: [ASSUNTO]
CORPO:
[COLE O EMAIL AQUI]
"""

CONTEXTO:
- Relacao com o destinatario: [CLIENTE / LEAD / PARCEIRO / FORNECEDOR]
- Objetivo do email: [INFORMAR / PEDIR / VENDER / COBRAR / AGENDAR]
- Nivel de formalidade esperado: [FORMAL / SEMIFORMAL / INFORMAL]
- Urgencia: [ALTA / MEDIA / BAIXA]

Revise:

1. ASSUNTO
   - E claro e especifico?
   - Gera vontade de abrir?
   - Tem tamanho adequado (max 50 caracteres)?
   - Sugestao de assunto alternativo

2. ABERTURA
   - Saudacao adequada ao contexto?
   - Primeira frase vai direto ao ponto?
   - Contextualizacao e suficiente?

3. CORPO
   - Mensagem e clara em uma leitura?
   - Paragrafos estao curtos (max 3 linhas)?
   - Informacoes estao na ordem logica?
   - Tem informacao desnecessaria?

4. CTA
   - Fica claro o que o destinatario precisa fazer?
   - Tem prazo definido (se aplicavel)?
   - O pedido e facil de cumprir?

5. FECHAMENTO
   - Despedida adequada?
   - Assinatura profissional?
   - Informacoes de contato presentes?

6. TOM
   - Nivel de formalidade esta correto?
   - Nenhuma frase soa passivo-agressiva?
   - Nenhuma frase soa insegura ou apologetica demais?

Me entregue:
- Lista de ajustes com justificativa
- Email revisado (versao final)
- Assunto alternativo
```

**Exemplo de resultado esperado:** Email revisado com tom adequado, estrutura otimizada e assunto alternativo.

---

### 10. Quality Check de Entregaveis

**Quando usar:** Antes de enviar qualquer lote de entregas ao cliente, para garantir que tudo esta no padrao.

**Prompt:**
```
Preciso fazer um quality check completo antes de entregar um lote de trabalho ao cliente. Me ajude a verificar tudo.

TIPO DE ENTREGA: [POSTS / ANUNCIOS / RELATORIO / LANDING PAGE / EMAILS / VIDEOS / MISTO]

LISTA DE ENTREGAVEIS:
"""
[LISTE TUDO QUE SERA ENTREGUE — ex:
- 12 posts para Instagram (feed)
- 5 copies de anuncio
- 1 relatorio mensal
- 3 roteiros de Reels]
"""

PADROES DO CLIENTE:
- Tom de voz: [TOM]
- Cores: [CORES]
- Restricoes: [LISTA]
- KPIs combinados: [LISTA]

Faca o quality check em cada item:

1. COMPLETUDE
   - Todos os itens da lista estao prontos?
   - Falta algum item combinado?
   - Tem itens extras nao solicitados?

2. QUALIDADE INDIVIDUAL
   Para cada tipo de entregavel, verifique o padrao minimo:
   - Posts: copy + arte descrita + hashtags + horario
   - Anuncios: headline + copy + CTA + segmentacao
   - Relatorio: dados + analise + recomendacoes
   - Roteiros: gancho + desenvolvimento + CTA + instrucoes
   - Emails: assunto + corpo + CTA + timing

3. CONSISTENCIA
   - Tom de voz uniforme em todas as pecas?
   - Mensagem alinhada entre pecas?
   - Visual coerente (se aplicavel)?

4. ERROS COMUNS
   - Ortografia e gramatica
   - Nome do cliente correto
   - Datas corretas
   - Links funcionando
   - Numeros/dados verificados

5. CHECKLIST FINAL
   - [ ] Todos os itens entregues
   - [ ] Todos revisados individualmente
   - [ ] Consistencia entre pecas
   - [ ] Sem erros de portugues
   - [ ] Nome/marca corretos
   - [ ] Formato de entrega adequado
   - [ ] Prazos cumpridos

Me entregue:
- Checklist preenchido
- Lista de ajustes necessarios antes de enviar
- Nota de qualidade geral (1 a 10)
- Mensagem de entrega para o cliente (texto pro WhatsApp/email)
```

**Exemplo de resultado esperado:** Checklist completo, lista de ajustes por prioridade, nota de qualidade e mensagem de entrega pronta.

---

> Total: 10 prompts de Revisao prontos para uso.
