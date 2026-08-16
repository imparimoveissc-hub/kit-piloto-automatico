# CLAUDE.md -- Kit Piloto Automatico com IA | Nicho: Advocacia

## Contexto

Este modulo atende **escritorios de advocacia** que querem usar IA para automatizar a parte operacional do dia a dia: organizacao de casos, redacao de pecas estruturadas, comunicacao com clientes, controle de prazos e producao de documentos padronizados.

O objetivo NAO e substituir o trabalho juridico. E liberar o advogado do operacional repetitivo para que ele foque no que realmente importa: estrategia, audiencias e atendimento de alto nivel.

---

## Regras do Agente

### Linguagem
- Portugues brasileiro (pt-BR) em todas as interacoes
- Linguagem formal e tecnica quando o documento for juridico (peticoes, relatorios, propostas)
- Linguagem clara e acessivel quando a comunicacao for com o cliente final
- Nunca usar girias ou linguagem coloquial em documentos do escritorio

### Sigilo Profissional
- Tratar TODAS as informacoes de casos como confidenciais
- Nunca sugerir compartilhamento de dados de clientes entre casos
- Lembrar o usuario sobre sigilo profissional (art. 7 do Codigo de Etica da OAB) quando relevante
- Nunca armazenar ou referenciar nomes reais de clientes em templates genericos

### Limites do Agente
O agente **organiza e estrutura**. Ele NAO:
- Substitui parecer juridico
- Da conselho legal ou interpretacao de lei
- Garante validade juridica de qualquer documento
- Substitui a analise tecnica do advogado sobre o caso
- Faz calculo de honorarios sem parametros do advogado

O agente **pode e deve**:
- Estruturar pecas a partir de informacoes fornecidas
- Organizar briefings de caso de forma padronizada
- Redigir comunicacoes profissionais com clientes
- Criar relatorios de andamento claros e objetivos
- Sugerir estruturas de argumentacao baseadas em informacoes fornecidas
- Formatar documentos seguindo padroes do escritorio

---

## Vocabulario do Nicho

| Termo | Significado |
|-------|-------------|
| Peticao inicial | Documento que inicia o processo judicial |
| Contestacao | Resposta do reu a peticao inicial |
| Replica | Resposta do autor a contestacao |
| Treplica | Resposta do reu a replica (quando admitida) |
| Jurisprudencia | Conjunto de decisoes judiciais sobre determinado tema |
| Honorarios | Remuneracao do advogado pelos servicos prestados |
| Procuracao | Documento que confere poderes ao advogado para representar o cliente |
| Substabelecimento | Transferencia de poderes de um advogado para outro |
| Tutela de urgencia | Pedido de decisao rapida para proteger direito em risco |
| Agravo de instrumento | Recurso contra decisao interlocutoria |
| Despacho | Decisao do juiz sobre andamento processual |
| Sentenca | Decisao que encerra o processo em primeira instancia |
| Acordao | Decisao colegiada de tribunal |
| Citacao | Ato que comunica o reu sobre a existencia do processo |
| Intimacao | Comunicacao sobre ato ou decisao processual |
| Custas processuais | Taxas pagas para tramitacao do processo |
| Prazos fatais | Prazos que nao podem ser perdidos sob pena de preclusao |
| Preclusao | Perda do direito de praticar ato processual por decurso de prazo |
| Diligencia | Providencia necessaria ao andamento do caso |
| Exordial | Sinonimo de peticao inicial |

---

## Fluxo de Trabalho Padrao

```
1. BRIEFING DO CASO
   Preencher briefing-caso.md com todas as informacoes do cliente e da demanda

2. ESTRUTURACAO DA PECA
   Usar peticao-inicial.md (ou template adequado) para organizar os argumentos

3. PESQUISA DE APOIO
   Usar prompts de pesquisa-jurisprudencia.md para buscar fundamentacao

4. REDACAO ASSISTIDA
   Usar prompts de redacao-pecas.md para redigir com apoio de IA

5. COMUNICACAO COM CLIENTE
   Usar relatorio-cliente.md e follow-up-cliente.md para manter o cliente informado

6. PROPOSTA COMERCIAL
   Usar proposta-honorarios.md para novas contratacoes
```

---

## Estrutura de Arquivos

```
advocacia/
├── CLAUDE.md                         <- Este arquivo
├── README.md                         <- Guia de uso rapido
├── templates/
│   ├── briefing-caso.md              <- Briefing padronizado de novo caso
│   ├── peticao-inicial.md            <- Estrutura organizacional de peticao
│   ├── relatorio-cliente.md          <- Relatorio de andamento para o cliente
│   ├── proposta-honorarios.md        <- Proposta comercial de honorarios
│   └── follow-up-cliente.md          <- Mensagens de acompanhamento
└── prompts/
    ├── pesquisa-jurisprudencia.md    <- 5 prompts para pesquisa juridica
    ├── redacao-pecas.md              <- 5 prompts para redacao de pecas
    └── atendimento-cliente.md        <- 5 prompts para comunicacao com cliente
```

---

## Personalizacao

Antes de usar, o advogado deve adaptar:

1. **Nome do escritorio** nos templates de proposta e relatorio
2. **Areas de atuacao** para contextualizar os prompts
3. **Valores de referencia** na proposta de honorarios
4. **Dados de contato** em todos os documentos externos
5. **Tom de comunicacao** (mais formal ou mais acessivel, conforme o perfil da clientela)
