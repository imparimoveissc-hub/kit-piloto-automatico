# Login Automatico Rogga

Status: draft seguro  
Objetivo: automatizar o acesso a Rogga sem expor senha/codigo no chat.

## Estrategia Recomendada

Usar 3 camadas:

1. **Sessao persistente no navegador interno**
   - Manter o login da Rogga salvo quando possivel.
   - A automacao tenta acessar direto as URLs de unidades/tabelas.
   - Se ja estiver logado, segue sem pedir nada.

2. **Login assistido quando a sessao expirar**
   - Se a Rogga pedir login, a automacao para.
   - Jonata digita usuario/senha diretamente no site.
   - Senha nunca entra no chat nem em arquivo do kit.

3. **Leitura automatica do codigo por e-mail**
   - Preferencia: acesso autorizado ao Outlook/Microsoft por OAuth ou Microsoft Graph.
   - Permissao minima: ler e-mails recentes apenas o suficiente para localizar o codigo da Rogga.
   - Filtrar por remetente/assunto da Rogga e janela curta de tempo.
   - Extrair apenas o codigo, sem salvar conteudo completo do e-mail.

## O Que Evitar

- Nao pedir senha no chat.
- Nao salvar senha em arquivo comum.
- Nao automatizar Outlook pela tela como caminho principal.
- Nao ler caixa inteira sem filtro.
- Nao usar codigo antigo.
- Nao continuar se houver captcha, alerta de seguranca ou erro de login.

## Fluxo Automatico

1. Abrir URL da Rogga.
2. Verificar se ja esta logado.
3. Se logado:
   - seguir para leitura das tabelas.
4. Se pediu login:
   - usar credencial segura somente se estiver configurada em ambiente protegido;
   - caso contrario, pedir login assistido.
5. Se pediu codigo:
   - aguardar novo e-mail da Rogga;
   - ler e-mail por conector seguro;
   - extrair codigo;
   - inserir codigo na Rogga.
6. Confirmar que a pagina de unidades/tabelas abriu.
7. Rodar comparacao.

## Outlook no Mac

O fato de o Outlook estar instalado ajuda, mas o caminho mais confiavel nao e controlar o app visualmente.

Ordem recomendada:

1. **Microsoft Graph/OAuth**: melhor para automacao recorrente.
2. **IMAP autorizado**: alternativa se a conta permitir.
3. **Outlook app visual no Mac**: apenas fallback manual/assistido, porque muda com janela, foco, layout e notificacoes.

## Dados Necessarios Para Ativar

- E-mail que recebe o codigo da Rogga: `[A PREENCHER]`
- Padrao do remetente da Rogga: `[A PREENCHER]`
- Padrao do assunto do e-mail de codigo: `[A PREENCHER]`
- Tempo maximo de espera pelo codigo: `5 minutos`
- Janela de busca: e-mails recebidos apos o inicio do login
- Acao se codigo nao chegar: bloquear execucao e avisar Jonata

## Regra de Seguranca

Enquanto o acesso ao e-mail nao estiver configurado por OAuth/IMAP seguro, a automacao pode rodar com:

- sessao ja logada; ou
- login assistido; ou
- codigo digitado por Jonata diretamente no site.

Nao automatizar atualizacao no Imobibrasil ate o login e a leitura de codigo estarem estaveis.
