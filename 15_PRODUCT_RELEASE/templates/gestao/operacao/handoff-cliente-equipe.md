# Handoff de Cliente Novo - Comercial -> Time de Entrega

> Documento que o vendedor preenche APOS fechar venda, ANTES do kick-off com o time de entrega.
> Garante que time de entrega comece sabendo TUDO que foi prometido + contexto do cliente.
> Sem isso bem feito: time entrega o que ACHA que foi vendido, cliente fica frustrado, churn.

---

## Cabecalho

```yaml
cliente: "{{NOME_CLIENTE}}"
empresa: "{{NOME_EMPRESA_CLIENTE}}"
data_fechamento: "[AAAA-MM-DD]"
vendedor_responsavel: "[Nome]"
gerente_conta_atribuido: "[Nome]"
data_kickoff_marcada: "[AAAA-MM-DD]"
modalidade_servico: "{{NOME_SERVICO_CONTRATADO}}"
ticket_mensal: "R$ {{VALOR}}"
prazo_contrato: "[N meses] [com renovacao automatica? S/N]"
```

---

## 1. DADOS BASICOS DO CLIENTE

### Empresa

| Campo | Valor |
|---|---|
| Razao social | [Nome completo] |
| Nome fantasia | [Nome comercial] |
| CNPJ | [XX.XXX.XXX/XXXX-XX] |
| Inscricao estadual | [se aplicavel] |
| Endereco | [Rua, num, bairro, cidade/UF, CEP] |
| Site | [URL] |
| Setor / segmento | [Industria + nicho especifico] |
| Faturamento estimado | [Faixa] |
| Numero de funcionarios | [N] |
| Tempo de mercado | [N anos] |
| Cidade onde opera | [Cidade ou multi-cidade/estado/pais] |

### Decisor / contato principal

| Campo | Valor |
|---|---|
| Nome completo | [Nome] |
| Cargo | [Cargo] |
| Email | [email@empresa.com] |
| WhatsApp | [+55 XX XXXXX-XXXX] |
| Idade aproximada | [faixa] |
| Personalidade (1 linha) | [analitico / decidido / paciente / impaciente / etc] |
| Como prefere se comunicar | [Email / WhatsApp / Reuniao gravada / Texto longo / Audio] |
| Horario preferido pra falar | [Manha / Tarde / Noite] |
| Conta secundaria de contato | [Outro decisor / financeiro / assistente] |

---

## 2. O QUE FOI VENDIDO

### Descricao do servico contratado (palavras do contrato)

[A PREENCHER - copia/cola exata do que esta no contrato]

### Entregaveis especificos (lista)

```
- [Entregavel 1 + frequencia]
- [Entregavel 2 + frequencia]
- [Entregavel 3 + frequencia]
...
```

Exemplo:
```
- DRE mensal enviado por email ate dia util 10
- Reuniao mensal de 30 min na primeira semana do mes
- Suporte por WhatsApp em horario comercial (resposta em ate 4h)
- Revisao trimestral profunda (1h30, mais aprofundada)
- Acesso ao painel do cliente com dados em tempo real
```

### Resultados prometidos (textualmente como foi vendido)

> Atencao: o que voce PROMETEU. Se prometeu algo, o time precisa saber pra entregar.

```
[A PREENCHER]
```

Exemplo:
"Em ate 90 dias, o cliente recebe DRE acionavel + identificacao de pelo menos 1 oportunidade de
economia tributaria + 1 reuniao mensal de revisao. Em 6 meses, projetamos melhoria minima de
10% na margem liquida atraves de identificacao de despesas ociosas (mas sem garantia formal de %)."

### O que NAO esta incluido (escopo OUT)

> Pra evitar atrito depois.

```
- [Item 1 que voce explicou que NAO faz]
- [Item 2]
- [Item 3]
```

Exemplo:
```
- Apuracao de IR pessoa fisica do socio (servico avulso, R$ X)
- Defesa em fiscalizacao da Receita (escopo separado)
- Treinamento de equipe do cliente (servico avulso)
- Implantacao de ERP (parceiro recomendado, nao nos)
```

---

## 3. COMERCIAL (CONTRATO E PAGAMENTO)

| Campo | Valor |
|---|---|
| Modalidade de cobranca | [Mensal / Trimestral / Anual / Por entrega] |
| Valor mensal | R$ [valor] |
| Forma de pagamento | [Boleto / Cartao recorrente / PIX / Boleto + Asaas] |
| Dia do mes de cobranca | [Dia X] |
| Vencimento configurado | [Antes do servico / depois / no dia] |
| Reajuste anual | [IGPM / IPCA / Fixo / Nao reajusta] |
| Multa rescisao | [Conforme contrato] |
| Prazo de fidelizacao | [N meses ou Nao tem] |

### Pendencias comerciais

- [ ] Contrato assinado pelas duas partes (anexar PDF aqui ou link)
- [ ] Primeira cobranca emitida
- [ ] Dados bancarios do cliente coletados (PIX ou conta pra reembolso)
- [ ] Termos de LGPD assinados

---

## 4. CONTEXTO E HISTORIA

### Como o cliente chegou (origem do lead)

[A PREENCHER]

Exemplos:
- "Indicacao do [Nome do cliente] em janeiro/2026"
- "Trafego pago Meta Ads, campanha [X]"
- "Conteudo organico Instagram, post viral [Y]"
- "Evento [Z] em [cidade]"

### Pra que ele esta contratando AGORA (gatilho real)

