#!/usr/bin/env python3
"""
Publicador assistido do Facebook Marketplace para a Impar.

Objetivo:
- abrir Chrome/Chromium com perfil persistente;
- anexar fotos locais automaticamente via set_input_files();
- preencher os principais campos do classificado;
- por padrao parar antes de publicar para revisao humana.

Uso seguro:
  python3 publish_marketplace_playwright.py --index 1 --headed

Publicar de verdade so com confirmacao explicita:
  python3 publish_marketplace_playwright.py --index 1 --headed --publish
"""

import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

# Kernel IMPAR: Seletor de imagens com regra global MARKETPLACE_MAX_IMAGES = 10
from marketplace_image_selector import (
    select_marketplace_images,
    MARKETPLACE_MAX_IMAGES,
)

# Kernel IMPAR: Gerenciador de sessão autenticada
from facebook_session_manager import FacebookSessionManager


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUEUE = (
    ROOT
    / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/uploads-2026-07-08/anuncios-2026-07-08.json"
)
DEFAULT_PROFILE = (
    ROOT
    / ".impar/runtime/facebook-profile"
)
DEFAULT_BROWSER_HOME = (
    ROOT
    / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/browser-home"
)
CREATE_URL = "https://www.facebook.com/marketplace/create/rental"


def only_digits(value):
    return re.sub(r"\D+", "", str(value or ""))


def load_listing(queue_path, index):
    listings = json.loads(queue_path.read_text(encoding="utf-8"))
    if index < 1 or index > len(listings):
        raise SystemExit(f"Indice invalido: {index}. A fila tem {len(listings)} anuncios.")
    listing = listings[index - 1]
    missing = [photo for photo in listing.get("fotos", []) if not Path(photo).exists()]
    if missing:
        raise SystemExit("Fotos nao encontradas:\n" + "\n".join(missing))
    return listing


def fill_first_visible_text_input(page, label_text, value, timeout=2500):
    """Tenta preencher por label/placeholder/texto visivel sem depender de ids dinamicos."""
    candidates = [
        lambda: page.get_by_label(label_text, exact=False),
        lambda: page.get_by_placeholder(label_text, exact=False),
    ]
    for candidate in candidates:
        try:
            locator = candidate()
            for i in range(locator.count()):
                element = locator.nth(i)
                if element.is_visible():
                    element.fill(value, timeout=timeout)
                    return True
        except Exception:
            pass
    return False


def click_text_if_visible(page, text, timeout=1500):
    try:
        locator = page.get_by_text(text, exact=True)
        if locator.count() == 1:
            locator.click(timeout=timeout)
            return True
    except Exception:
        return False
    return False


def fill_by_label(page, label_text, value, timeout=2500):
    """Preenche o input/textarea dentro do <label> cujo texto visivel casa.

    O Facebook nao usa aria-label/placeholder nos campos do Marketplace; o texto
    fica no proprio label que envolve o input.
    """
    try:
        containers = page.locator("label", has_text=label_text)
        for i in range(containers.count()):
            container = containers.nth(i)
            if not container.is_visible():
                continue
            field = container.locator("input, textarea").first
            if field.count() >= 1:
                field.fill(str(value), timeout=timeout)
                return True
    except Exception:
        pass
    return False


def choose_combobox_option(page, label_text, option_text):
    """Abre um combobox pelo texto do label e escolhe a opcao pelo texto."""
    try:
        box = page.locator("label", has_text=label_text)
        if box.count() == 0:
            box = page.get_by_text(label_text, exact=False)
        if box.count() >= 1:
            box.first.click(timeout=2500)
            page.wait_for_timeout(800)
            option = page.get_by_role("option", name=re.compile(re.escape(option_text), re.I))
            if option.count() == 0:
                option = page.get_by_text(option_text, exact=False)
            for i in range(option.count()):
                candidate = option.nth(i)
                if candidate.is_visible():
                    candidate.click(timeout=2500)
                    page.wait_for_timeout(600)
                    return True
    except Exception:
        return False
    return False


