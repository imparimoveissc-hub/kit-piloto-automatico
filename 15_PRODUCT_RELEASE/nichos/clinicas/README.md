# Nicho: Clinicas (Medicas, Odontologicas, Esteticas)

Kit de templates e prompts prontos para clinicas que querem usar IA para automatizar captacao, atendimento e relacionamento com pacientes.

---

## Estrutura

```
clinicas/
├── CLAUDE.md                        -- Instrucoes do agente para contexto clinico
├── templates/
│   ├── agendamento-automatico.md    -- Fluxo de agendamento via WhatsApp/chatbot
│   ├── follow-up-paciente.md        -- Mensagens pos-consulta e acompanhamento
│   ├── relatorio-captacao.md        -- Relatorio de captacao de pacientes
│   ├── proposta-tratamento.md       -- Apresentacao de plano de tratamento
│   └── reativacao-pacientes.md      -- Campanha para pacientes inativos
├── prompts/
│   ├── captacao-pacientes.md        -- 5 prompts para atrair novos pacientes
│   ├── comunicacao-paciente.md      -- 5 prompts para comunicacao com paciente
│   └── gestao-clinica.md            -- 5 prompts para gestao e operacao
└── README.md                        -- Este arquivo
```

---

## Para quem e

- Donos de clinica que fazem a gestao sozinhos ou com equipe pequena
- Gestores e administradores de clinicas
- Recepcionistas que precisam de scripts e fluxos prontos
- Profissionais de saude que querem melhorar a experiencia do paciente

---

## Como usar

### Templates
Os templates sao modelos prontos para implementar na operacao da clinica. Cada um cobre uma etapa do ciclo do paciente:

1. **Agendamento automatico** -- configure no seu WhatsApp Business ou chatbot
2. **Follow-up paciente** -- ative apos cada consulta para manter o vinculo
3. **Relatorio de captacao** -- preencha semanalmente para acompanhar resultados
4. **Proposta de tratamento** -- personalize e envie apos cada avaliacao
5. **Reativacao de pacientes** -- rode a cada 3 meses para trazer inativos de volta

### Prompts
Os prompts sao instrucoes prontas para usar com IA (ChatGPT, Claude, Gemini). Copie, substitua os campos entre colchetes [ ] e execute:

- **Captacao** -- anuncios, scripts de atendimento, conteudo educativo, programa de indicacao, Google Meu Negocio
- **Comunicacao** -- confirmacoes, respostas padrao, comunicados, orientacoes pos-consulta, pesquisa de satisfacao
- **Gestao** -- diagnostico operacional, SOPs, analise de dados, precificacao, planejamento mensal

---

## Ciclo do paciente coberto

```
CAPTACAO → AGENDAMENTO → CONSULTA → FOLLOW-UP → RETORNO → REATIVACAO
   ↑          ↑            ↑          ↑           ↑          ↑
 prompts   template     template    template    template   template
captacao   agendamento  proposta    follow-up   follow-up  reativacao
```

---

## Segmentos atendidos

| Segmento | Exemplos |
|----------|----------|
| Clinica medica | Consultorios, policlinicas, clinicas especializadas |
| Clinica odontologica | Dentistas, ortodontistas, implantodontistas |
| Clinica de estetica | Harmonizacao, dermatologia estetica, procedimentos corporais |

Os templates e prompts incluem variacoes por segmento quando necessario.

---

## Regras importantes

- **LGPD**: dados de saude sao dados sensiveis. Todos os templates incluem orientacoes de consentimento e opt-out.
- **Etica**: a IA nao faz diagnostico, nao prescreve e nao substitui profissional de saude.
- **Tom**: acolhedor e profissional. Nunca vendedor agressivo.
- **Vocabulario**: paciente (nao cliente), consulta (nao reuniao), agendamento (nao booking).
