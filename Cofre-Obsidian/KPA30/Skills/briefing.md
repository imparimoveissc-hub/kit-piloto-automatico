---
name: briefing
description: Monta briefing completo de cliente novo ou projeto
---

# /briefing — Briefing de Cliente

## Processo

### 1. Ler contexto
Leia `.claude/config.md` pra saber o segmento, servicos e tom de voz.

### 2. Coletar dados
Pergunte:
- "Nome do cliente ou empresa?"
- "Qual o projeto/demanda?"

### 3. Perguntas estrategicas (adaptar ao segmento)

**Se trafego:**
1. Qual o objetivo da campanha? (leads, vendas, agendamentos)
2. Qual a verba mensal disponivel?
3. Qual o publico-alvo? (idade, regiao, interesses)
4. Ja rodou campanha antes? Quais resultados?
5. Qual o KPI principal? (CPL, CPA, ROAS)

**Se social media:**
1. Qual o objetivo do conteudo? (engajamento, vendas, autoridade)
2. Quais plataformas? (Instagram, TikTok, LinkedIn)
3. Qual a frequencia de postagem desejada?
4. Tem identidade visual definida?
5. Quem e o publico-alvo?

**Se designer:**
1. Qual o tipo de material? (social, impresso, branding)
2. Tem identidade visual / brandbook?
3. Quais formatos e dimensoes?
4. Quais as referencias visuais?
5. Qual o prazo?

**Se videomaker:**
1. Qual o tipo de video? (institucional, reel, depoimento)
2. Qual a duracao desejada?
3. Tem roteiro ou precisa criar?
4. Onde sera veiculado?
5. Qual o tom? (corporativo, informal, educativo)

**Se advocacia:**
1. Qual a area do direito?
2. Qual a situacao atual do caso?
3. Quais documentos ja tem?
4. Qual a pretensao/objetivo?
5. Tem prazo processual proximo?

**Se B2B:**
1. Qual o produto/servico que vende?
2. Qual o ICP (perfil de cliente ideal)?
3. Qual o ticket medio?
4. Qual o ciclo de venda?
5. Quais canais de aquisicao usa?

**Se clinica:**
1. Qual a especialidade?
2. Quais procedimentos quer promover?
3. Qual a regiao de atendimento?
4. Qual o ticket medio dos procedimentos?
5. Ja faz marketing digital?

### 4. Gerar briefing

Monte o documento com:
```markdown
# Briefing — [Nome do Cliente]
Data: [data atual]

## Dados do cliente
- Empresa: [nome]
- Contato: [se informado]
- Segmento: [nicho do cliente]

## Objetivo do projeto
[resumo claro do que precisa ser feito]

## Publico-alvo
[quem e o publico final]

## Escopo e entregaveis
1. [entregavel 1]
2. [entregavel 2]
3. [entregavel 3]

## Cronograma
| Etapa | Prazo |
|-------|-------|
| [etapa 1] | [data] |
| [etapa 2] | [data] |

## KPIs / Metricas de sucesso
- [KPI 1]
- [KPI 2]

## Tom de voz
[como se comunicar]

## Observacoes
[qualquer detalhe adicional]
```

### 5. Salvar
Crie a pasta do cliente se nao existir:
```bash
mkdir -p clientes/[nome-cliente-kebab-case]
```
Salve em `clientes/[nome-cliente]/briefing.md`

### 6. Proximo passo
Pergunte: "Briefing pronto. Quer que eu comece a criar o material? (/criar)"
