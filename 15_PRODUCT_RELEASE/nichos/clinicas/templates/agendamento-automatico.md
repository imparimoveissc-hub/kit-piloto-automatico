# Template: Agendamento Automatico via WhatsApp/Chatbot

## Objetivo
Automatizar o processo de agendamento de consultas e avaliacoes, reduzindo a carga da recepcionista e diminuindo o no-show (faltas).

---

## Fluxo Completo

### Etapa 1 -- Primeiro Contato (paciente envia mensagem)

**Mensagem de boas-vindas (automatica):**

```
Ola! Bem-vindo(a) a [Nome da Clinica]. 😊

Sou a assistente virtual e estou aqui para ajudar voce.

O que voce precisa?

1 - Agendar uma consulta/avaliacao
2 - Remarcar um agendamento
3 - Informacoes sobre procedimentos
4 - Falar com a recepcionista

(Digite o numero da opcao)
```

---

### Etapa 2 -- Coleta de Informacoes (opcao 1 selecionada)

**Sequencia de perguntas:**

```
Otimo! Vamos agendar sua consulta.

Qual o seu nome completo?
```

```
Obrigada, [Nome]! Qual especialidade ou procedimento voce procura?

(Exemplos: clinico geral, ortodontia, limpeza, harmonizacao, dermatologia...)
```

```
Voce tem preferencia de dia e horario?

1 - Manha (8h-12h)
2 - Tarde (13h-18h)
3 - Noite (18h-21h) [se aplicavel]
4 - Sem preferencia

(Digite o numero)
```

```
Perfeito! Voce possui convenio ou seria atendimento particular?

1 - Particular
2 - Convenio (informe o nome)
```

---

### Etapa 3 -- Confirmacao do Agendamento

**Mensagem de confirmacao:**

```
Pronto, [Nome]! Seu agendamento esta confirmado:

📋 Procedimento: [Especialidade/Procedimento]
📅 Data: [Data]
🕐 Horario: [Horario]
📍 Endereco: [Endereco da clinica]
👨‍⚕️ Profissional: Dr(a). [Nome]

Importante:
- Chegue 15 minutos antes para cadastro
- Traga documento com foto e carteirinha do convenio (se aplicavel)
- Em caso de impedimento, avise com 24h de antecedencia

Precisando de algo, estamos aqui!
```

---

### Etapa 4 -- Lembretes Automaticos (anti no-show)

**48h antes:**
```
Ola, [Nome]! Passando para lembrar da sua consulta:

📅 [Data] as [Horario]
📍 [Endereco]

Voce confirma presenca?

1 - Sim, estarei la
2 - Preciso remarcar
```

**2h antes:**
```
Ola, [Nome]! Sua consulta e daqui a pouco:

🕐 [Horario] -- [Endereco]

Estamos esperando voce!
```

---

### Etapa 5 -- Remarcacao (opcao 2 no menu ou resposta "preciso remarcar")

```
Sem problema, [Nome]! Vamos encontrar um novo horario para voce.

Qual sua preferencia?

1 - Manha (8h-12h)
2 - Tarde (13h-18h)
3 - Noite (18h-21h)
4 - Proximo horario disponivel
```

---

## Variacoes por Segmento

### Clinica Odontologica
- Adicionar pergunta: "E sua primeira vez em nossa clinica ou ja e paciente?"
- Mencionar que radiografias anteriores podem ser uteis na avaliacao

### Clinica de Estetica
- Adicionar: "Voce ja realizou alguma avaliacao ou procedimento conosco?"
- Mencionar: "A avaliacao e gratuita e sem compromisso" (se aplicavel)

### Clinica Medica
- Adicionar pergunta sobre encaminhamento medico (se necessario)
- Mencionar documentos especificos por especialidade

---

## Metricas para Acompanhar

| Metrica | O que medir |
|---------|-------------|
| Taxa de agendamento | % de contatos que agendam |
| Taxa de no-show | % de faltas sobre agendamentos |
| Tempo medio de resposta | Minutos entre contato e agendamento concluido |
| Taxa de remarcacao | % de pacientes que remarcam vs. cancelam |
| Satisfacao do agendamento | NPS ou nota do processo (pesquisa pos-consulta) |

---

## Observacoes

- Adaptar os horarios e especialidades para a realidade da clinica
- O fluxo deve ser revisado pela equipe antes de ativar
- Todas as mensagens automatizadas devem ter opcao de falar com humano
- Respeitar LGPD: informar que dados serao usados para agendamento e incluir opcao de nao receber lembretes
