"""
Automação Playwright para emissão de NF-e de serviço (NFS-e) no Portal Nacional.

URL: https://www.nfse.gov.br/EmissorNacional

Fluxo:
  1. Login (Gov.br, usuário/senha ou certificado digital)
  2. Navegar para emissão de NF-e
  3. Preencher dados do tomador
  4. Preencher dados do serviço
  5. Revisar
  6. Emitir (ou abortar em dry_run)
  7. Baixar PDF

NOTA: Este módulo é uma adaptação do nfem_automation.py (Joinville).
Os seletores CSS precisam ser validados contra a interface real do Portal Nacional.
Use BROWSER_HEADLESS=false para debug visual quando necessário.
"""

import asyncio
import re
import ssl
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.request import urlopen

from playwright.async_api import async_playwright, Page, BrowserContext, TimeoutError as PlaywrightTimeout

from src.logger import log
from src.config import (
    NFSE_NACIONAL_URL,
    NFSE_NACIONAL_USER,
    NFSE_NACIONAL_PASSWORD,
    NFSE_CERT_PASSWORD,
    NFSE_CERT_PEM_PATH,
    NFSE_CERT_KEY_PATH,
    NFSE_DANFSE_API_URL,
    PRESTADOR_CNPJ,
    PRESTADOR_NOME,
    NFSE_NACIONAL_SESSION_STATE,
    client_certificates_nfse_nacional,
    certificado_digital_configurado,
    certificado_mtls_configurado,
    BROWSER_HEADLESS,
    DRY_RUN,
    NATUREZA_OPERACAO,
    CODIGO_SERVICO,
    ITEM_LISTA_SERVICO,
    ALIQUOTA_ISS,
    ALIQUOTA_SIMPLES,
    MUNICIPIO_INCIDENCIA,
    ISS_RETIDO,
    NBS_CORRETAGEM_SEGUROS,
    nbs_para_aluguel,
)

TIMEOUT = 30_000  # 30s

class NfseNacionalError(Exception):
    pass


class SessaoExpirada(NfseNacionalError):
    """Não há sessão válida e o modo desassistido não resolve autenticação."""
    pass