def confirm_leave_dialog(page):
    """Confirma o dialogo 'Sair da pagina?' ao trocar de categoria."""
    try:
        button = page.get_by_role("button", name=re.compile("Sair da p[aá]gina", re.I))
        for i in range(button.count()):
            candidate = button.nth(i)
            if candidate.is_visible():
                candidate.click(timeout=2500)
                page.wait_for_timeout(3000)
                return True
    except Exception:
        pass
    return False


def fill_location(page, city_text):
    """Preenche o autocomplete de localizacao (input dentro de label sem texto)."""
    try:
        containers = page.locator("label:has(input)")
        for i in range(containers.count()):
            container = containers.nth(i)
            if not container.is_visible():
                continue
            text = (container.inner_text() or "").strip()
            if text:
                continue
            field = container.locator("input").first
            field_type = (field.get_attribute("type") or "").lower()
            if field_type not in ("", "text"):
                continue
            box = field.bounding_box()
            # So o campo do formulario (coluna esquerda, abaixo do header).
            if not box or box["x"] > 380 or box["y"] < 120:
                continue
            field.click(timeout=2000)
            field.fill("", timeout=2000)
            field.type(city_text, delay=60)
            page.wait_for_timeout(2500)
            # Clicar a primeira sugestao do autocomplete; nunca usar Enter
            # (Enter fora de sugestao dispara navegacao/busca).
            option = page.get_by_role("option")
            for j in range(option.count()):
                suggestion = option.nth(j)
                if suggestion.is_visible():
                    suggestion.click(timeout=2500)
                    page.wait_for_timeout(1200)
                    return True
            return True
    except Exception:
        pass
    return False


def attach_photos(page, photo_paths):
    inputs = page.locator('input[type="file"]')
    count = inputs.count()
    if count == 0:
        raise RuntimeError("Nenhum input de foto encontrado no formulario.")

    # O primeiro input multiple costuma ser o uploader principal do Marketplace.
    for i in range(count):
        current = inputs.nth(i)
        try:
            multiple = current.evaluate("el => el.multiple")
            if multiple:
                current.set_input_files(photo_paths)
                return
        except Exception:
            continue

    inputs.nth(0).set_input_files(photo_paths)


