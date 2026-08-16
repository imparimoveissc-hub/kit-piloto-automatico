# Instrucoes do Kit Piloto Automatico V30

Sempre opere em pt-BR.

## Emissão automática de notas fiscais (Impar Imóveis)

Nos dias **20, 25, 29 e 30 de cada mês**, ou sempre que o usuário mencionar "emitir notas", "notas pendentes", "rodar emissão", "NFS-e", "notas fiscais Joinville" ou variações: acione a skill **`emitir-notas-fiscais`** imediatamente. O pipeline busca pagamentos no Asaas e emite no portal nfem.joinville.sc.gov.br. Credenciais em `18_AUTOMATION_STACK/nfem-joinville/.env`.

## Nota fiscal avulsa (uma nota manual)

Quando o usuário disser "emitir nota venda", "emitir nota de venda", "nova nota fiscal de venda", "emitir nota avulsa", "nota de aluguel avulsa", "emitir uma nota" ou variações: acione a skill **`emitir-nota-avulsa`**. Ela pergunta CNPJ/CPF → venda (item 1005) ou aluguel (item 1712) → descrição → valor; natureza sempre 107; emite e envia o PDF no WhatsApp do Jonata (`554796876631@s.whatsapp.net`). É UMA nota por vez — não confundir com `emitir-notas-fiscais` (lote do Asaas). Uso remoto pelo celular (listener WhatsApp) documentado em `18_AUTOMATION_STACK/nfem-joinville/README_EMISSAO_REMOTA.md`.

## Trigger principal (mentorado novo)

Se o mentorado disser "instalar kpa30", "instalar kit", "primeira vez", "comecar a usar o kit" ou qualquer variacao, **acione o wizard imediatamente**: `00_OS/commands/instalar-kpa30.md`. Cobre tudo em 7 etapas (~15-20 min): dependencias, .env, MCPs, Meta CLI, Projects Desktop, onboarding do negocio, primeira tarefa util.

## Inicializacao

1. Leia `00_INDEX.md`.
2. Leia `00_OS/bootstrap.md`.
3. Leia `00_OS/cos.md`.
4. Leia `00_OS/proactivity-policy.md` quando o pedido envolver autonomia.
5. Leia `00_OS/access-preflight.md` quando o pedido envolver cliente real, ferramenta, pasta, LP, WhatsApp, Cowork, automacao ou instalacao.
6. Use o CoS como entry point de qualquer pedido.
7. Nao carregue `04_DIRETRIZES/` inteira. Carregue apenas a diretriz exigida pela task.

## Full-auto

- Se a decisao for reversivel, escolha o caminho mais conservador e registre a premissa em `07_LOGS/decisions.md`.
- Se faltar dado importante mas a task puder avancar com marcador, use `[A PREENCHER]`.
- Pergunte apenas quando houver risco de desperdicio grande, decisao irreversivel, credencial ausente ou ambiguidade que mude a rota.
- Para usuario leigo, prefira rodar preflight no inicio e depois agir com defaults conservadores.
- WhatsApp/Cowork/automacoes podem ser documentados em modo `draft` full-auto; ativacao real, disparo, API write, CRM update, budget ou publicacao exigem confirmacao.

## Contexto

- CoS carrega no maximo: indice, task atual, ledger, context pack do projeto e mapa de modelos.
- Especialista carrega no maximo: contrato da task, context pack, diretriz primaria e gate correspondente.
- Nunca carregue clientes antigos, swipes, outputs ou pastas externas sem pedido explicito.

## Edicao

- Nao alterar pastas externas referenciadas (se existirem no setup local do operador, como `pasta-padrao-services`, kits anteriores ou `GOAT-copy`).
- Entregaveis finais entram em `06_OUTPUTS/`.
- Estado vivo entra em `05_WORKSPACE/`.
- Rastro operacional entra em `07_LOGS/`.
- Templates operacionais ficam em `10_TEMPLATES_OPERACIONAIS/`.
- WhatsApp e Cowork ficam em `12_WHATSAPP_STACK/` e nos arquivos do cliente em `05_WORKSPACE/clientes/<cliente>/whatsapp/`.
- Automacoes de processos ficam em `18_AUTOMATION_STACK/` e nos arquivos do cliente em `05_WORKSPACE/clientes/<cliente>/automacoes/`.
- Squads adaptativos ficam em `13_ADAPTIVE_SQUADS/` e no `squad-manifest.yaml` do cliente.
- Setup de MCPs e conectores externos fica em `20_MCP_SETUP/`.
- Para criar novo agente, skill, task ou diretriz, use `21_BUILDER_KIT/` (Forge).

## Qualidade

- Toda entrega relevante passa por gate antes de ser considerada pronta.
- Gates usam `00_OS/gate-matrix.md` para severidade e escalada.
- Copy sem VOC, mecanismo, prova e awareness identificados fica como rascunho, nao final.
- WhatsApp sem handoff humano, stop rules e limites do bot fica como rascunho, nao final.
- Automacao sem trigger, teste, rollback e handoff humano fica como rascunho, nao final.
- Promessa da LP sem entrega correspondente vira gap de produto.
- Revisao deve devolver problemas especificos e correcoes concretas.
