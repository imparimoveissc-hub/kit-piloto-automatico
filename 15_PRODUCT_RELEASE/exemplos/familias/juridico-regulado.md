# Familia — Juridico e Regulado

## Contexto

Operacao com alto risco de promessa, confidencialidade, prazos e linguagem precisa.

Exemplos: advocacia, contabilidade regulada, compliance, consultoria juridica.

## Primeira tarefa util

Criar intake de caso/cliente sem aconselhamento juridico automatico.

```text
/briefing
Quero um intake seguro para novo cliente juridico/regulado.
```

## Automacao sugerida

Nome: intake de caso.

Trigger: prospect entra em contato.

Fluxo:

1. coletar dados basicos;
2. entender area/tema;
3. coletar documentos existentes;
4. identificar prazo critico;
5. resumir para responsavel humano;
6. bloquear qualquer orientacao juridica final automatica.

## WhatsApp sugerido

```text
Oi, [NOME]. Para organizar seu atendimento, me envie:

1. qual e o assunto principal;
2. se existe algum prazo;
3. quais documentos voce ja tem;
4. melhor horario para retorno.

As informacoes serao revisadas por um responsavel antes de qualquer orientacao.
```

## Squad inicial

- CoS;
- Briefing Agent;
- Automation Architect;
- QA Editor;
- especialista humano responsavel.

## Riscos

- dar parecer sem humano;
- perder prazo;
- expor dado confidencial;
- prometer ganho/resultado;
- armazenar documento sensivel sem regra.

## Comandos recomendados

- `/setup-nicho`
- `/briefing`
- `/automatizar-processo`
- `/revisar`

