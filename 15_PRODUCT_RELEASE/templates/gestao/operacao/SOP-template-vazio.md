# SOP - {{NOME_DO_PROCESSO}}

> Standard Operating Procedure. Template padrao pra documentar qualquer processo recorrente.
> Substitua todas as `{{VARIAVEIS}}` e `[A PREENCHER]` antes de usar.

---

## Cabecalho

```yaml
processo: "{{NOME_DO_PROCESSO}}"
versao: "[v1.0]"
data_criacao: "[AAAA-MM-DD]"
ultima_revisao: "[AAAA-MM-DD]"
owner: "[Nome - cargo]"
revisado_por: "[Nome - cargo]"
area: "[Vendas / Marketing / Financeiro / Operacao / Entrega / RH / Outro]"
criticidade: "[Critico / Alto / Medio / Baixo]"
frequencia: "[Diario / Semanal / Mensal / Por demanda / Por evento]"
```

---

## Objetivo

> Em 1 paragrafo: o que esse processo entrega + por que importa.

[A PREENCHER]

Exemplo:
"Entregar resposta a leads inbound do site em ate 1 hora util, com qualificacao basica, pra que o vendedor recebem so leads quentes. Importante porque tempo de resposta > 1h reduz conversao em 60%."

---

## Quando usar (trigger)

> O que dispara este processo?

[A PREENCHER]

Exemplos:
- "Novo lead chega via formulario do site"
- "Cliente envia documento mensal"
- "Time de vendas marca status 'ganho' no CRM"
- "Toda segunda-feira as 9h"

---

## Quem participa (roles)

| Quem | O que faz nesse processo |
|---|---|
| [Nome ou cargo 1] | [Responsabilidade] |
| [Nome ou cargo 2] | [Responsabilidade] |
| [Nome ou cargo 3] | [Responsabilidade] |

---

## Entradas necessarias (inputs)

> O que precisa estar disponivel ANTES de comecar?

- [Input 1]
- [Input 2]
- [Input 3]
- ...

Exemplo:
- Lead com nome + email + telefone preenchidos
- Acesso ao CRM (HubSpot / RD / proprio)
- Template de email de boas-vindas atualizado

---

## Saidas (entregaveis)

> O que sai apos o processo rodar?

- [Output 1]
- [Output 2]
- [Output 3]

Exemplo:
- Lead respondido por email com proxima acao clara
- Tag aplicada no CRM ([Qualificado / Desqualificado / Nutrir])
- Tarefa de follow-up agendada (se aplicavel)
- Linha no controle interno preenchida

---

## Passo a passo

### Etapa 1 - [Nome da etapa]

**Quem:** [Cargo / pessoa]
**Tempo estimado:** [X minutos]
**Ferramenta:** [Sistema / plataforma]

1. [Acao 1]
2. [Acao 2]
3. [Acao 3]

**Bloqueador:** [Quando essa etapa nao pode avancar]

---

### Etapa 2 - [Nome da etapa]

**Quem:** [Cargo / pessoa]
**Tempo estimado:** [X minutos]
**Ferramenta:** [Sistema / plataforma]

1. [Acao 1]
2. [Acao 2]
3. [Acao 3]

**Bloqueador:** [...]

---

### Etapa 3 - [...]

[Continuar conforme necessario - geralmente 4-8 etapas]

---

## Gate de qualidade

> Antes de considerar o processo "feito", validar:

- [ ] [Criterio 1 - mensuravel]
- [ ] [Criterio 2]
- [ ] [Criterio 3]
- [ ] [Criterio 4]

**Bloqueador critico:** [Qual erro impede de marcar como feito]

---

## Tempo total estimado

[X horas / minutos por execucao]

---

## Frequencia de revisao do SOP

> Quando esse documento precisa ser atualizado?

- [Trigger 1: ex. mudanca de ferramenta]
- [Trigger 2: ex. reclamacao de cliente sobre o output]
- [Trigger 3: ex. revisao trimestral fixa]

---

## Anti-padroes (NAO fazer)

> O que NAO deve acontecer durante esse processo.

- [Anti-padrao 1]
- [Anti-padrao 2]
- [Anti-padrao 3]

Exemplo:
- Responder lead sem nome (gerar email "ola lead" - parece bot)
- Pular qualificacao e mandar direto pra vendedor (ele recebe lixo, perde tempo)
- Atrasar resposta mais de 1h util (perde conversao)

---

## Casos especiais e variantes

> Situacoes em que o processo padrao nao se aplica.

| Caso | Como tratar |
|---|---|
| [Caso 1] | [Procedimento adaptado] |
| [Caso 2] | [Procedimento adaptado] |
| [Caso 3] | [Procedimento adaptado] |

Exemplo:
| Lead vem com tag "VIP" | Pular qualificacao, mandar direto pro vendedor senior |
| Lead vem fora do horario comercial | Email automatico ate 5 min + qualificacao no inicio do proximo expediente |
| Lead duplicado (ja existe no CRM) | Atualizar registro existente, nao criar novo |

---

## Metricas de sucesso

> Como saber se o processo ta funcionando bem?

| Metrica | Meta | Como medir | Frequencia |
|---|---|---|---|
| [Metrica 1] | [Numero] | [Como calcular] | [Diario/Semanal/Mensal] |
| [Metrica 2] | [Numero] | [...] | [...] |
| [Metrica 3] | [Numero] | [...] | [...] |

Exemplo:
| Tempo medio de resposta | < 1h util | (Hora resposta - hora chegada do lead) | Semanal |
| Taxa de qualificacao | > 60% | (Qualificados / total leads) x 100 | Semanal |
| Erro de processo (escapou bloqueador) | < 2% | (Erros / total execucoes) x 100 | Mensal |

---

## Ferramentas e acessos

> Que sistemas precisam estar configurados?

| Ferramenta | Pra que | Quem tem acesso |
|---|---|---|
| [Sistema 1] | [Funcao] | [Time / pessoa] |
| [Sistema 2] | [Funcao] | [Time / pessoa] |

---

## Links e recursos

- [Link pro template de email]
- [Link pro CRM]
- [Link pro Loom explicando processo visualmente]
- [Link pra planilha relacionada]

---

## Treinamento

> Como uma pessoa nova aprende este processo?

1. Le este SOP completo (15-30 min)
2. [Recurso de treinamento 1 - ex: Loom de 10 min]
3. [Recurso 2 - ex: shadow de 3 execucoes com pessoa senior]
4. [Recurso 3 - ex: 3 execucoes assistidas]
5. Autonomo apos [N execucoes] OU [N dias]

---

## Mudancas e versoes

| Versao | Data | Mudanca | Quem |
|---|---|---|---|
| v1.0 | [AAAA-MM-DD] | Criacao do SOP | [Nome] |
| v1.1 | [AAAA-MM-DD] | [Descricao mudanca] | [Nome] |

---

## Owner ativo

> Quem MANTEM esse SOP atualizado.

Nome: [Pessoa]
Cargo: [Cargo]
Quando reportar problema: [Email / canal]