> O que mudou na vida dele que faz ele estar disposto a pagar hoje? Sem isso, voce nao entende
> a urgencia real do cliente.

[A PREENCHER]

Exemplo:
"Cliente acabou de demitir contador antigo apos descobrir que estava deixando R$ 18k/mes em
impostos a recolher errado. Esta com medo de auditoria. Quer alguem que pegue o caso DESDE JA,
nao em 60 dias."

### Dor principal (em palavras dele)

> Citacao direta de algo que ele disse em call.

```
"[Citacao direta]"
```

### O que JA TENTOU antes (e por que falhou)

```
- [Tentativa 1] - falhou porque [razao]
- [Tentativa 2] - falhou porque [razao]
```

### Expectativas declaradas pelo cliente

```
- [Expectativa 1]
- [Expectativa 2]
- [Expectativa 3]
```

> Se alguma expectativa esta fora do escopo, MARCAR e tratar na kickoff.

---

## 5. PERFIL DO CLIENTE (informacoes uteis pro time)

### Estilo de comunicacao

- Prefere: [Emails longos / WhatsApp rapido / Reunioes / Documentos formais]
- Evita: [Telefone / Audio longo / Reuniao demais]
- Decide: [Sozinho / Com socio / Com socio + esposa / Com conselho]
- Pode ser direto? [SIM - aprecia franqueza / NAO - precisa diplomacia]

### Sinais de alerta detectados pelo vendedor

```
- [Sinal 1: ex. cliente perguntou 4 vezes sobre prazo de resposta]
- [Sinal 2: ex. socio dele apareceu na call e fez 7 perguntas tecnicas detalhadas]
- [Sinal 3: ex. cliente mencionou que ja saiu de outro fornecedor por preco]
```

### O que cliente VALORIZA muito

```
- [Coisa 1 - ex: pontualidade]
- [Coisa 2 - ex: atencao individualizada]
- [Coisa 3 - ex: relatorios visuais]
```

### O que cliente NAO TOLERA

```
- [Coisa 1 - ex: erro de portugues]
- [Coisa 2 - ex: atraso]
- [Coisa 3 - ex: ser tratado igual aos outros]
```

---

## 6. ACESSOS E FERRAMENTAS NECESSARIOS

> O que o time vai precisar pra comecar?

### Acessos a coletar do cliente

- [ ] Acesso ao sistema atual (login + senha): [sistema]
- [ ] Acesso ao banco / extratos: [forma de envio]
- [ ] Acesso a conta de email (se for usar): [email]
- [ ] Acesso a Google Drive / Dropbox: [link]
- [ ] Senha do certificado digital (se aplicavel): [como pegar]
- [ ] Acesso a NF-e / sistema de nota: [endereco]

### Acessos a entregar pro cliente

- [ ] Login no painel
- [ ] Convite pro Drive compartilhado
- [ ] Grupo de WhatsApp do cliente criado
- [ ] Email institucional dedicado (se aplicavel)
- [ ] Cal.com / agenda do gerente de conta

---

## 7. PRIMEIRA REUNIAO (KICK-OFF)

| Campo | Valor |
|---|---|
| Data agendada | [AAAA-MM-DD HH:MM] |
| Duracao | [N min] |
| Modalidade | [Presencial / Video / Telefone] |
| Link da call | [URL] |
| Participantes do nosso lado | [Vendedor + Gerente de conta + Analista responsavel] |
| Participantes do lado do cliente | [Decisor + outros] |
| Pauta proposta | [link ou cola aqui] |

### Pauta sugerida da kickoff

1. Apresentacoes (5 min)
2. Recap do que foi vendido (5 min)
3. Cronograma das primeiras 4 semanas (10 min)
4. Coleta dos acessos e documentos necessarios (10 min)
5. Definicao de canais de comunicacao + horarios (5 min)
6. Primeira entrega prevista pra [DATA] (5 min)
7. Espaco pra perguntas / ajustes finais (5 min)

---

## 8. PRIMEIROS 30 DIAS - ROADMAP

| Semana | Atividade principal | Responsavel | Output |
|---|---|---|---|
| Semana 1 | Kick-off + coleta acessos + ambientacao | [nome] | Acessos OK |
| Semana 2 | [Atividade] | [nome] | [Output] |
| Semana 3 | [Atividade] | [nome] | [Output] |
| Semana 4 | [Primeira entrega] | [nome] | [Output principal] |

---

## 9. POS-HANDOFF (vendedor)

Apos preencher este doc:

- [ ] Compartilhar no canal #handoffs ou ferramenta interna
- [ ] Marcar reuniao de kickoff com cliente
- [ ] Atualizar status do cliente no CRM pra "Onboarding"
- [ ] Apresentar cliente pro gerente de conta atribuido (5 min de call rapida)
- [ ] Estar disponivel nas primeiras 2 semanas pra eventual atrito de transicao

---

## 10. RECEBIMENTO (time de entrega)

Apos receber este doc, gerente de conta:

- [ ] Le tudo (sem pular)
- [ ] Anota duvidas e pergunta pro vendedor ANTES da kickoff
- [ ] Prepara pauta da kickoff (pode usar a sugerida acima)
- [ ] Configura acessos internos (CRM, painel, grupo WhatsApp)
- [ ] Reserva agenda dos primeiros 30 dias

---

## Versionamento

| Versao | Data | Mudanca |
|---|---|---|
| v1 | [AAAA-MM-DD] | Handoff inicial |
| v2 | [AAAA-MM-DD] | [Ajuste pos-kickoff se aplicavel] |
