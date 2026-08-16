# Automacao 100% — Rogga x Impar x Imobibrasil

Status: draft seguro  
Objetivo: preparar a rotina para varios imoveis, com comparacao automatica e atualizacao controlada.

## O Que Pode Ficar 100% Automatico Agora

1. Abrir os links Rogga de cada imovel.
2. Ler todas as fases/tabelas informadas.
3. Ignorar vaga extra, vaga de garagem ou item apenas garagem.
4. Identificar o menor valor residencial valido.
5. Abrir o site publico da Impar.
6. Comparar valor publicado x menor valor Rogga.
7. Gerar relatorio por imovel.
8. Gerar resumo consolidado com recomendacao.

Com login automatico:

- usar sessao persistente da Rogga quando ela ainda estiver valida;
- se a sessao expirar, autenticar por fluxo seguro;
- ler o codigo de validacao por Outlook/Microsoft somente via OAuth/Graph ou IMAP autorizado.

## O Que Fica Travado Ate Aprovacao

1. Abrir o Imobibrasil para editar.
2. Salvar valor novo.
3. Publicar alteracao.
4. Rodar atualizacao em lote.

Motivo: CRM update e publicacao real sao escrita em sistema comercial. A automacao pode preparar tudo, mas a primeira ativacao precisa de aprovacao humana e rollback testado.

## Login Rogga

Detalhe operacional em:

`18_AUTOMATION_STACK/impar-atualizacao-rogga-imobibrasil/login-automatico-rogga.md`

## Formato da Lista de Imoveis

Usar uma planilha/CSV baseada em:

`18_AUTOMATION_STACK/impar-atualizacao-rogga-imobibrasil/imoveis-mapa.template.csv`

Fila atual da Impar/Rogga:

`05_WORKSPACE/clientes/impar-imoveis/automacoes/imoveis-rogga.csv`

Campos:

- `codigo_imobibrasil`: codigo usado para localizar o imovel no CRM.
- `codigo_site_impar`: codigo publico, quando existir.
- `nome_imovel`: nome interno para relatorio.
- `url_site_impar`: link publico que o cliente ve.
- `rogga_unidades_urls`: um ou mais links de unidades/fases da Rogga, separados por ` | `.
- `rogga_tabela_urls`: um ou mais links de tabela de vendas, separados por ` | `.
- `regra_preco`: padrao `menor_valor_residencial_sem_garagem`.
- `status_automacao`: `comparar_sem_alterar`, `pronto_para_aprovacao` ou `autorizado_para_atualizar`.
- `observacoes`: qualquer regra especifica do imovel.

## Criterio Para Atualizar Futuramente

So permitir atualizacao no Imobibrasil quando todos forem verdadeiros:

- pelo menos 3 dry-runs sem erro;
- login da Rogga esta estavel no navegador interno;
- acesso ao codigo por e-mail esta resolvido de forma segura;
- mapa de imoveis esta preenchido;
- relatorio mostra claramente valor anterior e valor novo;
- existe snapshot antes/depois;
- Jonata autorizou explicitamente atualizar CRM.

## Rotina Mensal Recomendada

Rodar nos dias 02, 03, 15, 20 e 25.

Primeiro modo:

`comparar_sem_alterar`

Depois de aprovado:

`atualizar_com_confirmacao`

Somente depois de validado:

`atualizar_automatico_com_log_e_rollback`
