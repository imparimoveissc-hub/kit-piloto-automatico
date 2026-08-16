# Prompts: Atendimento e Comunicacao com Cliente

## Instrucao de Uso

Estes prompts ajudam a criar comunicacoes profissionais com clientes. O objetivo e economizar tempo na redacao de e-mails, mensagens e relatorios, mantendo o padrao de qualidade do escritorio.

Adapte o tom conforme o perfil do cliente: mais tecnico para empresarios e gestores, mais acessivel para pessoas fisicas.

---

## Prompt 1: E-mail de Primeiro Contato Apos Consulta

**Quando usar:** Apos a consulta inicial, para formalizar o que foi discutido e os proximos passos.

**Prompt:**

```
Redija um e-mail profissional de primeiro contato apos consulta juridica com as seguintes informacoes:

NOME DO CLIENTE: [NOME]
TIPO DE DEMANDA: [Ex: Acao trabalhista / Revisao contratual / Defesa em processo civel]
RESUMO DO QUE FOI DISCUTIDO NA CONSULTA: [2-3 pontos principais]
PROXIMOS PASSOS ACORDADOS: [Ex: Cliente enviara documentos / Escritorio fara analise / Proposta de honorarios sera enviada]
PRAZO PARA PROXIMA INTERACAO: [Ex: 5 dias uteis]
NOME DO ADVOGADO: [NOME]
NOME DO ESCRITORIO: [NOME]

Tom: Profissional, acolhedor, transmitindo seguranca. O cliente acabou de conhecer o escritorio e precisa sentir que esta em boas maos.

Instrucoes:
- Agradecer a confianca
- Resumir o que foi conversado (sem detalhes confidenciais excessivos por e-mail)
- Listar proximos passos de forma clara
- Informar prazo e canal de contato
- Nao usar juridiques -- linguagem clara
- Maximo 200 palavras
```

**Resultado esperado:** E-mail profissional e acolhedor, pronto para envio apos personalizacao.

---

## Prompt 2: Explicacao de Decisao Judicial em Linguagem Simples

**Quando usar:** Quando precisar explicar ao cliente uma decisao do juiz de forma compreensivel.

**Prompt:**

```
Traduza a seguinte decisao judicial para linguagem simples, como se estivesse explicando para um cliente leigo:

TIPO DE DECISAO: [Sentenca / Despacho / Decisao interlocutoria / Acordao]
TEXTO DA DECISAO (ou resumo):
[COLAR O TRECHO RELEVANTE DA DECISAO]

RESULTADO: [FAVORAVEL / DESFAVORAVEL / PARCIALMENTE FAVORAVEL ao nosso cliente]

Gere:
1. RESUMO EM 1 FRASE: O que o juiz decidiu, em linguagem do dia a dia
2. EXPLICACAO DETALHADA: O que cada ponto da decisao significa na pratica (3-5 pontos)
3. IMPACTO PARA O CLIENTE: O que muda concretamente na vida/no caso do cliente
4. PROXIMOS PASSOS: O que acontece agora e o que o cliente precisa fazer (se algo)
5. PRAZO (se houver): Algum prazo que o cliente precisa estar ciente

Regras:
- Zero juridiques. Se usar um termo tecnico, explique entre parenteses
- Tom calmo e objetivo, mesmo se a decisao for desfavoravel
- Nao minimizar decisao desfavoravel, mas contextualizar (mostrar que ha opcoes)
- Maximo 300 palavras
```

**Resultado esperado:** Explicacao clara que o advogado pode enviar ao cliente ou usar como base para uma ligacao.

---

## Prompt 3: Respostas para Perguntas Frequentes de Clientes

**Quando usar:** Para preparar respostas padronizadas as duvidas mais comuns.

**Prompt:**

