# Prompts: Processo de Vendas B2B

## Como usar
Copie o prompt, substitua as variaveis entre colchetes e cole na IA. Cada prompt cobre uma etapa do processo de vendas: da discovery ao fechamento.

---

## Prompt 1: Preparar Reuniao de Discovery

```
Atue como um closer B2B que fecha contratos de [TICKET_MEDIO].

Vou ter uma reuniao de discovery com:
- Lead: [NOME] -- [CARGO]
- Empresa: [NOME_EMPRESA]
- Segmento: [SEGMENTO]
- Tamanho: [FUNCIONARIOS] funcionarios, faturamento estimado [FATURAMENTO]
- Como chegou: [ORIGEM_LEAD]
- O que sabemos da dor: [INFORMACOES_PREVIAS]

Meu produto/servico: [O QUE VOCE VENDE]
Resultado principal que entrego: [RESULTADO]
Duracao da reuniao: [DURACAO] minutos

Monte pra mim:
1. ROTEIRO DA REUNIAO com tempo estimado por bloco
2. 10 PERGUNTAS DE DISCOVERY ordenadas do geral ao especifico
   - 3 sobre situacao atual
   - 3 sobre dores e impacto
   - 2 sobre processo de decisao
   - 2 sobre urgencia e timing
3. SINAIS DE COMPRA para prestar atencao durante a conversa
4. 3 FORMAS DE TRANSICAO da discovery para a apresentacao da solucao
5. CHECKLIST POS-REUNIAO do que registrar no CRM
```

---

## Prompt 2: Criar Proposta Comercial Personalizada

```
Atue como um consultor de vendas B2B que escreve propostas que
convertem acima de 30%.

Com base nas informacoes da reuniao de discovery:

CLIENTE:
- Empresa: [NOME_EMPRESA]
- Decisor: [NOME] -- [CARGO]
- Segmento: [SEGMENTO]

DORES MAPEADAS:
1. [DOR_1] -- Impacto estimado: R$ [VALOR_1]/mes
2. [DOR_2] -- Impacto estimado: R$ [VALOR_2]/mes
3. [DOR_3] -- Impacto estimado: R$ [VALOR_3]/mes

SOLUCAO QUE VAMOS PROPOR:
- [DESCRICAO_DA_SOLUCAO]

INVESTIMENTO:
- Opcao 1: R$ [VALOR_1]/mes (pacote [NOME_PACOTE_1])
- Opcao 2: R$ [VALOR_2]/mes (pacote [NOME_PACOTE_2]) -- recomendado
- Prazo de implementacao: [PRAZO]

CASES DE REFERENCIA:
- [CASE_1]: [RESULTADO_1]
- [CASE_2]: [RESULTADO_2]

Crie a proposta comercial completa com:
1. Resumo executivo (3-4 paragrafos)
2. Diagnostico (espelhando as dores na linguagem do cliente)
3. Solucao proposta com entregas detalhadas
4. ROI projetado com calculo explicito
5. Timeline de implementacao
6. Investimento com 2 opcoes (ancoragem)
7. Cases de prova social
8. Proximos passos com data
9. FAQs antecipando objecoes

Tom: profissional, direto, focado em resultado. Sem enrolacao.
```

---

## Prompt 3: Contornar Objecoes Especificas