def fill_listing(page, listing):
    page.goto(CREATE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3500)

    # Combobox 1 ("Imóvel residencial para venda ou locação"): opcoes reais
    # sao "Aluguel" e "À venda". Obrigatorio para habilitar o Avancar.
    texto_ref = f"{listing.get('titulo','')} {listing.get('url','')}".lower()
    operacao = "À venda" if "venda" in texto_ref else "Aluguel"
    choose_combobox_option(page, "Imóvel residencial para venda ou locação", operacao)
    page.wait_for_timeout(1200)

    # Combobox 2: tipo do imovel.
    tipo = listing["tipo"].lower()
    if "apartamento" in tipo:
        choose_combobox_option(page, "Tipo de imóvel", "Apartamento")
    elif "casa" in tipo:
        choose_combobox_option(page, "Tipo de imóvel", "Casa")
    else:
        # Sala comercial nao existe no fluxo residencial; usar "Outro" se houver.
        if not choose_combobox_option(page, "Tipo de imóvel", "Sala comercial"):
            choose_combobox_option(page, "Tipo de imóvel", "Outro")
    page.wait_for_timeout(1200)

    # Kernel IMPAR: Limitar a máximo 10 imagens antes de enviar
    # Regra global: MARKETPLACE_MAX_IMAGES = 10 (desde 2026-07-24)
    fotos = listing.get("fotos", [])
    rejected = listing.get("rejected_images", [])
    property_code = listing.get("codigo", listing.get("codigo_imovel", "UNKNOWN"))

    selection_result = select_marketplace_images(
        all_images=fotos,
        rejected_images=rejected,
        max_images=MARKETPLACE_MAX_IMAGES,
        property_code=property_code,
    )

    fotos_selecionadas = selection_result["selected"]
    print(
        f"[MARKETPLACE_MAX_IMAGES] {property_code}: "
        f"{selection_result['total_input']} → {selection_result['total_selected']} "
        f"(limite: {MARKETPLACE_MAX_IMAGES})"
    )

    attach_photos(page, fotos_selecionadas)
    page.wait_for_timeout(2500)

    fill_by_label(page, "Número de quartos", "0" if "sala" in listing["tipo"].lower() else "1")
    fill_by_label(page, "Número de banheiros", "1")
    fill_by_label(page, "Preço", only_digits(listing["preco"]))

    # Localizacao e obrigatoria para habilitar o Avancar.
    fill_location(page, listing.get("cidade") or "Joinville")

    # Campos numericos opcionais quando o Facebook os exibe.
    area_match = re.search(r"(?:area util|área útil|area total|área total)\s+([0-9,.]+)", listing["descricao"], re.I)
    if area_match:
        area = only_digits(area_match.group(1).split(",")[0])
        fill_by_label(page, "Metros quadrados", area)

    # Descricao por ultimo para nao ser sobrescrita por fills genericos.
    # O label muda conforme a operacao: "Descrição da locação" (Aluguel)
    # ou "Descrição do imóvel" (À venda).
    for descricao_label in ("Descrição da locação", "Descrição do imóvel", "Descrição"):
        if fill_by_label(page, descricao_label, listing["descricao"]):
            break


ITEM_CREATE_URL = "https://www.facebook.com/marketplace/create/item"


def fill_listing_item(page, listing):
    """Fluxo de ITEM generico (titulo customizado) - usado para Sala Comercial etc.

    Campos: fotos, Titulo, Preco, Categoria, Condicao, Descricao.
    """
    page.goto(ITEM_CREATE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3500)

    # Kernel IMPAR: Limitar a máximo 10 imagens antes de enviar
    fotos = listing.get("fotos", [])
    rejected = listing.get("rejected_images", [])
    property_code = listing.get("codigo", listing.get("codigo_imovel", "UNKNOWN"))

    selection_result = select_marketplace_images(
        all_images=fotos,
        rejected_images=rejected,
        max_images=MARKETPLACE_MAX_IMAGES,
        property_code=property_code,
    )

    fotos_selecionadas = selection_result["selected"]
    print(
        f"[MARKETPLACE_MAX_IMAGES] {property_code}: "
        f"{selection_result['total_input']} → {selection_result['total_selected']} "
        f"(limite: {MARKETPLACE_MAX_IMAGES})"
    )

    attach_photos(page, fotos_selecionadas)
    page.wait_for_timeout(2500)

    titulo = (listing.get("titulo") or listing.get("titulo_sugerido") or "").strip()
    # Limite do Facebook para titulo de item (~99 chars): truncar em palavra.
    if len(titulo) > 95:
        titulo = titulo[:95].rsplit(" ", 1)[0].rstrip(" -|,;")
    fill_by_label(page, "Título", titulo)
    fill_by_label(page, "Preço", only_digits(listing["preco"]))

    # Categoria: lista longa; Playwright rola ate a opcao ao clicar.
    try:
        page.locator("label", has_text="Categoria").first.click(timeout=3000)
        page.wait_for_timeout(1200)
        for categoria in ("Diversos", "Venda de garagem"):
            alvo = page.get_by_text(categoria, exact=True)
            achou = False
            for i in range(alvo.count()):
                candidato = alvo.nth(i)
                try:
                    candidato.click(timeout=2500)
                    achou = True
                    break
                except Exception:
                    continue
            if achou:
                print(f"Categoria escolhida: {categoria}")
                break
        page.wait_for_timeout(1200)
    except Exception:
        pass

    # Condicao (se seguir visivel/obrigatoria para a categoria escolhida).
    try:
        cond = page.locator("label", has_text="Condição")
        if cond.count() and cond.first.is_visible():
            cond.first.click(timeout=2500)
            page.wait_for_timeout(1000)
            opcao = page.get_by_role("option", name=re.compile("Novo", re.I))
            if opcao.count() == 0:
                opcao = page.get_by_text("Novo", exact=True)
            for i in range(opcao.count()):
                if opcao.nth(i).is_visible():
                    opcao.nth(i).click(timeout=2500)
                    break
            page.wait_for_timeout(800)
    except Exception:
        pass

    for descricao_label in ("Descrição", "Descricao"):
        if fill_by_label(page, descricao_label, listing["descricao"]):
            break


