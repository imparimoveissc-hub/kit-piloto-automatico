# Command — automação incluir imóveis

> Cadastrar imóveis NOVOS no CRM da Impar Imóveis (painel1.imobibrasil.app.br) a partir da fonte oficial da construtora (começando pela Rogga), buscando fotos reais e dados, e preenchendo o formulário de inclusão. Complementa o comando `atualizar apartamentos na planta` (que só atualiza valor de imóvel já cadastrado).

## Triggers

- `automação incluir imóveis`
- `automacao incluir imoveis`
- `incluir imóveis`
- `cadastrar imóveis novos`
- `cadastro automático de imóveis`
- `subir imóvel novo no CRM`

## Acesso (mesmo caminho da automação "atualizar imóveis na planta")

Esta automação **dirige o Chrome logado do usuário via extensão do Claude** (não é script headless). Antes de rodar:

1. Chrome pareado com a extensão do Claude (`list_connected_browsers` deve retornar o navegador).
2. Usuário logado em:
   - `https://vendas.rogga.com.br` (fonte dos empreendimentos)
   - `https://painel1.imobibrasil.app.br/imobiliarias/identificacao.php` (CRM Impar)
3. Se algum site pedir login/código, o **usuário faz manualmente** e avisa. Nunca pedir senha/login/token no chat.

Conhecimento de valores (menor valor residencial sem garagem) e leitura das tabelas Rogga: reaproveitar de `00_OS/commands/atualizar-apartamentos-na-planta.md`.

## Passo 1 — Descobrir imóveis novos (Rogga, Joinville)

1. Abrir `https://vendas.rogga.com.br` → menu esquerdo **Unidades**.
2. Três seletores: **Cidade / Empreendimentos / Torres**. Deixar **Cidade = Joinville**.
3. Listar **todos** os empreendimentos e **excluir os já cadastrados**:

| Já cadastrado | Ref Impar |
|---|---|
| Urban Baviera | AP0094 |
| Urban Azaleia | AP0167 |
| Torres do Glória | AP0202 |
| Polinésia | AP0163 |
| Floratta | AP0162 |

4. Apresentar ao usuário a **lista de empreendimentos novos** e aguardar confirmação antes de escrever no CRM.
5. Depois de Joinville, seguir para as demais cidades.

## Passo 2 — Incluir cada imóvel no CRM Impar

No painel `painel1.imobibrasil.app.br`:

1. **CRM Imóveis → Imóveis: Incluir**.
2. **Adicionar proprietário:** `Matheus Rogga`.
3. **Corretor responsável:** `Jonata`.
4. **Cód. Referência:** `AP0206`, `AP0207`, `AP0208`… em diante. **Nunca repetir** — conferir no CRM se o código já existe antes de usar.
5. **Finalidade:** Venda.
6. **Tipo de Imóvel:** Apartamento na Planta.
7. **Localização:** copiar do site da Rogga.
8. **Valor:** **menor valor da tabela de Vendas**, ignorando garagem/vaga (regra `menor_valor_residencial_sem_garagem`; ver comando de atualização).
9. Preencher **medidas** (área privativa/útil).
10. Preencher **características** conforme cada imóvel (dormitórios, suítes, banheiros, vagas, etc.).
11. **Descrição:** clicar em **Descrição Simples** (gera a descrição automática).
12. Clicar em **Salvar Imóveis**.

## Passo 3 — Imagens (obrigatório marca d'água)

1. Aba **Imagens** → **Selecionar Imagens**.
2. Inserir **apenas fotos reais do imóvel** (baixadas da Rogga). **Nunca inventar imagem.**
3. Clicar no botão azul **Enviar imagens** para concluir o upload.
4. Depois do envio, clicar em **Aplicar Marca d'água em todas as fotos** — **sempre**, sem exceção.

## Passo 4 — Relatório

Ao final, gerar relatório de tudo que foi publicado no CRM para conferência, contendo por imóvel:
- Ref gerada (AP02xx), empreendimento, localização, valor usado (e menor unidade escolhida), medidas, nº de fotos, marca d'água aplicada (sim/não), link do cadastro.

Salvar cópia em `05_WORKSPACE/clientes/impar-imoveis/automacoes/cadastro-imoveis/logs/relatorio-inclusao-YYYY-MM-DD.md`.

## Estado atual (retomar daqui)

- **Status:** pausado no Passo 0 (aguardando Chrome pareado + login nos 2 sites).
- **Nada foi escrito no CRM ainda.**
- Próxima ref a usar: **AP0206** (confirmar no CRM que está livre).
- Plano combinado: recon Joinville → confirmar lista → cadastrar **1 imóvel piloto completo** → validar padrão → seguir os demais → relatório.
- Ferramenta de apoio (coletor de fotos/dados e mapa de campos): `05_WORKSPACE/clientes/impar-imoveis/automacoes/cadastro-imoveis/`.

## Regras de segurança

- Não pedir login/senha/token/código no chat.
- Escrita real no CRM exige confirmação explícita do usuário no turno.
- Nunca inventar foto — só fotos reais do empreendimento.
- Sempre aplicar marca d'água.
- Não usar valor de garagem/vaga/entrada/financiamento/condomínio/parcela como valor principal.
- Registrar log/relatório com rollback (excluir cadastro AP02xx no CRM).