class NfseNacionalAutomation:
    def __init__(
        self,
        user: str,
        password: str,
        natureza_operacao: str,
        codigo_servico: str,
        item_lista_servico: str,
        aliquota_iss: float,
        municipio_incidencia: str,
        iss_retido: bool,
        headless: bool = True,
        dry_run: bool = True,
        storage_state: Optional[str] = None,
        unattended: bool = False,
    ):
        self.user = user
        self.password = password
        self.natureza_operacao = natureza_operacao
        self.codigo_servico = codigo_servico
        self.item_lista_servico = item_lista_servico
        self.aliquota_iss = aliquota_iss
        self.municipio_incidencia = municipio_incidencia
        self.iss_retido = iss_retido
        self.headless = headless
        self.dry_run = dry_run
        self.storage_state = str(storage_state) if storage_state else None
        self.unattended = unattended
        self.usa_certificado = certificado_digital_configurado()
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
        # Portal Nacional usa Gov.br (OAuth/OIDC), não mTLS — client_certificates
        # causa ERR_CONNECTION_CLOSED. O cert A1 é usado para assinar documentos,
        # não como certificado de cliente TLS.
        certificados = client_certificates_nfse_nacional()
        if certificados:
            log.info(
                "Certificado A1 disponível para %s (não usado como TLS client cert — "
                "Portal Nacional usa Gov.br/OAuth)",
                certificados[0]["origin"],
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
            path = LOGS_DIR / f"nacional_{nome}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await self._page.screenshot(path=str(path), full_page=True)
            log.debug("Screenshot salvo: %s", path)
        except Exception as e:
            log.debug("Erro ao salvar screenshot: %s", e)

    async def _preencher(self, selector: str, valor: str, limpar: bool = True, timeout: int = TIMEOUT) -> None:
        el = self._page.locator(selector).first
        await el.wait_for(state="visible", timeout=timeout)
        if limpar:
            await el.clear()
        await el.fill(valor)

    async def _preencher_primeiro(self, seletores: list[str], valor: str, limpar: bool = True) -> bool:
        """Tenta preencher o primeiro seletor visível da lista."""
        for selector in seletores:
            try:
                el = self._page.locator(selector).first
                if await el.count() == 0:
                    continue
                readonly = await el.evaluate(
                    "(element) => element.hasAttribute('readonly') || element.disabled"
                )
                if readonly:
                    continue
                await self._preencher(selector, valor, limpar=limpar, timeout=10_000)
                return True
            except Exception:
                continue
        return False

    async def _definir_valor_js_primeiro(self, seletores: list[str], valor: str) -> bool:
        """Define valor via JS no primeiro seletor encontrado, mesmo se estiver read-only."""
        for selector in seletores:
            try:
                el = self._page.locator(selector).first
                if await el.count() == 0:
                    continue
                await el.wait_for(state="attached", timeout=TIMEOUT)
                await el.evaluate(
                    """
                    (element, value) => {
                        element.value = value;
                        element.dispatchEvent(new Event('input', { bubbles: true }));
                        element.dispatchEvent(new Event('change', { bubbles: true }));
                        element.dispatchEvent(new Event('blur', { bubbles: true }));
                    }
                    """,
                    valor,
                )
                return True
            except Exception:
                continue
        return False

    async def _definir_valor_por_rotulo(self, rotulo: str, valor: str) -> bool:
        """Busca um campo a partir do rótulo visível e define o valor via JS."""
        try:
            return bool(
                await self._page.evaluate(
                    """
                    (labelText, value) => {
                      const norm = (text) => (text || "")
                        .replace(/\\s+/g, " ")
                        .trim()
                        .toLowerCase();
                      const alvo = norm(labelText);
                      const elementos = Array.from(document.querySelectorAll(
                        'label, span, div, p, strong, h1, h2, h3, legend'
                      ));
                      for (const el of elementos) {
                        if (!el.isConnected || !el.getClientRects().length) {
                          continue;
                        }
                        if (!norm(el.textContent).includes(alvo)) {
                          continue;
                        }
                        let node = el;
                        for (let depth = 0; depth < 6 && node; depth += 1, node = node.parentElement) {
                          const field = node.querySelector(
                            "input, select, textarea, [role='combobox'], [contenteditable='true']"
                          );
                          if (!field) {
                            continue;
                          }
                          const tag = field.tagName.toLowerCase();
                          if (tag === "select") {
                            const options = Array.from(field.options || []);
                            const option = options.find((opt) => {
                              const texto = norm(opt.textContent);
                              const valorOpt = norm(opt.value);
                              const valorBuscado = norm(value);
                              return texto.includes(valorBuscado) || valorOpt.includes(valorBuscado);
                            });
                            if (option) {
                              field.value = option.value;
                              field.dispatchEvent(new Event("input", { bubbles: true }));
                              field.dispatchEvent(new Event("change", { bubbles: true }));
                              field.dispatchEvent(new Event("blur", { bubbles: true }));
                              return true;
                            }
                            continue;
                          }
                          if (field.getAttribute("contenteditable") === "true") {
                            field.textContent = value;
                            field.dispatchEvent(new Event("input", { bubbles: true }));
                            field.dispatchEvent(new Event("change", { bubbles: true }));
                            field.dispatchEvent(new Event("blur", { bubbles: true }));
                            return true;
                          }
                          field.value = value;
                          field.dispatchEvent(new Event("input", { bubbles: true }));
                          field.dispatchEvent(new Event("change", { bubbles: true }));
                          field.dispatchEvent(new Event("blur", { bubbles: true }));
                          return true;
                        }
                      }
                      return false;
                    }
                    """,
                    rotulo,
                    valor,
                )
            )
        except Exception:
            return False

    async def _definir_select_direto(self, selector: str, valor: str, texto: str) -> bool:
        """Define selects AJAX/chosen/select2 criando a opção quando necessário."""
        try:
            return bool(
                await self._page.evaluate(
                    """
                    ({ selector, value, text }) => {
                      const el = document.querySelector(selector);
                      if (!el) return false;
                      el.disabled = false;
                      el.removeAttribute("readonly");
                      if (el.tagName === "SELECT") {
                        let option = Array.from(el.options || []).find((opt) => opt.value === value);
                        if (!option) {
                          option = new Option(text, value, true, true);
                          el.add(option);
                        }
                        option.selected = true;
                      } else {
                        el.value = value;
                      }
                      el.value = value;
                      el.dispatchEvent(new Event("input", { bubbles: true }));
                      el.dispatchEvent(new Event("change", { bubbles: true }));
                      el.dispatchEvent(new Event("blur", { bubbles: true }));
                      if (window.jQuery) {
                        const $el = window.jQuery(el);
                        $el.trigger("change");
                        $el.trigger("chosen:updated");
                        $el.trigger("change.select2");
                      }
                      return true;
                    }
                    """,
                    {"selector": selector, "value": valor, "text": texto},
                )
            )
        except Exception:
            return False

    async def _selecionar_select2(self, selector: str, termo: str) -> bool:
        """Seleciona um Select2 usando a busca do próprio Portal."""
        try:
            campo = self._page.locator(selector).first
            if await campo.count() == 0:
                return False
            await campo.wait_for(state="attached", timeout=TIMEOUT)
            await campo.evaluate(
                """
                (element) => {
                  element.disabled = false;
                  if (window.jQuery) {
                    window.jQuery(element).select2("open");
                  } else {
                    element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
                  }
                }
                """
            )
            busca = self._page.locator(
                "input.select2-search__field, input[role='searchbox'], .select2-search input"
            ).last
            await busca.fill(termo, timeout=10_000)
            await asyncio.sleep(1)

            primeira_opcao = self._page.locator(".select2-results__option").first
            if await primeira_opcao.count() > 0:
                await primeira_opcao.click(timeout=10_000)
            else:
                await self._page.keyboard.press("Enter")

            await asyncio.sleep(1)
            return True
        except Exception as e:
            log.debug("Não consegui selecionar %s via Select2: %s", selector, e)
            return False

    async def _marcar_radio(self, name: str, valor: str) -> bool:
        """Marca um radio mesmo quando o Portal o renderiza com estilos customizados."""
        try:
            return bool(
                await self._page.evaluate(
                    """
                    ({ name, value }) => {
                      const radios = Array.from(document.querySelectorAll(
                        `input[type="radio"][name="${name}"]`
                      ));
                      const alvo = radios.find((radio) => radio.value === value);
                      if (!alvo) return false;
                      alvo.disabled = false;
                      alvo.checked = true;
                      alvo.click();
                      alvo.dispatchEvent(new Event("input", { bubbles: true }));
                      alvo.dispatchEvent(new Event("change", { bubbles: true }));
                      return true;
                    }
                    """,
                    {"name": name, "value": valor},
                )
            )
        except Exception:
            return False

    async def _clicar_por_rotulo(self, rotulo: str) -> bool:
        """Clica no primeiro elemento visível cujo texto coincida com o rótulo."""
        try:
            return bool(
                await self._page.evaluate(
                    """
                    (labelText) => {
                      const norm = (text) => (text || "")
                        .replace(/\\s+/g, " ")
                        .trim()
                        .toLowerCase();
                      const alvo = norm(labelText);
                      const elementos = Array.from(document.querySelectorAll(
                        'label, span, div, p, button'
                      ));
                      for (const el of elementos) {
                        if (!el.isConnected || !el.getClientRects().length) {
                          continue;
                        }
                        if (!norm(el.textContent).includes(alvo)) {
                          continue;
                        }
                        el.click();
                        return true;
                      }
                      return false;
                    }
                    """,
                    rotulo,
                )
            )
        except Exception:
            return False

    async def _selecionar_dropdown_por_rotulo(self, rotulo: str, termo: str) -> bool:
        """Seleciona opção em dropdown/select2 localizado pelo rótulo visível."""
        try:
            abriu = bool(
                await self._page.evaluate(
                    """
                    (labelText, searchText) => {
                      const norm = (text) => (text || "")
                        .replace(/\\s+/g, " ")
                        .trim()
                        .toLowerCase();
                      const alvo = norm(labelText);
                      const termo = norm(searchText);
                      const labels = Array.from(document.querySelectorAll(
                        'label, span, div, p, strong, h1, h2, h3, legend'
                      ));

                      for (const label of labels) {
                        if (!label.isConnected || !label.getClientRects().length) continue;
                        if (!norm(label.textContent).includes(alvo)) continue;

                        let node = label;
                        for (let depth = 0; depth < 7 && node; depth += 1, node = node.parentElement) {
                          const select = node.querySelector("select");
                          if (select) {
                            const options = Array.from(select.options || []);
                            const option = options.find((opt) => {
                              const texto = norm(opt.textContent);
                              const valor = norm(opt.value);
                              return texto.includes(termo) || valor.includes(termo) || termo.includes(valor);
                            });
                            if (option) {
                              select.value = option.value;
                              select.dispatchEvent(new Event("input", { bubbles: true }));
                              select.dispatchEvent(new Event("change", { bubbles: true }));
                              select.dispatchEvent(new Event("blur", { bubbles: true }));
                              return true;
                            }
                          }

                          const campo = node.querySelector(
                            ".select2-selection, [role='combobox'], input:not([type='hidden'])"
                          );
                          if (campo) {
                            campo.click();
                            return true;
                          }
                        }
                      }
                      return false;
                    }
                    """,
                    rotulo,
                    termo,
                )
            )
            if not abriu:
                return False

            await asyncio.sleep(0.5)
            busca = self._page.locator(
                "input.select2-search__field, input[role='searchbox'], .select2-search input"
            ).last
            if await busca.count() > 0:
                await busca.fill(termo, timeout=5_000)
                await asyncio.sleep(1)
                await self._page.keyboard.press("Enter")
                await asyncio.sleep(0.5)
            return True
        except Exception:
            return False

    async def _selecionar(self, selector: str, valor: str) -> None:
        el = self._page.locator(selector).first
        await el.wait_for(state="visible", timeout=TIMEOUT)
        await el.select_option(value=valor)

    async def _selecionar_dom(self, selector: str, valor: str) -> None:
        """Seleciona um option mesmo quando o select está oculto no wizard."""
        el = self._page.locator(selector).first
        await el.wait_for(state="attached", timeout=TIMEOUT)
        try:
            await el.select_option(value=valor)
        except Exception:
            await el.evaluate(
                """
                (element, value) => {
                    element.value = value;
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                }
                """,
                valor,
            )

    async def _clicar(self, selector: str) -> None:
        el = self._page.locator(selector).first
        await el.wait_for(state="visible", timeout=TIMEOUT)
        await el.click()

    # ── login ─────────────────────────────────────────────────────────────────

    async def _ja_autenticado(self) -> bool:
        """True se a página atual já está logada (sessão restaurada dos cookies)."""
        try:
            # [AJUSTAR] Detectar elementos específicos da tela logada no Portal Nacional
            conteudo = await self._page.inner_text("body")
            return any(
                m in conteudo
                for m in (
                    "Emitir",
                    "NF-e",
                    "Serviços",
                    "Sair",
                    "Rascunhos",
                    "Últimas NFS-e emitidas",
                    "Meus dados",
                    "Acesso Rápido",
                    "Portal Contribuinte",
                )
            )
        except Exception:
            return False

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
        """
        Faz login no Portal Nacional da NFS-e.

        Portal Nacional suporta:
        1. Gov.br (login único do governo) — recomendado
        2. Certificado digital A1/A3 — alternativa
        3. Usuário/senha — último recurso

        [AJUSTAR] Testar qual fluxo de autenticação o portal usa.
        """
        log.info("Acessando Portal Nacional NFS-e...")
        await self._page.goto(NFSE_NACIONAL_URL, wait_until="networkidle", timeout=60_000)
        await self._screenshot("01_home")

        # Sessão "quente": se os cookies restaurados ainda valem, pula o login
        if await self._ja_autenticado():
            log.info("Sessão restaurada dos cookies — login não necessário")
            return

        if self.usa_certificado:
            # Portal Nacional usa Gov.br/OAuth — o cert A1 não autentica automaticamente
            # via TLS. Segue para o fluxo normal de login.
            log.debug("Cert A1 disponível mas Portal Nacional requer login via Gov.br/OAuth")
            if self.unattended and not (self.storage_state and Path(self.storage_state).exists()):
                raise SessaoExpirada(
                    "Sessão do Portal Nacional expirada. "
                    "Rode 'python -m src.cli login-manual' para renovar a sessão."
                )
            log.info("Seguindo para login assistido via Gov.br")

        if self.unattended and not (self.storage_state and Path(self.storage_state).exists()):
            raise SessaoExpirada(
                "Sessão do Portal Nacional expirada e não há como completar a autenticação "
                "sem um humano. Rode 'python -m src.cli login-manual' para renovar a sessão."
            )

        # [AJUSTAR] Adaptar seletores CSS conforme interface real do Portal Nacional
        # Tente um destes fluxos de login:

        # Opção 1: Procurar botão "Login" ou "Entrar" visível
        try:
            botao_login = self._page.locator("button:has-text('Entrar')").first
            await botao_login.wait_for(state="visible", timeout=10_000)
            await botao_login.click()
            await asyncio.sleep(1)
        except (PlaywrightTimeout, Exception):
            log.debug("Botão 'Entrar' não encontrado, tentando alternativas...")

        # Opção 2: Se for Gov.br, há um redirecionamento automático ou botão específico
        try:
            await self._page.wait_for_url("**/**login**", timeout=15_000)
        except PlaywrightTimeout:
            pass

        # Opção 3: Tela de login com campos de usuário/senha
        try:
            # [AJUSTAR] Validar seletores contra a interface real
            preenchido_usuario = await self._preencher_primeiro(
                [
                    "input[placeholder='CPF/CNPJ']",
                    "input[name='usuario']",
                    "input[name='login']",
                    "input[type='email']",
                    "input[type='text']",
                ],
                self.user,
                limpar=True,
            )
            if not preenchido_usuario:
                log.debug("Campo de usuário não encontrado de forma direta")
        except Exception:
            pass

        try:
            preenchido_senha = await self._preencher_primeiro(
                [
                    "input[placeholder='Senha']",
                    "input[name='senha']",
                    "input[name='password']",
                    "input[type='password']",
                ],
                self.password,
                limpar=True,
            )
            if not preenchido_senha:
                log.debug("Campo de senha não encontrado de forma direta")
        except Exception:
            pass

        # Clica em "Entrar" ou "Login"
        botao_login_encontrado = False
        try:
            await self._page.get_by_role("button", name=re.compile(r"^Entrar$", re.I)).click(timeout=10_000)
            botao_login_encontrado = True
        except Exception:
            try:
                await self._page.get_by_role("button", name=re.compile(r"^Login$", re.I)).click(timeout=10_000)
                botao_login_encontrado = True
            except Exception:
                try:
                    await self._page.locator("input[type='submit']").first.click(timeout=10_000)
                    botao_login_encontrado = True
                except PlaywrightTimeout:
                    await self._screenshot("01_login_preenchimento_falhou")
                    # Em algumas telas do Portal Nacional o login já fica concluído
                    # antes de um botão visível aparecer. Se não houver formulário
                    # de login exposto e o conteúdo parecer autenticado, tratamos
                    # como sessão válida e salvamos o estado atual.
                    conteudo = await self._page.content()
                    tem_campos_login = False
                    for seletor in (
                        "input[placeholder='CPF/CNPJ']",
                        "input[name='usuario']",
                        "input[name='login']",
                        "input[type='password']",
                        "input[type='email']",
                    ):
                        try:
                            if await self._page.locator(seletor).count():
                                tem_campos_login = True
                                break
                        except Exception:
                            continue
                    if not tem_campos_login and any(
                        p in conteudo.lower() for p in ["nfs-e", "emitir", "serviços", "sair"]
                    ):
                        log.warning(
                            "Botão de login não apareceu, mas a página parece autenticada; "
                            "seguindo com a sessão atual."
                        )
                        await self._salvar_sessao()
                        return
                    raise NfseNacionalError(
                        "Não foi possível localizar botão de login no Portal Nacional. "
                        "Verifique a interface do site e ajuste os seletores CSS."
                    )

        await self._page.wait_for_load_state("networkidle", timeout=30_000)
        await self._screenshot("02_pos_login")

        # Verifica se login foi bem-sucedido
        conteudo = await self._page.content()
        if any(p in conteudo.lower() for p in ["senha incorreta", "login inválido", "acesso negado", "erro", "falha"]):
            await self._screenshot("02_login_erro")
            raise NfseNacionalError("Falha no login: credenciais inválidas ou portal indisponível")

        log.info("Login realizado com sucesso no Portal Nacional")
        await self._salvar_sessao()

    # ── navegar para emissão ──────────────────────────────────────────────────

    async def _navegar_emissao(self) -> None:
        """Navega até o formulário de emissão de nova NF-e."""
        # O Portal Nacional abre a emissão completa em /DPS/Pessoas/NovaNFSe.
        # Se a sessão cair em login, o fluxo de login já cuida disso antes.
        try:
            await self._page.goto(
                f"{NFSE_NACIONAL_URL}/DPS/Pessoas/NovaNFSe",
                wait_until="networkidle",
                timeout=30_000,
            )
        except Exception:
            log.warning("Não consegui abrir a emissão completa por URL — tentando pelos links da home")
            await self._page.goto(NFSE_NACIONAL_URL, wait_until="networkidle", timeout=30_000)
            for seletor in (
                "a[href='/EmissorNacional/DPS/Pessoas/NovaNFSe']",
                "a[href='/EmissorNacional/DPS/Pessoas']",
                "a.btnAcesso",
            ):
                try:
                    await self._page.locator(seletor).first.click(timeout=5_000)
                    break
                except Exception:
                    continue

        await self._page.wait_for_load_state("networkidle", timeout=30_000)
        await self._screenshot("03_emissao_formulario")
        log.info("Navegou para o formulário de emissão")

    # ── preencher formulário ──────────────────────────────────────────────────

    async def _preencher_emitente(self, dados: dict) -> None:
        """Preenche a etapa inicial do wizard do Portal Nacional."""
        log.debug("Preenchendo dados do emitente...")

        data_competencia = dados.get("data_pagamento") or datetime.now().strftime("%Y-%m-%d")
        try:
            data_competencia = datetime.fromisoformat(data_competencia).strftime("%d/%m/%Y")
        except Exception:
            data_competencia = datetime.now().strftime("%d/%m/%Y")

        # O Portal Nacional passou a exigir esta escolha antes de habilitar
        # a data de competencia na etapa inicial.
        try:
            ibs_cbs_nao = self._page.locator(
                "xpath=(//*[contains(normalize-space(.), 'Preencher as informações IBS/CBS') or "
                "contains(normalize-space(.), 'Preencher as informacoes IBS/CBS')]/following::input[@type='radio'])[2]"
            ).first
            if await ibs_cbs_nao.count() > 0:
                try:
                    await ibs_cbs_nao.check(timeout=5_000)
                except Exception:
                    await ibs_cbs_nao.evaluate("(el) => el.click()")
        except Exception:
            log.debug("Campo IBS/CBS não ficou disponível nesta etapa")

        await self._preencher_primeiro(
            [
                "input#DataCompetencia",
                "input[name='DataCompetencia']",
                "input[placeholder*='Competência']",
            ],
            data_competencia,
        )

        cpf_cnpj_prestador = re.sub(r"\D", "", PRESTADOR_CNPJ)
        await self._preencher_primeiro(
            [
                "input#Prestador_Inscricao",
                "input[name='Prestador_Inscricao']",
                "input[name='Prestador.Inscricao']",
            ],
            cpf_cnpj_prestador,
        )

        await self._preencher_primeiro(
            [
                "input#Prestador_Nome",
                "input[name='Prestador_Nome']",
                "input[name='Prestador.Nome']",
            ],
            PRESTADOR_NOME,
        )

        # O regime do Simples costuma ficar oculto nesta etapa; tenta marcar
        # o valor mais compatível com o prestador da Impar.
        try:
            await self._selecionar_dom("#SimplesNacional_RegimeApuracaoTributosSN", "1")
        except Exception:
            log.debug("Campo de regime do Simples não ficou disponível nesta etapa")

        # O tipo do emitente pode já vir selecionado pelo portal; se estiver
        # exposto, a opção 3 costuma ser a mais compatível com pessoa jurídica.
        for valor in ("3", "2", "1"):
            try:
                radio = self._page.locator(f"input[name='TipoEmitente'][value='{valor}']").first
                if await radio.count() > 0:
                    try:
                        await radio.check(timeout=5_000)
                    except Exception:
                        await radio.evaluate("(el) => el.click()")
                    break
            except Exception:
                continue

        await self._screenshot("03a_emitente_preenchido")

        try:
            await self._clicar("button#btnAvancar")
        except Exception:
            await self._clicar("button:has-text('Avançar')")

        await self._page.wait_for_load_state("networkidle", timeout=30_000)
        conteudo = await self._page.inner_text("body")
        if "Não foi possível recuperar informações do contribuinte" in conteudo:
            raise NfseNacionalError(
                "O portal não conseguiu recuperar as informações do contribuinte na etapa inicial. "
                "Verifique se o Prestador CNPJ/Nome e o tipo de emitente estão corretos."
            )

        await self._screenshot("03b_emitente_avancado")

    async def _preencher_tomador(self, dados: dict) -> None:
        """Preenche dados do tomador (cliente que recebe o serviço)."""
        log.debug("Informando CPF/CNPJ do tomador...")

        # No Portal Nacional, o bloco do tomador costuma iniciar com
        # "Tomador não informado". Precisamos mudar para "Brasil" antes de
        # tentar preencher CPF/CNPJ, senão o campo não aparece.
        try:
            for seletor in (
                "input[value='Brasil']",
                "label:has-text('Brasil')",
                "text=Brasil",
            ):
                try:
                    opcao = self._page.locator(seletor).first
                    if await opcao.count() > 0:
                        try:
                            await opcao.check(timeout=5_000)
                        except Exception:
                            await opcao.click(timeout=5_000)
                        break
                except Exception:
                    continue
        except Exception:
            log.debug("Não consegui selecionar 'Brasil' explicitamente no tomador")

        # Dá um instante para o portal renderizar os campos após a troca da
        # opção do domicílio.
        await asyncio.sleep(1)

        cpf_cnpj_limpo = re.sub(r"\D", "", dados["cpf_cnpj"])

        candidatos_cpf = [
            "input#Tomador_Inscricao",
            "input[name='Tomador_Inscricao']",
            "input[name='Tomador.Inscricao']",
            "input#cpfCnpjTomador",
            "input[name='cpfCnpjTomador']",
            "input#cpfCnpj",
            "input[name='cpfCnpj']",
            "input[name='cpfCnpjTomador']",
            "input[placeholder*='CPF/CNPJ']",
            "input[id*='tomador']",
        ]
        cpf_preenchido = False
        cpf_selector_usado = None
        for selector in candidatos_cpf:
            try:
                campo = self._page.locator(selector).first
                if await campo.count() > 0:
                    await self._preencher(selector, cpf_cnpj_limpo)
                    cpf_preenchido = True
                    cpf_selector_usado = selector
                    break
            except Exception:
                continue
        if not cpf_preenchido:
            raise NfseNacionalError("Não encontrei campo de CPF/CNPJ do tomador no formulário")

        # Dispara a consulta do tomador para que o portal traga nome e demais
        # dados cadastrais antes de tentar avançar.
        try:
            if cpf_selector_usado:
                campo_cpf = self._page.locator(cpf_selector_usado).first
                await campo_cpf.press("Enter")
                try:
                    await campo_cpf.blur()
                except Exception:
                    pass
                try:
                    await campo_cpf.evaluate(
                        """
                        (element) => {
                          const root = element.parentElement || element.parentElement?.parentElement || element;
                          const buttons = root ? Array.from(root.querySelectorAll('button')) : [];
                          if (buttons.length > 0) {
                            buttons[0].click();
                            return true;
                          }
                          return false;
                        }
                        """
                    )
                except Exception:
                    pass
            else:
                await self._page.keyboard.press("Enter")
        except Exception:
            pass
        try:
            for seletor in (
                "button[aria-label*='Pesquisar']",
                "button[title*='Pesquisar']",
                "button:has-text('Pesquisar')",
                "button:has-text('Buscar')",
                "button:has-text('Consultar')",
                "input#Tomador_Inscricao + button",
                "input[name='Tomador_Inscricao'] + button",
                "input[name='Tomador.Inscricao'] + button",
                "input#cpfCnpjTomador + button",
                "input[name='cpfCnpjTomador'] + button",
                "input#cpfCnpj + button",
                "input#cpfCnpj + button",
                "input[name='cpfCnpj'] + button",
            ):
                try:
                    botao_busca = self._page.locator(seletor).first
                    if await botao_busca.count() > 0:
                        await botao_busca.click(timeout=5_000)
                        break
                except Exception:
                    continue
        except Exception:
            log.debug("Não consegui disparar a busca automática do tomador")

        await asyncio.sleep(2)

        candidatos_nome = [
            "input#Tomador_Nome",
            "input[name='Tomador_Nome']",
            "input[name='Tomador.Nome']",
            "input#nomeTomador",
            "input[name='nomeTomador']",
        ]
        nome_preenchido = await self._preencher_primeiro(candidatos_nome, dados["nome_tomador"])
        if not nome_preenchido:
            candidatos_nome_js = [
                "input[name*='nome' i]",
                "input[id*='nome' i]",
                "input[placeholder*='Nome' i]",
                "input[aria-label*='Nome' i]",
                "input[name*='razao' i]",
                "input[id*='razao' i]",
                "input[placeholder*='Razão' i]",
                "input[aria-label*='Razão' i]",
                "textarea[name*='nome' i]",
                "textarea[id*='nome' i]",
                "textarea[placeholder*='Nome' i]",
                "textarea[aria-label*='Nome' i]",
            ]
            await self._definir_valor_js_primeiro(candidatos_nome_js, dados["nome_tomador"])

        # Alguns rascunhos do Portal Nacional pedem domicílio/endereço na
        # mesma etapa. Tenta completar os campos que existirem sem travar.
        endereco = dados.get("endereco", "")
        numero = dados.get("numero", "")
        complemento = dados.get("complemento", "")
        bairro = dados.get("bairro", "")
        municipio = dados.get("municipio", "")
        uf = dados.get("uf", "")
        cep = dados.get("cep", "")

        for seletores, valor in (
            (["input#Tomador_EnderecoNacional_Logradouro", "input[name='Tomador_EnderecoNacional_Logradouro']"], endereco),
            (["input#Tomador_EnderecoNacional_Numero", "input[name='Tomador_EnderecoNacional_Numero']"], numero),
            (["input#Tomador_EnderecoNacional_Complemento", "input[name='Tomador_EnderecoNacional_Complemento']"], complemento),
            (["input#Tomador_EnderecoNacional_Bairro", "input[name='Tomador_EnderecoNacional_Bairro']"], bairro),
            (["input#Tomador_EnderecoNacional_Municipio", "input[name='Tomador_EnderecoNacional_Municipio']"], municipio),
            (["input#Tomador_EnderecoNacional_UF", "input[name='Tomador_EnderecoNacional_UF']"], uf),
            (["input#Tomador_EnderecoNacional_CEP", "input[name='Tomador_EnderecoNacional_CEP']"], cep),
        ):
            if valor:
                await self._preencher_primeiro(seletores, valor)

        # Se houver campo de busca/validação automática, aguarda carregamento
        await asyncio.sleep(1)
        await self._screenshot("04_tomador_preenchido")

        # Se o nome não veio preenchido em dados (emissão manual), tenta extrair do formulário
        if not dados.get("nome_tomador"):
            try:
                # [AJUSTAR] Localizar campo de nome do tomador
                nome_field = self._page.locator("input[name='nomeTomador']").first
                dados["nome_tomador"] = await nome_field.input_value()
            except Exception:
                dados["nome_tomador"] = f"TOMADOR {cpf_cnpj_limpo}"

        # Depois que o tomador está preenchido, tenta avançar para a etapa de
        # serviço. No Portal Nacional atual essa transição normalmente libera
        # os campos de descrição/valor.
        try:
            await self._clicar("button#btnAvancar")
        except Exception:
            try:
                await self._clicar("button:has-text('Avançar')")
            except Exception:
                log.debug("Não consegui avançar explicitamente para a etapa de serviço")

        await asyncio.sleep(1)
        await self._screenshot("04b_tomador_avancado")

    async def _preencher_servico(self, dados: dict) -> None:
        """Preenche dados do serviço."""
        log.debug("Preenchendo dados do serviço...")

        if not await self._selecionar_select2("#LocalPrestacao_CodigoMunicipioPrestacao", MUNICIPIO_INCIDENCIA):
            await self._definir_select_direto(
                "#LocalPrestacao_CodigoMunicipioPrestacao",
                "4209102",
                "Joinville/SC",
            )
            await self._definir_valor_js_primeiro(
                ["#LocalPrestacao_DescricaoMunicipioPrestacao"],
                "Joinville/SC",
            )
        await asyncio.sleep(1)

        codigo_servico = re.sub(r"\D", "", str(dados.get("codigo_servico") or self.codigo_servico))
        if codigo_servico == "1005":
            codigo_tributacao = "10.05"
            codigo_tributacao_valor = "10.05.01"
            codigo_tributacao_texto = (
                "10.05.01 - Agenciamento, corretagem ou intermediação de bens móveis ou imóveis."
            )
        else:
            codigo_tributacao = "17.12"
            codigo_tributacao_valor = "17.12.01"
            codigo_tributacao_texto = (
                "17.12.01 - Administração em geral, inclusive de bens e negócios de terceiros."
            )

        if not await self._selecionar_select2("#ServicoPrestado_CodigoTributacaoNacional", codigo_tributacao):
            await self._definir_select_direto(
                "#ServicoPrestado_CodigoTributacaoNacional",
                codigo_tributacao_valor,
                codigo_tributacao_texto,
            )
            await self._definir_valor_js_primeiro(
                ["#ServicoPrestado_DescricaoCodigoTributacaoNacional"],
                codigo_tributacao_texto,
            )
        await asyncio.sleep(1)

        await self._marcar_radio("ServicoPrestado.HaExportacaoImunidadeNaoIncidencia", "0")

        if codigo_servico == "1005":
            nbs = re.sub(r"\D", "", NBS_CORRETAGEM_SEGUROS)
            nbs_texto = (
                "109061100 - Serviços de agenciamento e corretagem de seguros, "
                "resseguros e previdência complementar, exceto de seguros saúde"
            )
        else:
            nbs = re.sub(r"\D", "", nbs_para_aluguel(dados.get("tipo_imovel")))
            nbs_texto = (
                "109051200 - Serviços de corretagem de derivativos e commodities"
                if nbs == "109051200"
                else (
                    "110011290 - Serviços de administração e locação de outros imóveis não residenciais"
                    if nbs == "110011290"
                    else "110011100 - Serviços de administração e locação de imóveis residenciais"
                )
            )
        await self._definir_select_direto("#ServicoPrestado_CodigoNBS", nbs, nbs_texto)
        try:
            await self._page.wait_for_function(
                """
                () => {
                  const campo = document.querySelector("#ServicoPrestado_Descricao");
                  return campo && !campo.disabled && !campo.readOnly;
                }
                """,
                timeout=20_000,
            )
        except Exception:
            log.debug("Campo de descrição do serviço não destravou antes do preenchimento")

        # O Portal só libera a descrição depois que Tributação Nacional e NBS
        # ficam consistentes.
        candidatos_descricao = [
            "#ServicoPrestado_Descricao",
            "textarea[name='ServicoPrestado.Descricao']",
            "textarea[name='descricao']",
            "textarea[name='descricaoServico']",
            "textarea[name='Descricao']",
            "textarea[name='DescricaoServico']",
            "textarea#descricaoServico",
            "textarea#DescricaoServico",
            "textarea[id*='descricao']",
            "textarea[placeholder*='Descrição']",
            "input[name='descricaoServico']",
            "input[name='DescricaoServico']",
            "input[id*='descricao']",
            "textarea[name*='servico' i]",
            "textarea[id*='servico' i]",
            "textarea[placeholder*='Serviço' i]",
            "textarea[aria-label*='Descrição' i]",
            "input[name*='descricao' i]",
            "input[id*='descricao' i]",
            "input[placeholder*='Descrição' i]",
            "input[aria-label*='Descrição' i]",
        ]
        if not await self._preencher_primeiro(candidatos_descricao, dados["descricao_servico"]):
            if not await self._definir_valor_js_primeiro(candidatos_descricao, dados["descricao_servico"]):
                raise NfseNacionalError("Não encontrei campo de descrição do serviço")

        # Item de serviço (código) — [AJUSTAR] Testar se é dropdown ou campo livre
        try:
            await self._preencher("input[name='itemLista']", dados.get("codigo_servico") or self.codigo_servico)
        except Exception:
            try:
                await self._selecionar("select[name='itemLista']", dados.get("codigo_servico") or self.codigo_servico)
            except Exception:
                log.warning("Não localizei campo de item de serviço — pode ser preenchido automaticamente")

        await self._screenshot("05_servico_preenchido")

        try:
            await self._clicar("button#btnAvancar")
        except Exception:
            try:
                await self._clicar("button:has-text('Avançar')")
            except Exception:
                log.warning("Não consegui avançar da etapa de serviço para a etapa de valores")

        try:
            confirmar = self._page.locator(
                "button:has-text('SIM'), button:has-text('Sim')"
            ).last
            if await confirmar.count() > 0 and await confirmar.is_visible():
                await confirmar.click(timeout=5_000)
                await self._page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            log.debug("Nenhum modal de confirmação apareceu ao avançar do serviço")

        await asyncio.sleep(1)
        await self._screenshot("05b_servico_avancado")

    async def _preencher_valores(self, dados: dict) -> None:
        """Preenche a etapa de valores/tributação e avança para revisão."""
        log.debug("Preenchendo valores e tributação...")

        valor_str = f"{dados['valor_servico']:.2f}".replace(".", ",")
        if not await self._preencher_primeiro(["#Valores_ValorServico"], valor_str):
            if not await self._definir_valor_js_primeiro(["#Valores_ValorServico"], valor_str):
                raise NfseNacionalError("Não encontrei campo de valor do serviço na etapa Valores")

        await asyncio.sleep(1)

        # Locação simples: sem retenção, sem benefício, sem dedução e sem
        # estimativa detalhada de tributos. Estes campos são defaults do
        # Portal, mas marcamos explicitamente para evitar validação pendente.
        await self._marcar_radio("ISSQN.HaRetencao", "0")
        await self._marcar_radio("ISSQN.HaBeneficioMunicipal", "0")
        await self._marcar_radio("ISSQN.HaDeducaoReducao", "0")
        await self._marcar_radio("ValorTributos.TipoValorTributos", "4")
        await self._definir_valor_js_primeiro(
            ["#ValorTributos_AliquotaSN"],
            f"{ALIQUOTA_SIMPLES:.2f}".replace(".", ","),
        )
        await self._definir_select_direto(
            "#TributacaoFederal_PISCofins_SituacaoTributaria",
            "0",
            "00 - Nenhum",
        )
        await self._definir_select_direto(
            "#TributacaoFederal_PISCofins_TipoRetencao",
            "0",
            "0 - PIS/COFINS/CSLL Não Retidos",
        )

        for selector in (
            "#TributacaoFederal_ValorIRRF",
            "#TributacaoFederal_ValorCSLL",
            "#TributacaoFederal_ValorCP",
        ):
            await self._definir_valor_js_primeiro([selector], "0,00")

        await self._screenshot("06_valores_preenchido")

        try:
            await self._clicar("button#btnAvancar")
        except Exception:
            try:
                await self._clicar("button:has-text('Avançar')")
            except Exception:
                log.warning("Não consegui avançar da etapa de valores para revisão")

        await asyncio.sleep(2)
        await self._screenshot("06b_valores_avancado")

    # ── emitir ────────────────────────────────────────────────────────────────

    async def _clicar_emitir(self) -> None:
        if self.dry_run:
            log.warning("DRY RUN ativo — formulário revisado; não clicando em 'Emitir NFS-e'.")
            await self._screenshot("07_dry_run_revisao")
            return

        # Emissão real
        for selector in (
            "a#btnProsseguir[href*='/DPS/NFSe']",
            "button:has-text('Emitir NFS-e')",
            "a.btn-primary:has-text('Emitir NFS-e')",
            "input[value*='Emitir NFS-e']",
            "button:has-text('Emitir')",
            "a.btn-primary:has-text('Emitir')",
            "input[value*='Emitir']",
            "button:has-text('Enviar')",
            "a.btn-primary:has-text('Enviar')",
        ):
            try:
                await self._page.locator(selector).first.click(timeout=10_000)
                break
            except Exception:
                continue
        else:
            raise NfseNacionalError("Não encontrei botão de emissão no formulário")

        await self._page.wait_for_load_state("networkidle", timeout=30_000)
        await self._screenshot("06_pos_emissao")
        log.info("NF-e enviada com sucesso")

    # ── número da nota + PDF oficial ───────────────────────────────────────────

    async def _baixar_danfse_adn(self, chave_acesso: str) -> bytes:
        """Baixa o DANFSe pela API oficial do ADN, autenticada com certificado A1."""
        if not certificado_mtls_configurado():
            raise NfseNacionalError(
                "Certificado PEM/chave privada não configurados para a API do DANFSe"
            )

        ssl_context = ssl.create_default_context()
        ssl_context.load_cert_chain(
            certfile=NFSE_CERT_PEM_PATH,
            keyfile=NFSE_CERT_KEY_PATH,
            password=NFSE_CERT_PASSWORD,
        )

        url = f"{NFSE_DANFSE_API_URL.rstrip('/')}/{chave_acesso}"
        pdf_bytes = await asyncio.to_thread(
            lambda: urlopen(url, context=ssl_context, timeout=60).read()
        )
        if not pdf_bytes.startswith(b"%PDF"):
            raise NfseNacionalError("A API do ADN não retornou um PDF válido")

        log.info("DANFSe baixado pela API oficial do ADN | chave=%s", chave_acesso)
        return pdf_bytes

    async def _obter_numero_e_pdf(self) -> tuple[str, bytes]:
        """
        Localiza o número da NF-e emitida e baixa o PDF oficial.

        Usa preferencialmente a API oficial do ADN com certificado A1. O download
        pela interface fica apenas como contingência, pois pode exigir hCaptcha.
        """
        if self.dry_run:
            log.warning("DRY RUN — retornando número/PDF placeholder")
            return "DRY-RUN", b"%PDF-1.4 DRY RUN PLACEHOLDER"

        numero = "N/D"
        conteudo = ""
        try:
            conteudo = await self._page.inner_text("body")
            m = re.search(r"(?:número|nº)\s*:?\s*(\d+)", conteudo, re.IGNORECASE)
            if m:
                numero = m.group(1)
        except Exception:
            pass

        chave = re.search(r"\b(\d{50})\b", conteudo)
        if chave:
            try:
                return numero, await self._baixar_danfse_adn(chave.group(1))
            except Exception as e:
                log.warning(
                    "Falha no download do DANFSe pela API do ADN; "
                    "tentando interface do portal: %s",
                    e,
                )

        # Localiza link para download do PDF. No Portal Nacional, o botão
        # oficial costuma ser um <a> com imagem e sem texto visível.
        pdf_link = None
        for selector in (
            "#btnDownloadDANFSE",
            "a[href*='/Notas/Download/DANFSe/']",
            "a[href*='DANFSe']",
            "button:has-text('Baixar DANFSe')",
            "button:has-text('DANFSe')",
            "a[href*='.pdf']",
        ):
            try:
                candidate = self._page.locator(selector).first
                await candidate.wait_for(state="visible", timeout=5_000)
                pdf_link = candidate
                break
            except PlaywrightTimeout:
                continue
            except Exception:
                continue

        if pdf_link is None:
            log.warning(
                "NF-e %s emitida, mas não encontrei link para download do PDF. "
                "A nota pode estar disponível na Consulta.", numero
            )
            return numero, b"%PDF-1.4 PDF not available"

        try:
            async with self._page.expect_download(timeout=20_000) as download_info:
                await pdf_link.click()
            download = await download_info.value
            pdf_path = await download.path()
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
        except Exception as e:
            try:
                conteudo_pos_download = await self._page.inner_text("body")
                if "VALIDAÇÃO DE USUÁRIO" in conteudo_pos_download or "Sou humano" in conteudo_pos_download:
                    log.warning(
                        "Portal exigiu hCaptcha para baixar o DANFSe da nota %s. "
                        "A nota foi emitida, mas o PDF oficial precisa ser baixado "
                        "após validação humana no Portal Nacional.",
                        numero,
                    )
                    return numero, b"%PDF-1.4 DANFSe requires hCaptcha"
            except Exception:
                pass
            log.warning("Erro ao baixar PDF da nota %s: %s", numero, e)
            return numero, b"%PDF-1.4 Erro no download"

        if pdf_bytes[:4] != b"%PDF":
            log.warning("Arquivo baixado não é um PDF válido para nota %s", numero)
            return numero, b"%PDF-1.4 File is not PDF"

        return numero, pdf_bytes

    # ── método principal ──────────────────────────────────────────────────────

    async def emitir(self, dados: dict) -> tuple[bytes, str]:
        """
        Executa o fluxo completo de emissão.
        Retorna (pdf_bytes, numero_nota).
        """
        await self.login()
        await self._navegar_emissao()
        await self._preencher_emitente(dados)
        await self._preencher_tomador(dados)
        await self._preencher_servico(dados)
        await self._preencher_valores(dados)
        await self._clicar_emitir()
        numero, pdf = await self._obter_numero_e_pdf()
        return pdf, numero

    async def emitir_lote(self, lista_dados: list[dict]) -> list[dict]:
        """
        Emite várias notas em uma única sessão (um único login).

        Retorna uma lista alinhada com lista_dados, cada item:
          {"sucesso": True, "numero_nota": str, "pdf_bytes": bytes}
          ou
          {"sucesso": False, "erro": str}
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
                await self._preencher_emitente(dados)
                await self._preencher_tomador(dados)
                await self._preencher_servico(dados)
                await self._preencher_valores(dados)
                await self._clicar_emitir()
                numero, pdf = await self._obter_numero_e_pdf()
                resultados.append({"sucesso": True, "numero_nota": numero, "pdf_bytes": pdf})
                log.info("Nota %d/%d emitida: número %s", i + 1, len(lista_dados), numero)
            except Exception as e:
                log.error("Falha na nota %d/%d (%s): %s", i + 1, len(lista_dados), dados.get("nome_tomador"), e)
                resultados.append({"sucesso": False, "erro": str(e)})
                await self._screenshot(f"lote_erro_item_{i+1}")

        return resultados


async def emitir_nota(
    dados: dict,
    user: Optional[str] = None,
    password: Optional[str] = None,
    natureza_operacao: Optional[str] = None,
    codigo_servico: Optional[str] = None,
    item_lista_servico: Optional[str] = None,
    aliquota_iss: Optional[float] = None,
    municipio_incidencia: Optional[str] = None,
    iss_retido: Optional[bool] = None,
    headless: Optional[bool] = None,
    dry_run: Optional[bool] = None,
    storage_state: Optional[str] = None,
) -> tuple[bytes, str]:
    """Função de conveniência para uso externo (emissão única)."""
    user = user or NFSE_NACIONAL_USER
    password = password or NFSE_NACIONAL_PASSWORD
    natureza_operacao = natureza_operacao or NATUREZA_OPERACAO
    codigo_servico = codigo_servico or CODIGO_SERVICO
    item_lista_servico = item_lista_servico or ITEM_LISTA_SERVICO
    aliquota_iss = ALIQUOTA_ISS if aliquota_iss is None else aliquota_iss
    municipio_incidencia = municipio_incidencia or MUNICIPIO_INCIDENCIA
    iss_retido = ISS_RETIDO if iss_retido is None else iss_retido
    headless = (BROWSER_HEADLESS if headless is None else headless) or certificado_digital_configurado()
    dry_run = DRY_RUN if dry_run is None else dry_run
    storage_state = storage_state or str(NFSE_NACIONAL_SESSION_STATE)

    async with NfseNacionalAutomation(
        user=user,
        password=password,
        natureza_operacao=natureza_operacao,
        codigo_servico=codigo_servico,
        item_lista_servico=item_lista_servico,
        aliquota_iss=aliquota_iss,
        municipio_incidencia=municipio_incidencia,
        iss_retido=iss_retido,
        headless=headless,
        dry_run=dry_run,
        storage_state=storage_state,
    ) as nfse:
        return await nfse.emitir(dados)


async def emitir_notas_em_lote(
    lista_dados: list[dict],
    user: Optional[str] = None,
    password: Optional[str] = None,
    natureza_operacao: Optional[str] = None,
    codigo_servico: Optional[str] = None,
    item_lista_servico: Optional[str] = None,
    aliquota_iss: Optional[float] = None,
    municipio_incidencia: Optional[str] = None,
    iss_retido: Optional[bool] = None,
    headless: Optional[bool] = None,
    dry_run: Optional[bool] = None,
    storage_state: Optional[str] = None,
) -> list[dict]:
    """Função de conveniência para uso externo (emissão em lote, um único login)."""
    user = user or NFSE_NACIONAL_USER
    password = password or NFSE_NACIONAL_PASSWORD
    natureza_operacao = natureza_operacao or NATUREZA_OPERACAO
    codigo_servico = codigo_servico or CODIGO_SERVICO
    item_lista_servico = item_lista_servico or ITEM_LISTA_SERVICO
    aliquota_iss = ALIQUOTA_ISS if aliquota_iss is None else aliquota_iss
    municipio_incidencia = municipio_incidencia or MUNICIPIO_INCIDENCIA
    iss_retido = ISS_RETIDO if iss_retido is None else iss_retido
    headless = (BROWSER_HEADLESS if headless is None else headless) or certificado_digital_configurado()
    dry_run = DRY_RUN if dry_run is None else dry_run
    storage_state = storage_state or str(NFSE_NACIONAL_SESSION_STATE)
    # Função de conveniência é sempre chamada sem supervisão humana
    unattended = True

    async with NfseNacionalAutomation(
        user=user,
        password=password,
        natureza_operacao=natureza_operacao,
        codigo_servico=codigo_servico,
        item_lista_servico=item_lista_servico,
        aliquota_iss=aliquota_iss,
        municipio_incidencia=municipio_incidencia,
        iss_retido=iss_retido,
        headless=headless,
        dry_run=dry_run,
        storage_state=storage_state,
        unattended=unattended,
    ) as nfse:
        return await nfse.emitir_lote(lista_dados)
