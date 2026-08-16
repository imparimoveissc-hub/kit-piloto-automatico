# Task — Build Process Automation

Use quando o usuario quiser automatizar um processo de qualquer segmento.

## Input minimo

```yaml
process_name:
segment:
goal:
current_steps:
trigger:
who_is_involved:
tools_used:
data_sources:
desired_output:
constraints:
automation_limit:
```

Se o usuario nao souber preencher, conduza com perguntas simples e aceite respostas incompletas.

## Procedimento

1. Reescreva o processo atual em etapas numeradas.
2. Separe:
   - entrada;
   - transformacao;
   - decisao;
   - saida;
   - responsavel.
3. Marque cada etapa como:
   - automatizar agora;
   - assistida por IA;
   - manter humano;
   - bloquear por risco/dado.
4. Monte `automation-blueprint.yaml`.
5. Monte SOP humano.
6. Monte checklist de teste.
7. Liste acessos necessarios.
8. Defina rollback.

## Output

Entregar nesta ordem:

1. resumo executivo;
2. blueprint;
3. SOP;
4. ferramentas/acessos;
5. riscos e limites;
6. teste;
7. proximo passo.

## Acceptance

Passa em `GATE-AUTOMATION` quando:

- processo tem trigger claro;
- inputs/outputs estao definidos;
- etapa humana esta separada de etapa automatica;
- riscos e permissoes estao explicitos;
- existe teste antes de ativar;
- nao ha acao real sem confirmacao.