```
Atue como um especialista em negociacao B2B.

Estou em uma negociacao com:
- Empresa: [NOME_EMPRESA]
- Valor da proposta: R$ [VALOR]/mes
- Estagio: [ESTAGIO -- pos-proposta, negociacao final, etc.]

A objecao que recebi foi:
"[OBJECAO_EXATA_DO_LEAD]"

Contexto adicional:
- Dor principal do lead: [DOR]
- Resultado que prometi: [RESULTADO]
- Concorrente que ele mencionou: [CONCORRENTE ou "nenhum"]
- Decisor tem autonomia? [SIM/NAO -- precisa de comite]

Me de:
1. ANALISE DA OBJECAO
   - E uma objecao real ou uma desculpa?
   - O que esta por tras dessa objecao?

2. 3 RESPOSTAS DIFERENTES
   - Resposta direta (quando o lead e pragmatico)
   - Resposta com pergunta (quando precisa de mais informacao)
   - Resposta com reframe (quando precisa mudar a perspectiva)

3. FOLLOW-UP POS-OBJECAO
   - Email ou mensagem para enviar depois da conversa
   - Reforco do valor sem ser insistente

4. PLANO B
   - Se a objecao for intransponivel, qual a melhor saida?
   - Como manter a porta aberta pra futuro?
```

---

## Prompt 4: Criar Apresentacao de Vendas (Deck Consultivo)

```
Atue como um estrategista de vendas B2B que monta decks que vendem.

Preciso de um roteiro de apresentacao consultiva (NAO e pitch deck
de startup -- e apresentacao de vendas pra fechar contrato).

CONTEXTO:
- Minha empresa: [NOME_DA_SUA_EMPRESA]
- O que vendemos: [PRODUTO/SERVICO]
- Pra quem: [ICP]
- Ticket medio: R$ [VALOR]
- Diferencial principal: [DIFERENCIAL]
- Case mais forte: [CASE] -- [RESULTADO]

O LEAD:
- Empresa: [NOME_EMPRESA]
- Dores identificadas na discovery: [DOR_1], [DOR_2], [DOR_3]
- O que ele ja tentou: [SOLUCOES_ANTERIORES]

Crie o roteiro slide a slide:

SLIDE 1: Capa (titulo que fale de resultado, nao do produto)
SLIDE 2: Agenda da reuniao
SLIDE 3: "O que ouvimos de voces" (espelho das dores)
SLIDE 4: O custo de nao resolver (impacto financeiro)
SLIDE 5: Como resolvemos [DOR_1]
SLIDE 6: Como resolvemos [DOR_2]
SLIDE 7: Como resolvemos [DOR_3]
SLIDE 8: Case de resultado (antes/depois com numeros)
SLIDE 9: Processo / timeline de implementacao
SLIDE 10: Investimento (2 opcoes)
SLIDE 11: Proximos passos
SLIDE 12: Perguntas

Para cada slide, inclua:
- Titulo do slide
- Bullet points do conteudo
- Nota do apresentador (o que FALAR, nao o que MOSTRAR)
- Tempo estimado
```

---

## Prompt 5: Criar Email de Follow-up Pos-Proposta

```
Atue como um closer B2B que transforma "vou pensar" em "fechado".

Situacao:
- Enviei proposta para [NOME] da [NOME_EMPRESA] ha [DIAS] dias
- Valor: R$ [VALOR]/mes
- O lead [DESCRICAO_REACAO -- "disse que ia analisar", "pediu pra
  falar com o socio", "nao respondeu", etc.]
- Prazo de validade da proposta: [DATA_VALIDADE]

Crie uma sequencia de 4 follow-ups:

FOLLOW-UP 1 (D+2 apos proposta)
- Objetivo: Confirmar recebimento e tirar duvidas
- Tom: prestativo, nao vendedor
- Maximo 80 palavras

FOLLOW-UP 2 (D+5)
- Objetivo: Agregar valor com dado novo (case, insight, benchmark)
- Tom: consultivo
- Maximo 100 palavras

FOLLOW-UP 3 (D+10)
- Objetivo: Criar urgencia suave (vagas, prazo, condicao)
- Tom: direto
- Maximo 80 palavras

FOLLOW-UP 4 (D+15 -- break-up)
- Objetivo: Ultima tentativa, deixar porta aberta
- Tom: respeitoso, sem pressao
- Maximo 60 palavras

Para cada follow-up:
- Assunto do email
- Corpo completo
- CTA especifico
- Horario ideal de envio
```
