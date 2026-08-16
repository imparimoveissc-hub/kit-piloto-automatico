# 18_AUTOMATION_STACK — Automacoes de Processos

Camada para transformar processos criados pelo usuario em automacoes seguras, documentadas e adaptaveis a qualquer nicho.

## Objetivo

O cliente pode ser de qualquer segmento. O agente de automacoes deve conseguir pegar um processo descrito em linguagem simples e devolver:

- processo entendido;
- gargalos e riscos;
- automacao possivel;
- ferramentas sugeridas;
- blueprint;
- SOP;
- dados necessarios;
- gatilhos;
- handoffs;
- checklist de teste;
- plano de ativacao.

## Principio

Automacao nao e sair conectando ferramenta. Automacao e padronizar processo antes.

Ordem obrigatoria:

1. Entender processo atual.
2. Separar entradas, decisoes, saidas e responsaveis.
3. Identificar riscos e pontos que exigem humano.
4. Criar fluxo em modo `draft`.
5. Definir teste.
6. Ativar somente com confirmacao humana.

## Agente

- `agents/automation-orchestrator.md`: entry point unico para processos, SOPs, automacoes e integrações.

## Task principal

- `tasks/build-process-automation.md`: contrato para transformar processo em automacao.

## Templates

- `templates/process-intake.md`: coleta minima.
- `templates/automation-blueprint.yaml`: blueprint estruturado.
- `templates/sop-template.md`: SOP de execucao humana/assistida.
- `templates/tool-connector-matrix.md`: matriz de ferramenta, acesso, risco e confirmacao.

## Ferramentas alvo

O V30 nao deve depender de uma ferramenta unica. O blueprint pode ser usado para:

- Cowork;
- n8n;
- Make;
- Zapier;
- planilhas;
- CRM;
- WhatsApp;
- email;
- ClickUp/Notion/Asana;
- scripts locais;
- operacao manual assistida por IA.

## Safety

Bloqueia ativacao real quando:

- envia mensagem para cliente/lead;
- altera CRM ou status comercial;
- movimenta dinheiro;
- altera campanha/anuncio;
- expõe dados pessoais;
- executa acao irreversivel;
- depende de credencial nao validada;
- nao tem plano de rollback.

