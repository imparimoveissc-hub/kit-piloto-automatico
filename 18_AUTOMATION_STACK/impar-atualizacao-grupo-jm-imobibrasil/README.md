# Automacao — Grupo JM x Impar x Imobibrasil

Status: draft  
Objetivo: atualizar os imoveis da Impar que dependem de tabelas/valores do Grupo JM.

## Fonte Preferida

Primeiro tentar pelo site do Grupo JM.

Fallback: planilha, se o site nao permitir leitura confiavel ou exigir dado que nao esteja disponivel.

## Regra Base

- Ler a fonte oficial do Grupo JM.
- Identificar o menor valor de unidade residencial valida.
- Ignorar vaga extra, vaga de garagem ou item apenas garagem.
- Comparar com o site publico da Impar.
- Gerar relatorio antes de qualquer atualizacao.
- Abrir Imobibrasil somente apos aprovacao humana.

## Lista de Imoveis

Fila inicial:

`05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-grupo-jm.csv`

Campos:

- `codigo_imobibrasil`: codigo interno usado no CRM.
- `codigo_site_impar`: codigo publico, exemplo `AP0...`.
- `nome_imovel`: nome do empreendimento.
- `url_site_impar`: link publico da Impar.
- `fonte_jm_tipo`: `site` ou `planilha`.
- `fonte_jm_urls`: link do site ou planilha do Grupo JM.
- `regra_preco`: regra de menor valor.
- `status_automacao`: `comparar_sem_alterar`, `pronto_para_aprovacao`, `atualizado_com_aprovacao`.
- `observacoes`: regra especifica do empreendimento.

## Proximo Passo

Preencher pelo menos 1 imovel piloto com:

- link publico da Impar;
- link correspondente no site do Grupo JM;
- se houver, informacao de fases/tabelas/blocos.
