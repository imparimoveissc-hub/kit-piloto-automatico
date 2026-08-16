# Command — atualizar apartamentos na planta

> Fluxo operacional para atualizar valores de apartamentos na planta da Impar Imoveis no CRM Imobibrasil, usando fonte oficial do empreendimento/construtora e validacao no site publico.

## Triggers

- `atualizar apartamentos na planta`
- `atualizar apartamento na planta`
- `atualizar imoveis na planta`
- `atualizar imóveis na planta`
- `atualizar tabela de apartamentos na planta`

## Objetivo

Atualizar com seguranca os anuncios de apartamentos na planta publicados no site da Impar Imoveis, mantendo consistencia entre:

1. fonte oficial do empreendimento/construtora;
2. site publico da Impar;
3. CRM Imobibrasil;
4. descricao do imovel;
5. valor por m2.

## Modos de Execucao

### Manual

Quando o usuario escrever `atualizar apartamentos na planta`, executar este fluxo no momento da conversa, usando os codigos/links informados ou a fila geral em `05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-apartamentos-na-planta.csv`.

### Automatico

Rodar nos dias `02`, `03`, `15`, `20` e `25` de cada mes para todos os imoveis cadastrados na fila geral, nao apenas Rogga.

Fila geral:

- `05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-apartamentos-na-planta.csv`

Fontes atualmente contempladas:

- Rogga;
- Grupo JM;
- Residencial Maria Laura via Google Docs/Drive;
- proximas construtoras/tabelas adicionadas pelo usuario.

No modo automatico, se houver bloqueio de login, codigo, captcha, fonte ambigua ou divergencia sensivel, gerar relatorio e pedir intervencao humana antes de alterar o CRM.

## Regras de Seguranca

- Nao pedir login, senha, token ou codigo no chat.
- Se o CRM, construtora, Drive ou e-mail pedir login/codigo, o usuario faz a etapa manualmente no navegador e avisa quando estiver logado.
- Nao atualizar CRM se a fonte oficial estiver ambigua ou conflitante.
- Nao usar valor de vaga de garagem, vaga extra, entrada, financiamento, condominio, IPTU, aluguel, TLU ou parcela como valor principal do imovel.
- Atualizacao real no Imobibrasil exige pedido/aprovacao explicita do usuario no turno.
- Em rodada automatica sem credenciais seguras persistentes, a automacao deve comparar e gerar relatorio; a escrita real fica pendente de aprovacao/login humano.
- Depois de salvar, validar no site publico da Impar.
- Registrar log com valor anterior, valor novo, fonte e rollback.

## Entrada Esperada

O usuario pode enviar:

- codigos da Impar, como `AP0154` e `AP0155`;
- links do site publico da Impar;
- link de tabela no Google Drive, Google Docs, PDF, planilha ou site da construtora;
- regra especifica, como `2 dormitorios`, `3 dormitorios` ou `menor valor`.

Se o usuario enviar mais de uma fonte, comparar as fontes. Se houver conflito, parar e registrar como `nao validado`.

## Fluxo

1. Identificar os codigos e links enviados pelo usuario.
2. Abrir a fonte oficial: Rogga, Grupo JM, Google Drive/Docs/PDF, site da construtora ou outra fonte indicada.
3. Ler a tabela e separar por tipologia: dormitorios, suites, coberturas, giardino/garden e outras variacoes.
4. Para cada codigo da Impar, localizar o anuncio publico, preferindo busca por referencia exata: `https://www.imparimoveis.com/imovel/?reftipo=exata&ref=CODIGO`.
5. Confirmar codigo, dormitorios, area util/privativa e valor atual.
6. Definir o valor correto:
   - se o usuario indicou unidade especifica, usar aquela unidade;
   - se pediu menor valor, usar menor unidade residencial valida da tipologia correta;
   - ignorar vagas de garagem e itens nao residenciais.
7. Calcular valor por m2 usando a area privativa/util cadastrada no anuncio/CRM, salvo se o usuario pedir outra regra.
8. Abrir o Imobibrasil em `CRM Imoveis > Imoveis: Listar`.
9. Buscar por `Referencia Exata` e confirmar que existe um unico cadastro.
10. Antes de salvar, conferir codigo de referencia, dormitorios/suites, area privativa/util, valor atual e trecho `Valor do Imovel` na descricao.
11. Atualizar `valor_esperado`, `valor_m2` e trecho `Valor do Imovel R$ ...` na descricao.
12. Salvar o imovel.
13. Reabrir o cadastro e validar os campos.
14. Abrir o site publico da Impar e validar o valor publicado.
15. Registrar log operacional.

## Relatorio Obrigatorio

Toda rodada deste comando deve gerar um relatorio final, mesmo quando:

- nenhum valor mudar;
- houver bloqueio de login ou fonte ambigua;
- a escrita no CRM nao for autorizada;
- apenas parte da fila for validada.

O relatorio deve informar, no minimo:

- data e modo da rodada;
- codigos processados;
- o que mudou de fato;
- o que nao mudou;
- o que ficou bloqueado;
- valores anteriores e novos quando houver alteracao;
- valor m2 anterior e novo quando houver alteracao;
- descricao do imovel: atualizada ou nao;
- validacao publica: OK, pendente ou bloqueada;
- proximo passo por item.

Padrao de saida:

- `06_OUTPUTS/YYYY-MM-DD_atualizar-apartamentos-na-planta-impar-imoveis/relatorio.md`
- `07_LOGS/imobibrasil-updates-YYYY-MM-DD.md`

## Padrao de Log

Registrar em `07_LOGS/imobibrasil-updates-YYYY-MM-DD.md`:

```markdown
## Atualizacao apartamentos na planta — [empreendimento]

- Fonte usada:
- Codigos atualizados:
- Valor anterior:
- Valor novo:
- Valor m2 anterior:
- Valor m2 novo:
- Descricao atualizada: sim/nao
- Validacao publica: OK/pendente
- Rollback:
```

## Exemplo Executado

Em 2026-07-05, comando usado para `Residencial Maria Laura`:

- `AP0155`: 2 dormitorios, valor atualizado para `R$ 398.900,00`, valor m2 `R$ 7.978,00`.
- `AP0154`: 3 dormitorios, valor atualizado para `R$ 539.400,00`, valor m2 `R$ 8.990,00`.

Fonte correta: Google Docs `Tabela Preco Residencial Maria Laura.docx`.

Fonte descartada: PDF `Tabela Golden Beach Julho 2026.pdf`, por ser outro empreendimento.
