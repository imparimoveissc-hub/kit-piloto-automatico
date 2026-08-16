# Piloto Seguro — Residencial Baviera

Status: draft  
Objetivo: comparar Rogga x site publico da Impar, sem CRM e sem alteracao real.

## Links

- Site publico Impar: `https://www.imparimoveis.com/imovel/3824292/apartamento-na-planta-venda-joinville-sc-itaum`
- Rogga unidades: `https://vendas.rogga.com.br/unidades?city_id=Joinville&building_id=412&tower_id=&show=table`
- Rogga tabela de vendas: `https://vendas.rogga.com.br/precos/412/410/`

## Fluxo Mais Seguro

1. Abrir a Rogga em navegador controlado e autenticado.
2. Se pedir login/codigo/captcha, parar e pedir intervencao humana.
3. Verificar todas as fases/tabelas disponiveis do Baviera na Rogga.
4. Ignorar itens descritos como `vaga extra`, `vaga de garagem` ou apenas garagem.
5. Identificar a menor unidade residencial valida.
6. Abrir o site publico da Impar.
7. Capturar os dados visiveis do anuncio Baviera.
8. Comparar o menor valor residencial valido da Rogga com o valor publicado.
9. Marcar campos ausentes ou ambiguos como `nao validado`.
10. Entregar relatorio.

## Fora de Escopo Neste Piloto

- Abrir Imobibrasil.
- Editar cadastro.
- Salvar alteracoes.
- Publicar qualquer mudanca.
- Usar Google Drive como fonte.
- Usar valor de vaga de garagem como preco do imovel.

## Criterio de Sucesso

- Rogga lida com sucesso.
- Todas as fases/tabelas relevantes do Baviera verificadas.
- Vagas de garagem excluidas da comparacao.
- Menor unidade residencial valida identificada.
- Site publico lido com sucesso.
- Relatorio mostra divergencias sem inferir dados faltantes.
- Nenhuma acao de escrita e executada.
