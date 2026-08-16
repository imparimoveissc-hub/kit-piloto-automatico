# Kit Piloto Automatico com IA -- Nicho Advocacia

## O que e isto

Kit de templates e prompts prontos para escritorios de advocacia que querem usar IA para automatizar o operacional: organizacao de casos, redacao de pecas, comunicacao com clientes e gestao de honorarios.

O foco e PRODUTIVIDADE e ORGANIZACAO. O kit nao substitui o trabalho juridico -- ele elimina o tempo gasto com formatacao, redacao repetitiva e comunicacoes de rotina.

---

## Como usar em 3 passos

### Passo 1: Personalize

Antes de comecar, edite os templates com os dados do seu escritorio:

- Nome do escritorio
- Dados de contato (telefone, e-mail, endereco)
- Areas de atuacao
- Nome dos advogados responsaveis
- Faixa de valores de honorarios (proposta)

### Passo 2: Escolha o template ou prompt certo

| Preciso de... | Use |
|----------------|-----|
| Organizar um novo caso | `templates/briefing-caso.md` |
| Estruturar uma peticao | `templates/peticao-inicial.md` |
| Informar o cliente sobre o andamento | `templates/relatorio-cliente.md` |
| Apresentar honorarios | `templates/proposta-honorarios.md` |
| Enviar mensagem de acompanhamento | `templates/follow-up-cliente.md` |
| Pesquisar jurisprudencia | `prompts/pesquisa-jurisprudencia.md` |
| Redigir pecas com IA | `prompts/redacao-pecas.md` |
| Comunicar com cliente via IA | `prompts/atendimento-cliente.md` |

### Passo 3: Preencha, revise, use

1. Copie o template ou prompt
2. Preencha os campos entre `[COLCHETES]`
3. Se for prompt, cole na IA de sua preferencia (ChatGPT, Claude, Gemini)
4. Revise o resultado -- nunca use sem revisar
5. Adapte ao caso especifico

---

## Estrutura de Arquivos

```
advocacia/
├── CLAUDE.md                         <- Instrucoes do agente (contexto juridico)
├── README.md                         <- Este arquivo
├── templates/
│   ├── briefing-caso.md              <- Briefing padronizado de novo caso
│   ├── peticao-inicial.md            <- Estrutura de organizacao de peticao
│   ├── relatorio-cliente.md          <- Relatorio de andamento pro cliente
│   ├── proposta-honorarios.md        <- Proposta de honorarios profissional
│   └── follow-up-cliente.md          <- 5 modelos de mensagem de acompanhamento
└── prompts/
    ├── pesquisa-jurisprudencia.md    <- 5 prompts para pesquisa juridica
    ├── redacao-pecas.md              <- 5 prompts para redacao de pecas
    └── atendimento-cliente.md        <- 5 prompts para comunicacao com cliente
```

---

## Templates (5)

| Template | Para que serve | Quando usar |
|----------|---------------|-------------|
| **Briefing de Caso** | Centralizar todas as informacoes de um novo caso | Ao receber qualquer demanda nova |
| **Peticao Inicial** | Organizar a estrutura de uma peticao | Antes de redigir a peca (nao e modelo juridico, e organizador) |
| **Relatorio ao Cliente** | Manter o cliente informado | Mensal (andamento regular) ou semanal (fase critica) |
| **Proposta de Honorarios** | Apresentar valores de forma profissional | Na contratacao de novo servico |
| **Follow-up** | Mensagens padronizadas de acompanhamento | Boas-vindas, atualizacoes, lembretes, pedidos de documentos, resultados |

---

## Prompts (15)

### Pesquisa de Jurisprudencia (5)

| Prompt | Objetivo |
|--------|----------|
| Mapeamento de Teses | Identificar todas as teses aplicaveis ao caso |
| Busca por Tema | Encontrar decisoes de apoio para tese especifica |
| Analise de Sumulas | Verificar sumulas e OJs aplicaveis |
| Construcao de Argumentacao | Montar estrutura logica do argumento juridico |
| Comparativo entre Tribunais | Mapear divergencias e definir estrategia |

### Redacao de Pecas (5)

| Prompt | Objetivo |
|--------|----------|
| Peticao Inicial | Gerar rascunho completo de exordial |
| Contestacao | Estruturar defesa completa |
| Recurso | Elaborar razoes de apelacao ou agravo |
| Peticao Intermediaria | Criar manifestacoes e peticoes de andamento |
| Revisao de Peca | Analisar e melhorar peca ja escrita |

### Atendimento ao Cliente (5)

| Prompt | Objetivo |
|--------|----------|
| E-mail Pos-Consulta | Formalizar o primeiro contato apos consulta |
| Explicacao de Decisao | Traduzir decisao judicial para linguagem simples |
| Respostas para FAQ | Criar banco de respostas para duvidas comuns |
| Relatorio Simplificado | Gerar atualizacao rapida para o cliente |
| Roteiro de Reuniao | Preparar pauta estruturada para reuniao |

---

## Avisos Importantes

1. **A IA nao substitui o advogado.** Todo output deve ser revisado por profissional habilitado.

2. **Sigilo profissional.** Ao usar IA com dados de clientes, verifique as politicas de privacidade da ferramenta. Prefira ferramentas que nao usam seus dados para treinamento.

3. **Jurisprudencia.** A IA pode gerar referencias incorretas ou inexistentes. Sempre valide em fontes oficiais (sites dos tribunais, bases de dados juridicas).

4. **Responsabilidade.** O advogado e o responsavel por todo documento produzido. A IA e ferramenta, nao autora.

5. **OAB e Etica.** Respeite o Codigo de Etica da OAB. A IA nao pode captar clientes, prometer resultados ou substituir a consultoria juridica personalizada.
