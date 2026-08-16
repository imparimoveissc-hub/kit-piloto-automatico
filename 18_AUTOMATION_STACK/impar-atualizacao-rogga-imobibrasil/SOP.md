# SOP — Atualizacao de tabelas Rogga no Imobibrasil

Status: draft  
Owner: Jonata / Impar Imoveis  
Ultima revisao: 2026-07-05

## Objetivo

Atualizar, nos dias 02, 03, 15, 20 e 25 de cada mes, os valores/tabelas dos imoveis da Rogga publicados no site da Impar via CRM Imobibrasil.

## Fonte Recomendada

Use a Rogga como fonte unica/oficial.

Motivo: a Rogga deve refletir a tabela oficial mais recente. Se a Rogga falhar, a rotina deve parar e pedir intervencao humana em vez de usar fonte alternativa.

## Regra de Menor Valor

Sempre procurar a **unidade residencial mais em conta** na Rogga.

Quando o empreendimento tiver varias fases ou tabelas, como `Urban Baviera primeira fase`, `Urban Baviera segunda fase` e `Urban Baviera terceira fase`, verificar todas elas e comparar o menor valor residencial valido.

Nao usar valores de garagem. Ignorar qualquer item descrito como:

- `vaga extra`;
- `vaga de garagem`;
- apenas garagem ou item equivalente.

Se houver duvida se a linha e unidade residencial ou garagem, marcar como `nao validado` e pedir revisao humana.

## Entradas Necessarias

- Credencial Rogga em ambiente seguro, nao no chat.
- Acesso autorizado ao e-mail que recebe o codigo Rogga.
- Credencial Imobibrasil em ambiente seguro, nao no chat.
- Lista de imoveis com:
  - codigo do imovel no Imobibrasil;
  - identificador do imovel na Rogga;
  - nome do empreendimento;
  - URL publica do imovel no site da Impar, se existir.

## Passo a Passo

1. Abrir a Rogga em `https://vendas.rogga.com.br`.
2. Entrar com credencial segura.
3. Solicitar codigo de acesso por e-mail.
4. Abrir o e-mail autorizado, localizar o codigo mais recente e validar o acesso.
5. Para cada imovel mapeado, capturar tabela, valores, data de vigencia, status e observacoes.
6. Se houver mais de uma fase/tabela, repetir a captura em todas as fases/tabelas do empreendimento.
7. Remover da comparacao itens de garagem, vaga extra ou vaga de garagem.
8. Identificar a menor unidade residencial valida.
9. Salvar um snapshot da Rogga para auditoria.
10. Abrir a pagina publica do imovel no site da Impar.
11. Comparar o menor valor residencial valido da Rogga com o valor publicado no site publico.
12. Marcar divergencias e campos nao validados.
13. Nao abrir o Imobibrasil no piloto inicial.
14. Gerar relatorio de diferencas.
15. Pedir aprovacao humana antes de salvar qualquer alteracao.
16. Em uma etapa posterior, apos aprovacao, abrir o Imobibrasil e alterar somente os campos aprovados.
17. Validar no site publico da Impar se os valores ficaram corretos.
18. Registrar log com data, imovel, valor anterior, valor novo, origem da informacao e aprovador.

## Decisoes Humanas

| Momento | Quem aprova | Criterio |
|---|---|---|
| Antes de salvar no Imobibrasil | Jonata | Diferenca de valor/tabela revisada e autorizada |
| Rogga indisponivel | Jonata | Decide quando tentar novamente |
| Divergencia Rogga x site publico | Jonata | Autoriza ou nao etapa posterior no CRM |
| Linha ambigua entre unidade e garagem | Jonata | Confirma se entra ou nao no menor valor |
| Campo nao previsto no CRM | Jonata | Decide se atualiza manualmente ou ajusta o processo |

## Automacoes Sugeridas

| Etapa | Modo | Ferramenta | Risco |
|---|---|---|---|
| Agendamento dias 02, 03, 15, 20 e 25 | draft/pausado | Codex automations, n8n ou Make | baixo |
| Login Rogga e solicitacao de codigo | assistido | Browser automation | medio |
| Leitura do codigo por e-mail | assistido | Gmail/OAuth ou IMAP | alto |
| Captura de todas as fases/tabelas Rogga | automatizado | Browser automation + CSV | medio |
| Exclusao de vagas de garagem | automatizado | Regra de filtro + evidencia | baixo |
| Comparacao com site publico da Impar | automatizado | Browser automation | baixo |
| Atualizacao no Imobibrasil | bloqueado ate aprovacao | Browser automation | alto |
| Validacao no site publico | automatizado | Browser automation | baixo |

## Teste

Entrada de teste: Residencial Baviera com URL publica da Impar e links da Rogga.

Resultado esperado: relatorio de diferencas gerado sem alterar o CRM.

Criterio de sucesso:

- Acesso Rogga validado.
- Codigo por e-mail lido corretamente.
- Todas as fases/tabelas relevantes verificadas.
- Vagas de garagem ignoradas.
- Menor unidade residencial valida identificada.
- Pagina publica correta encontrada no site da Impar.
- Diferenca apontada com clareza.
- CRM nao acessado no piloto inicial.
- Nenhuma alteracao publicada sem aprovacao.

## Rollback

Como parar: pausar o agendamento e encerrar a sessao do navegador.

Como desfazer: usar o log da ultima execucao para recolocar os valores anteriores no Imobibrasil manualmente.

## Dados Pendentes

- Credenciais Rogga: `[A PREENCHER EM AMBIENTE SEGURO]`
- E-mail que recebe codigo Rogga: `[A PREENCHER]`
- Credenciais Imobibrasil: `[A PREENCHER EM AMBIENTE SEGURO]`
- Lista de codigos dos imoveis: `[A PREENCHER]`
- Links de Drive por imovel: `nao aplicavel`
- Navegador recomendado: `navegador interno do Codex com login assistido`
- Horario preferido da execucao: `09:00` assumido como padrao conservador.