```
Crie respostas profissionais e acessiveis para as seguintes perguntas frequentes de clientes de um escritorio de advocacia:

AREA DE ATUACAO DO ESCRITORIO: [Ex: Trabalhista / Civel / Familia / Empresarial]

PERGUNTAS:
1. [Ex: Quanto tempo demora meu processo?]
2. [Ex: Qual a chance de ganhar?]
3. [Ex: Por que o processo esta demorando tanto?]
4. [Ex: Posso ligar para voce a qualquer hora?]
5. [Ex: Quanto vou gastar com custas?]

Para cada pergunta, gere:
- RESPOSTA CURTA (para WhatsApp, maximo 3 linhas)
- RESPOSTA COMPLETA (para e-mail, maximo 100 palavras)

Regras:
- Tom profissional mas humano
- Ser honesto sem ser pessimista
- Nunca prometer resultados
- Gerenciar expectativas de forma transparente
- Deixar claro que cada caso e unico quando relevante
```

**Resultado esperado:** Banco de respostas padronizadas para as duvidas mais comuns, economizando tempo no atendimento.

---

## Prompt 4: Relatorio Simplificado de Andamento

**Quando usar:** Para gerar um resumo rapido do caso que possa ser compartilhado com o cliente.

**Prompt:**

```
Gere um relatorio simplificado de andamento processual para enviar ao cliente:

NOME DO CLIENTE: [NOME]
NUMERO DO PROCESSO: [NUMERO]
TIPO DE ACAO: [TIPO]

ULTIMAS MOVIMENTACOES (da mais recente para a mais antiga):
1. [DATA] - [MOVIMENTACAO PROCESSUAL TECNICA]
2. [DATA] - [MOVIMENTACAO]
3. [DATA] - [MOVIMENTACAO]

SITUACAO ATUAL:
[DESCREVER EM LINGUAGEM TECNICA O QUE ESTA ACONTECENDO]

PROXIMA ETAPA PREVISTA:
[DESCREVER]

Gere o relatorio com:
1. Saudacao personalizada
2. Resumo da situacao atual (linguagem simples, sem juridiques)
3. O que aconteceu no periodo (traduzir cada movimentacao)
4. O que vem pela frente
5. Se o cliente precisa fazer algo
6. Encerramento com canal de contato

Tom: Informativo, tranquilizador, profissional.
Formato: Pronto para enviar por e-mail.
Maximo: 250 palavras.
```

**Resultado esperado:** E-mail de atualizacao claro e profissional, pronto para envio.

---

## Prompt 5: Roteiro para Reuniao com Cliente

**Quando usar:** Antes de uma reuniao importante (inicio de caso, audiencia, decisao, acordo).

**Prompt:**

```
Crie um roteiro para reuniao com cliente com as seguintes informacoes:

TIPO DE REUNIAO: [CONSULTA INICIAL / PREPARACAO PARA AUDIENCIA / DISCUSSAO DE PROPOSTA DE ACORDO / EXPLICACAO DE SENTENCA / OUTRO]
DURACAO ESTIMADA: [Ex: 30 minutos]
NOME DO CLIENTE: [NOME]
CASO: [RESUMO BREVE]
OBJETIVO DA REUNIAO: [O que precisa ser resolvido/comunicado]

PONTOS QUE O ADVOGADO PRECISA ABORDAR:
1. [PONTO 1]
2. [PONTO 2]
3. [PONTO 3]

INFORMACOES QUE O ADVOGADO PRECISA COLETAR DO CLIENTE:
1. [INFO 1]
2. [INFO 2]

DECISOES QUE O CLIENTE PRECISA TOMAR:
1. [DECISAO 1]

Gere:
1. ROTEIRO SEQUENCIAL: Ordem dos assuntos com tempo estimado por topico
2. PERGUNTAS-CHAVE: Perguntas que o advogado deve fazer
3. PONTOS DE ATENCAO: O que pode ser sensivel ou gerar resistencia do cliente
4. MATERIAL DE APOIO: Documentos que devem estar em maos durante a reuniao
5. CHECKLIST POS-REUNIAO: O que fazer imediatamente apos (ata, e-mail de confirmacao, etc.)

Formato: Lista estruturada, facil de consultar durante a reuniao.
```

**Resultado esperado:** Roteiro pratico que o advogado imprime ou abre no tablet durante a reuniao.
