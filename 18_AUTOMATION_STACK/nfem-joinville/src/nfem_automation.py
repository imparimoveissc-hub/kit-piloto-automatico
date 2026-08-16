"""
Automação Playwright para emissão de NF-em no site da Prefeitura de Joinville.

Fluxo:
  1. Login
  2. Navegar para emissão de NF
  3. Preencher dados do tomador
  4. Preencher dados do serviço
  5. Revisar
  6. Emitir (ou abortar em dry_run)
  7. Baixar PDF
"""

import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Page, BrowserContext, TimeoutError as PlaywrightTimeout

from src.config import (
    NFEM_USER,
    NFEM_PASSWORD,
    NFEM_URL,
    NATUREZA_OPERACAO,
    CODIGO_SERVICO,
    ITEM_LISTA_SERVICO,
    ALIQUOTA_ISS,
    MUNICIPIO_INCIDENCIA,
    ISS_RETIDO,
    DRY_RUN,
    BROWSER_HEADLESS,
)
from src.logger import log

TIMEOUT = 30_000  # 30s


class NfemError(Exception):
    pass


class SessaoExpirada(NfemError):
    """Não há sessão válida e o modo desassistido não resolve captcha."""
    pass


class NfemAutomation:
    def __init__(
        self,
        headless: bool = BROWSER_HEADLESS,
        dry_run: bool = DRY_RUN,
        storage_state: Optional[str] = None,
        unattended: bool = False,
    ):
        self.headless = headless
        self.dry_run = dry_run
        # storage_state: caminho do arquivo de cookies da sessão "quente". Se
        # existir, é carregado para pular o captcha; ao fazer login manual, é
        # regravado. unattended=True significa "sem humano pra digitar captcha":
        # se a sessão estiver expirada, aborta com SessaoExpirada em vez de travar.
        self.storage_state = str(storage_state) if storage_state else None
        self.unattended = unattended
        self._playwright = None
        self._browser = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def __aenter__(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context_kwargs = dict(
            accept_downloads=True,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )
        if self.storage_state and Path(self.storage_state).exists():
            context_kwargs["storage_state"] = self.storage_state
            log.info("Carregando sessão salva de %s", self.storage_state)
        self._context = await self._browser.new_context(**context_kwargs)
        self._page = await self._context.new_page()
        return self

    async def __aexit__(self, *_):
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    # ── helpers ────────────────────────────────────────────────────────────────

    async def _screenshot(self, nome: str) -> None:
        """Salva screenshot de debug."""
        try:
            from src.config import LOGS_DIR
            path = LOGS_DIR / f"{nome}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await self._page.screenshot(path=str(path), full_page=True)
            log.debug("Screenshot salvo: %s", path)
        except Exception as e:
            log.debug("Erro ao salvar screenshot: %s", e)

    async def _preencher(self, selector: str, valor: str, limpar: bool = True) -> None:
        el = self._page.locator(selector).first
        await el.wait_for(state="visible", timeout=TIMEOUT)
        if limpar:
            await el.clear()
        await el.fill(valor)

    async def _selecionar(self, selector: str, valor: str) -> None:
        el = self._page.locator(selector).first
        await el.wait_for(state="visible", timeout=TIMEOUT)
        await el.select_option(value=valor)

    async def _clicar(self, selector: str) -> None:
        el = self._page.locator(selector).first
        await el.wait_for(state="visible", timeout=TIMEOUT)
        await el.click()

    # ── login ─────────────────────────────────────────────────────────────────

    async def _ja_autenticado(self) -> bool:
        """True se a página atual já está logada (sessão restaurada dos cookies)."""
        if await self._page.locator("input[name='cpf']").count() > 0:
            return False
        try:
            conteudo = await self._page.inner_text("body")
        except Exception:
            return False
        return any(m in conteudo for m in ("Serviços", "Sair", "Emitir NF-em"))

    async def _salvar_sessao(self) -> None:
        """Persiste os cookies da sessão logada para reuso desassistido."""
        if not self.storage_state:
            return
        try:
            Path(self.storage_state).parent.mkdir(parents=True, exist_ok=True)
            await self._context.storage_state(path=self.storage_state)
            log.info("Sessão salva em %s", self.storage_state)
        except Exception as e:
            log.warning("Não consegui salvar a sessão: %s", e)

    async def login(self) -> None:
        log.info("Acessando NF-em Joinville...")
        await self._page.goto(NFEM_URL, wait_until="networkidle", timeout=60_000)
        await self._screenshot("01_home")

        # Sessão "quente": se os cookies restaurados ainda valem, pula o login
        # (e o captcha) por completo. É o que permite emitir remoto/desassistido.
        if await self._ja_autenticado():
            log.info("Sessão restaurada dos cookies — login não necessário")
            return

        # Sem sessão válida e sem humano para o captcha: aborta explicitamente
        # para o listener avisar que é preciso refazer o login manual no Mac.
        if self.unattended:
            raise SessaoExpirada(
                "Sessão do NF-em expirada e não há como resolver o captcha sem um humano. "
                "Rode 'python -m src.cli login-manual' no Mac para renovar a sessão."
            )

        # Preenche usuário e senha automaticamente — o captcha (campo "COD")
        # muda a cada carregamento da página e não pode ser automatizado de
        # forma confiável, então o login fica semi-automático: a automação
        # prepara o formulário e pausa esperando um humano digitar o captcha
        # e clicar em "Login" (ou completar o login por certificado digital).
        try:
            await self._preencher("input[name='cpf']", NFEM_USER)
            await self._preencher("input[name='senha']", NFEM_PASSWORD)
        except PlaywrightTimeout:
            await self._screenshot("01_login_preenchimento_falhou")
            raise NfemError("Não foi possível preencher usuário/senha. Verifique os seletores do site.")

        if self.headless:
            raise NfemError(
                "O site exige captcha no login — não é possível rodar headless. "
                "Rode com BROWSER_HEADLESS=false para completar o login manualmente."
            )

        log.warning(
            "AÇÃO NECESSÁRIA: digite o código do captcha (campo 'COD') na janela do "
            "navegador e clique em Login. Aguardando você concluir (até 5 minutos)..."
        )
        await self._screenshot("01b_aguardando_captcha")

        # Aguarda o formulário de login (campo cpf) sair do DOM — sinal de que a
        # página recarregou após o envio, dando tempo generoso para o humano
        # digitar o captcha e clicar em Login.
        try:
            await self._page.locator("input[name='cpf']").wait_for(
                state="detached",
                timeout=300_000,  # 5 minutos
            )
        except PlaywrightTimeout:
            await self._screenshot("01c_captcha_timeout")
            raise NfemError(
                "Login não foi concluído em 5 minutos. A automação foi cancelada — "
                "rode novamente quando estiver pronto para digitar o captcha."
            )

        await self._page.wait_for_load_state("networkidle", timeout=30_000)
        await self._screenshot("02_pos_login")

        # Verifica se login foi bem-sucedido (sem mensagem de erro)
        conteudo = await self._page.content()
        if any(p in conteudo.lower() for p in ["senha incorreta", "login inválido", "acesso negado", "usuário não encontrado", "código inválido"]):
            raise NfemError("Falha no login: credenciais ou captcha inválidos")

        log.info("Login realizado com sucesso")
        # Salva a sessão recém-criada para os próximos disparos remotos pularem o captcha.
        await self._salvar_sessao()

    # ── navegar para emissão ──────────────────────────────────────────────────

    async def _navegar_emissao(self) -> None:
        """Navega até o formulário de emissão de nova NF (menu Serviços > Emitir NF-em)."""
        try:
            await self._page.click("a:has-text('Serviços')")
            await self._page.click("a:has-text('Emitir NF-em')")
            await self._page.wait_for_load_state("networkidle", timeout=30_000)
        except PlaywrightTimeout:
            await self._screenshot("03_nav_falhou")
            raise NfemError(
                "Não foi possível clicar em 'Emitir NF-em' no menu Serviços. "
                "O site pode ter mudado a estrutura do menu."
            )

        conteudo = await self._page.content()
        if "não foi possível acessar a página solicitada" in conteudo.lower():
            await self._screenshot("03_nav_falhou")
            raise NfemError(
                "Página de emissão retornou erro após clicar no menu. "
                "Verifique se o link 'Emitir NF-em' ainda existe no menu Serviços."
            )

        await self._screenshot("03_emissao_formulario")
        log.info("Navegou para o formulário de emissão")

    # ── preencher formulário ──────────────────────────────────────────────────

    async def _preencher_tomador(self, dados: dict) -> None:
        """
        Informa o CPF/CNPJ do tomador na tela inicial de emissão e clica em
        'Lançar'. Se o tomador já estiver cadastrado no NF-em, o sistema
        preenche nome e endereço automaticamente (confirmado em teste real).
        """
        log.debug("Informando CPF/CNPJ do tomador...")
        cpf_cnpj_limpo = re.sub(r"\D", "", dados["cpf_cnpj"])

        await self._preencher("#cpf", cpf_cnpj_limpo)
        await self._clicar("input[value='Lançar']")
        await self._page.wait_for_load_state("networkidle", timeout=15_000)
        await self._screenshot("04_pos_lancar")

        # Confirma se o tomador foi reconhecido pelo CPF/CNPJ (cadastro existente)
        conteudo = await self._page.inner_text("body")
        if "Tomador:" not in conteudo:
            raise NfemError(
                f"Tomador com CPF/CNPJ {dados['cpf_cnpj']} não está cadastrado no NF-em. "
                "Cadastre-o manualmente em Serviços > Configurações > Clientes (Emissão NF-em) "
                "antes de emitir a nota, ou complete o cadastro na aba 'Tomador' do formulário."
            )

        log.info("Tomador reconhecido pelo cadastro existente no NF-em")

        # Na emissão manual só temos o CPF/CNPJ — o nome do tomador (usado para
        # nomear o PDF) vem do próprio cadastro do NF-em, exibido como "Tomador:
        # NOME" na tela. Só preenche se ainda não veio nos dados (fluxo em lote
        # já traz nome_tomador de clientes.json).
        if not dados.get("nome_tomador"):
            m = re.search(r"Tomador:\s*(.+)", conteudo)
            if m:
                dados["nome_tomador"] = m.group(1).splitlines()[0].strip()

        # Alguns tomadores têm o cadastro incompleto no NF-em (ex: CEP em
        # branco), o que bloqueia a emissão sem aviso claro. Se clientes.json
        # tiver um endereço de reforço (cep_tomador etc.), completa os campos
        # vazios na aba "Tomador" antes de prosseguir.
        if dados.get("cep_tomador"):
            await self._completar_endereco_tomador(dados)

    async def _completar_endereco_tomador(self, dados: dict) -> None:
        """
        Preenche CEP/endereço do tomador na aba 'Tomador' com o endereço de
        reforço cadastrado em clientes.json. Sempre sobrescreve — o endereço
        já presente no NF-em pode estar errado/desatualizado (confirmado em
        caso real), não só vazio.
        """
        await self._clicar("a:has-text('Tomador')")
        await asyncio.sleep(0.5)

        log.warning("Sobrescrevendo endereço do tomador com dado de reforço de clientes.json")
        cep_limpo = re.sub(r"\D", "", dados["cep_tomador"])
        await self._preencher("#cep", cep_limpo)

        if dados.get("endereco_tomador"):
            await self._preencher("#logradouro", dados["endereco_tomador"])
        if dados.get("numero_tomador"):
            await self._preencher("#numero", dados["numero_tomador"])
        if dados.get("bairro_tomador"):
            await self._preencher("#bairro", dados["bairro_tomador"])
        if dados.get("complemento_tomador"):
            await self._preencher("#complemento", dados["complemento_tomador"])

        await self._screenshot("04b_endereco_tomador_completado")
        await self._clicar("a:has-text('Geral')")
        await asyncio.sleep(0.5)

    async def _preencher_servico(self, dados: dict) -> None:
        log.debug("Preenchendo dados do serviço (aba Geral)...")

        # Natureza e item de serviço: por padrão vêm das constantes de config
        # (fluxo em lote do Asaas), mas cada nota pode sobrescrever — usado pela
        # emissão manual (nota de venda usa item 1005, aluguel usa 1712).
        natureza = dados.get("natureza_operacao") or NATUREZA_OPERACAO
        codigo_servico = dados.get("codigo_servico") or CODIGO_SERVICO

        # Natureza da operação: 107 — digitar código + Tab dispara busca AJAX
        # que preenche a descrição automaticamente (confirmado em teste real)
        await self._preencher("#CST_CODIGO", natureza)
        await self._page.keyboard.press("Tab")
        await asyncio.sleep(1.5)

        # Item da lista de serviços — mesmo padrão de busca AJAX
        await self._preencher("#ATV_CODIGO", codigo_servico)
        await self._page.keyboard.press("Tab")
        await asyncio.sleep(1.5)

        # Confirma que as descrições foram carregadas pela busca AJAX
        cst_nome = await self._page.input_value("#CST_NOME")
        atv_desc = await self._page.input_value("#ATV_DESCRICAO")
        if not cst_nome or not atv_desc:
            await self._screenshot("05_codigos_nao_resolvidos")
            raise NfemError(
                f"Natureza da operação ({natureza}) ou item de serviço "
                f"({codigo_servico}) não foram reconhecidos pelo site. Verifique os códigos."
            )
        log.debug("Natureza: %s | Item: %s", cst_nome, atv_desc)

        # Descrição do serviço
        await self._preencher("#NRI_DESCSERVICO", dados["descricao_servico"])

        # Valor do serviço (formato brasileiro: vírgula decimal)
        valor_str = f"{dados['valor_servico']:.2f}".replace(".", ",")
        await self._preencher("#nri_vlrtotal", valor_str)

        # Alíquota ISS: 5%
        aliquota_str = f"{ALIQUOTA_ISS:.2f}".replace(".", ",")
        await self._preencher("#nri_aliqiss", aliquota_str)

        await self._page.keyboard.press("Tab")
        await asyncio.sleep(1.5)
        await self._screenshot("05_servico_preenchido")

    # ── emitir ────────────────────────────────────────────────────────────────

    async def _clicar_emitir(self) -> None:
        if self.dry_run:
            log.warning(
                "DRY RUN ativo — clicando em 'Visualizar prévia' (não emite a nota de verdade)."
            )
            await self._clicar("input[value='Visualizar prévia']")
            await asyncio.sleep(2)
            await self._screenshot("06_dry_run_previa")
            return

        await self._clicar("input[value='Emitir NFS-e']")
        await self._page.wait_for_load_state("networkidle", timeout=30_000)
        await self._screenshot("06_pos_emissao")
        log.info("NF emitida com sucesso")

    # ── número da nota + PDF oficial ───────────────────────────────────────────

    async def _obter_numero_e_pdf(self) -> tuple[str, bytes]:
        """
        Após clicar em 'Emitir NFS-e', a página recarrega na tela de Consulta
        já mostrando a nota recém-emitida na primeira linha da lista, com um
        link no formato "NUMERO / SÉRIE" (ex: "277 / A1") que abre o PDF
        oficial em nova aba (servido por tributario-file-server). Esse link
        fica dentro de um menu suspenso (não visível por padrão), por isso o
        clique é feito via JavaScript em vez de Locator.click().

        Retorna (numero_nota, pdf_bytes).
        """
        if self.dry_run:
            log.warning("DRY RUN — retornando número/PDF placeholder")
            return "DRY-RUN", b"%PDF-1.4 DRY RUN PLACEHOLDER"

        # Seletor por padrão de URL (mais robusto que depender de uma classe
        # CSS específica, que pode não estar presente em todo carregamento).
        link_nota = self._page.locator("a[href*='NFES?']").first
        try:
            await link_nota.wait_for(state="attached", timeout=20_000)
        except PlaywrightTimeout:
            # Fallback: clica em Pesquisar para forçar o carregamento da lista
            try:
                await self._page.click("input[value='Pesquisar']", timeout=5_000)
                await self._page.wait_for_load_state("networkidle", timeout=15_000)
                await link_nota.wait_for(state="attached", timeout=15_000)
            except Exception:
                await self._screenshot("07_link_nota_nao_encontrado")
                raise NfemError(
                    "Não encontrei o link da nota na tela pós-emissão. "
                    "A nota pode ter sido emitida mesmo assim — verifique manualmente "
                    "em Serviços > Consulta NF-em antes de tentar emitir de novo."
                )

        texto_link = await link_nota.inner_text()
        match = re.search(r"(\d+)\s*/", texto_link)
        numero = match.group(1).lstrip("0") or "0" if match else "N/D"

        try:
            async with self._context.expect_page(timeout=15_000) as nova_pagina_info:
                await link_nota.evaluate("el => el.click()")
            nova_pagina = await nova_pagina_info.value
            await nova_pagina.wait_for_load_state("networkidle", timeout=20_000)

            resposta = await self._context.request.get(nova_pagina.url)
            pdf_bytes = await resposta.body()
            await nova_pagina.close()
        except Exception as e:
            raise NfemError(
                f"Nota {numero} foi emitida, mas não consegui baixar o PDF oficial: {e}. "
                "Baixe manualmente em Serviços > Consulta NF-em."
            )

        if pdf_bytes[:4] != b"%PDF":
            raise NfemError(
                f"Nota {numero} foi emitida, mas o arquivo baixado não é um PDF válido."
            )

        return numero, pdf_bytes

    # ── método principal ──────────────────────────────────────────────────────

    async def emitir(self, dados: dict) -> tuple[bytes, str]:
        """
        Executa o fluxo completo de emissão.
        Retorna (pdf_bytes, numero_nota).
        """
        await self.login()
        await self._navegar_emissao()
        await self._preencher_tomador(dados)
        await self._preencher_servico(dados)
        await self._clicar_emitir()
        numero, pdf = await self._obter_numero_e_pdf()
        return pdf, numero

    async def emitir_lote(self, lista_dados: list[dict]) -> list[dict]:
        """
        Emite várias notas em uma única sessão (um único login/captcha).

        Retorna uma lista alinhada com lista_dados, cada item:
          {"sucesso": True, "numero_nota": str, "pdf_bytes": bytes}
          ou
          {"sucesso": False, "erro": str}

        Uma falha em um item não interrompe os demais — cada nota é
        independente, então erro em uma não deve bloquear o resto do lote.
        """
        await self.login()

        resultados = []
        for i, dados in enumerate(lista_dados):
            log.info(
                "Emitindo nota %d/%d | tomador=%s | valor=%.2f",
                i + 1,
                len(lista_dados),
                dados.get("nome_tomador"),
                dados.get("valor_servico", 0),
            )
            try:
                await self._navegar_emissao()
                await self._preencher_tomador(dados)
                await self._preencher_servico(dados)
                await self._clicar_emitir()
                numero, pdf = await self._obter_numero_e_pdf()
                resultados.append({"sucesso": True, "numero_nota": numero, "pdf_bytes": pdf})
                log.info("Nota %d/%d emitida: número %s", i + 1, len(lista_dados), numero)
            except Exception as e:
                log.error("Falha na nota %d/%d (%s): %s", i + 1, len(lista_dados), dados.get("nome_tomador"), e)
                resultados.append({"sucesso": False, "erro": str(e)})
                await self._screenshot(f"lote_erro_item_{i+1}")

        return resultados


async def emitir_nota(dados: dict) -> tuple[bytes, str]:
    """Função de conveniência para uso externo (emissão única)."""
    async with NfemAutomation() as nfem:
        return await nfem.emitir(dados)


async def emitir_notas_em_lote(lista_dados: list[dict]) -> list[dict]:
    """Função de conveniência para uso externo (emissão em lote, um único login)."""
    async with NfemAutomation() as nfem:
        return await nfem.emitir_lote(lista_dados)
