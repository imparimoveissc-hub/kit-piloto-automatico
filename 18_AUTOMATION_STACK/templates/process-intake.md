# Intake de Processo

Use para coletar o minimo sobre um processo que o usuario quer automatizar.

## Perguntas essenciais

1. Qual processo voce quer automatizar?
2. O que dispara esse processo?
3. Quem participa hoje?
4. Quais ferramentas usa?
5. Quais informacoes entram?
6. O que precisa sair no final?
7. O que nao pode acontecer de jeito nenhum?
8. O que pode rodar automatico e o que precisa de aprovacao?

## Resumo estruturado

```yaml
process_name:
segment:
trigger:
input_data:
current_steps:
desired_output:
tools:
human_approval_needed:
risks:
```

