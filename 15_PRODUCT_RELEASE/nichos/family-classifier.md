# Classificador de Familia Operacional

Use quando o usuario descrever o negocio em linguagem simples.

## Saida obrigatoria

```yaml
family:
confidence: 0-100
why:
preset_available:
closest_preset:
recommended_templates:
whatsapp_priority:
automation_priority:
risk_level:
first_task:
```

## Familias

### Servico local

Sinais:

- atende por cidade/bairro;
- agenda/orcamento;
- WhatsApp como canal principal;
- lead quer rapidez.

Templates:

- geral;
- whatsapp;
- automacoes.

Primeira tarefa:

- atendimento WhatsApp;
- triagem;
- agenda/orcamento.

### Profissional liberal

Sinais:

- pessoa vende expertise;
- decisao depende de confianca;
- agenda/diagnostico;
- relacionamento individual.

Templates:

- geral;
- proposta;
- briefing;
- follow-up.

Primeira tarefa:

- briefing de diagnostico;
- follow-up;
- proposta simples.

### B2B consultivo

Sinais:

- vende para empresas;
- ciclo de venda longo;
- reuniao/proposta;
- multiplos decisores.

Preset:

- `nichos/b2b`.

Primeira tarefa:

- qualificacao SDR;
- proposta;
- CRM/follow-up.

### Ecommerce

Sinais:

- produtos;
- pedido, carrinho, entrega, troca;
- catalogo;
- suporte/pos-venda.

Templates:

- whatsapp;
- relatorio;
- automacoes.

Primeira tarefa:

- atendimento de produto;
- recuperacao de carrinho;
- suporte pos-venda.

### Infoproduto

Sinais:

- curso, mentoria, comunidade;
- checkout;
- area de membros;
- onboarding de aluno;
- suporte e engajamento.

Templates:

- onboarding;
- follow-up;
- relatorio;
- whatsapp.

Primeira tarefa:

- onboarding pos-compra;
- suporte de acesso;
- recuperacao de lead.

### Agencia/servico digital

Sinais:

- social media, trafego, copy, design, video;
- entregas recorrentes;
- briefing, aprovacao, relatorio.

Templates:

- gestor-trafego;
- social-media;
- designer;
- videomaker;
- geral.

Primeira tarefa:

- organizar briefing;
- criar entrega;
- revisar e empacotar.

### Clinica/saude

Sinais:

- paciente;
- consulta/procedimento;
- agenda;
- dados sensiveis;
- restricao de promessa.

Preset:

- `nichos/clinicas`.

Primeira tarefa:

- agendamento seguro;
- triagem administrativa;
- follow-up pos-atendimento.

### Juridico/regulado

Sinais:

- caso, processo, documento, prazo;
- confidencialidade;
- parecer ou orientacao regulada;
- risco alto.

Preset:

- `nichos/advocacia` quando for juridico.

Primeira tarefa:

- intake seguro;
- organizacao documental;
- briefing de caso.

## Regra de desempate

Se cair em duas familias:

1. escolha a de maior risco regulatorio;
2. se risco igual, escolha a que define o canal principal;
3. se ainda empatar, escolha a que define a primeira entrega.

