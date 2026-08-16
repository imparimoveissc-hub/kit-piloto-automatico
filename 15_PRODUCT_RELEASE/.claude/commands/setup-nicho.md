# /setup-nicho

Configure o kit para qualquer segmento, mesmo quando nao existir preset pronto.

## Execute

1. Leia `nichos/family-classifier.md`.
2. Leia `nichos/setup-nicho-playbook.md`.
3. Se o usuario ainda nao explicou o negocio, pergunte apenas:
   - o que vende;
   - para quem;
   - canal principal;
   - maior gargalo hoje;
   - se usa WhatsApp.
4. Classifique a familia operacional.
5. Verifique preset em `nichos/`.
6. Escolha templates, WhatsApp flow e automacao inicial.
7. Gere `.claude/config.md` usando `nichos/config-template.yaml`.
8. Sugira:
   - squad inicial;
   - comandos recorrentes;
   - primeira tarefa util;
   - riscos que exigem humano.

## Output curto para o usuario

```yaml
familia:
preset_usado:
templates_recomendados:
whatsapp_recomendado:
automacao_recomendada:
squad_inicial:
primeira_tarefa:
pendencias:
```

Tudo que envolver envio, CRM, API, publicacao ou dado sensivel fica em modo `draft`.