def maybe_publish(page, publish):
    page.wait_for_timeout(1500)
    if not publish:
        print("REVISAO: formulario preenchido. Publicacao nao enviada porque --publish nao foi usado.")
        return

    # Fluxo em etapas do Marketplace: 0..N cliques em "Avançar" e por fim "Publicar".
    pattern = re.compile(r"^\s*(publicar|avan[cç]ar|next|publish)\s*$", re.I)
    clicked_any = False
    for _ in range(4):
        buttons = page.get_by_role("button", name=pattern)
        target = None
        label = ""
        for i in range(buttons.count()):
            candidate = buttons.nth(i)
            try:
                if candidate.is_visible() and candidate.is_enabled():
                    target = candidate
                    label = (candidate.inner_text() or "").strip()
                    break
            except Exception:
                continue
        if target is None:
            break
        target.click(timeout=5000)
        page.wait_for_timeout(4500)
        clicked_any = True
        print(f"Acao clicada: {label or 'botao'}")
        if label and label.lower().startswith("publicar"):
            print("PUBLICADO: botao Publicar clicado.")
            return
    if not clicked_any:
        # Forcar clique no botao aria-disabled: o Facebook destaca o campo
        # obrigatorio faltante com mensagem de erro visivel.
        try:
            fallback = page.get_by_role("button", name=pattern)
            for i in range(fallback.count()):
                candidate = fallback.nth(i)
                if candidate.is_visible():
                    candidate.click(timeout=3000, force=True)
                    page.wait_for_timeout(3000)
                    break
            errors = page.evaluate(
                """() => Array.from(document.querySelectorAll('[role=\"alert\"], [aria-invalid=\"true\"]'))
                    .map(e => (e.innerText || e.getAttribute('aria-label') || '').slice(0, 120))
                    .filter(Boolean)"""
            )
            print("ERROS_VALIDACAO:", json.dumps(errors, ensure_ascii=False))
            page.screenshot(path="/tmp/marketplace-debug-postclick.png")
        except Exception:
            pass
        try:
            page.screenshot(path="/tmp/marketplace-debug-publicar.png")
            dump = page.evaluate(
                """() => Array.from(document.querySelectorAll('[role=\"button\"], button'))
                    .filter(e => e.offsetParent !== null)
                    .map(e => ({
                        name: (e.innerText || e.getAttribute('aria-label') || '').slice(0, 40),
                        aria_disabled: e.getAttribute('aria-disabled'),
                        tabindex: e.getAttribute('tabindex'),
                    }))
                    .filter(b => b.name)"""
            )
            Path("/tmp/marketplace-debug-buttons.json").write_text(
                json.dumps(dump, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            fields = page.evaluate(
                """() => Array.from(document.querySelectorAll('label'))
                    .filter(e => e.offsetParent !== null)
                    .map(e => {
                        const f = e.querySelector('input, textarea');
                        return {
                            label: (e.innerText || '').split('\\n')[0].slice(0, 45),
                            value: f ? (f.value || '').slice(0, 45) : null,
                            invalid: f ? f.getAttribute('aria-invalid') : null,
                        };
                    })"""
            )
            Path("/tmp/marketplace-debug-fields.json").write_text(
                json.dumps(fields, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            page.screenshot(path="/tmp/marketplace-debug-fullpage.png", full_page=True)
        except Exception:
            pass
        raise RuntimeError("Botao Publicar/Avancar nao encontrado.")
    print("AVISO: cliquei em etapas, mas nao vi o botao final 'Publicar'. Verificar screenshot.")
    try:
        page.screenshot(path="/tmp/marketplace-debug-publicar.png")
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser()

    # Modos de autenticação
    auth_group = parser.add_argument_group("Autenticação (Kernel IMPAR)")
    auth_group.add_argument("--auth-setup", action="store_true", help="Modo AUTH_SETUP: Capturar login manual")
    auth_group.add_argument("--auth-check", action="store_true", help="Modo AUTH_CHECK: Validar sessão")

    # Argumentos normais
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--browser-home", type=Path, default=DEFAULT_BROWSER_HOME)
    parser.add_argument("--index", type=int, default=1, help="1 a 5 para os anuncios do dia")
    parser.add_argument("--headed", action="store_true", help="Abrir navegador visivel")
    parser.add_argument("--publish", action="store_true", help="Clicar para publicar de verdade")
    parser.add_argument("--dry-run", action="store_true", help="Executar sem clicar em Avançar")
    parser.add_argument("--system-chrome", action="store_true", help="Usar Google Chrome do sistema em vez do Chromium do Playwright")
    args = parser.parse_args()

    # Inicializar gerenciador de sessão
    session_manager = FacebookSessionManager(args.profile)

    # Modo AUTH_SETUP
    if args.auth_setup:
        success = session_manager.auth_setup(headless=False)
        sys.exit(0 if success else 1)

    # Modo AUTH_CHECK
    if args.auth_check:
        result = session_manager.auth_check()
        sys.exit(0 if result == "FACEBOOK_SESSION_VALID" else 1)

    # Modo normal: Publicação/Dry Run
    listing = load_listing(args.queue, args.index)
    args.profile.mkdir(parents=True, exist_ok=True)
    args.browser_home.mkdir(parents=True, exist_ok=True)
    (args.browser_home / "Library/Application Support").mkdir(parents=True, exist_ok=True)
    (args.browser_home / "Library/Caches").mkdir(parents=True, exist_ok=True)

    try:
        # Obter contexto autenticado
        browser, page, auth_status = session_manager.get_authenticated_context()

        if auth_status != "AUTHENTICATED":
            print(f"Erro: Sessão não autenticada ({auth_status})")
            print("Execute: python3 publish_marketplace_playwright.py --auth-setup")
            sys.exit(1)

        try:
            fill_listing(page, listing)

            if args.dry_run:
                # Dry run: Não clicar em Avançar
                print("DRY RUN: Formulário preenchido, não clicando em Avançar")
                page.screenshot(path="marketplace-dryrun-final.png")
            else:
                maybe_publish(page, args.publish)

            print(json.dumps({"ok": True, "codigo": listing["codigo"], "url": page.url}, ensure_ascii=False))

        except PlaywrightTimeoutError as exc:
            print(json.dumps({"ok": False, "codigo": listing["codigo"], "error": f"timeout: {exc}"}, ensure_ascii=False))
            sys.exit(1)
        except Exception as exc:
            print(json.dumps({"ok": False, "codigo": listing["codigo"], "error": str(exc)}, ensure_ascii=False))
            sys.exit(1)
        finally:
            if not args.headed:
                browser.close()
            else:
                print("Navegador mantido aberto para revisao. Feche manualmente quando terminar.")

    except RuntimeError as e:
        print(f"Erro de autenticação: {e}")
        print("\nPróximo passo: python3 publish_marketplace_playwright.py --auth-setup")
        sys.exit(1)


if __name__ == "__main__":
    main()
