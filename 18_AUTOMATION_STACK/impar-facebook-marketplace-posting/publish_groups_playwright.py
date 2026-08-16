#!/usr/bin/env python3
"""
Publicador assistido de grupos do Facebook para a Impar.

Objetivo:
- ler fila de grupos (fila-grupos-postagens.csv);
- abrir Chrome/Chromium com perfil persistente;
- publicar em cada grupo com cadencia de 3 minutos;
- por padrao parar antes de publicar para revisao humana.

Uso seguro (dry-run):
  python3 publish_groups_playwright.py --headed

Publicar de verdade so com confirmacao explicita:
  python3 publish_groups_playwright.py --headed --publish

Cadência em lotes (19 grupos × 2 min):
  python3 publish_groups_playwright.py --headed --publish --batch-size 19 --batch-interval 120
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "05_WORKSPACE" / "clientes" / "impar-imoveis" / "automacoes" / "facebook-marketplace"
DEFAULT_QUEUE = WORKSPACE / "fila-grupos-postagens.csv"
DEFAULT_PROFILE = WORKSPACE / "browser-profile"
DEFAULT_BROWSER_HOME = WORKSPACE / "browser-home"
LOG_FILE = WORKSPACE / "publicacao-grupos.log"

FACEBOOK_HOME = "https://www.facebook.com/"


def log_event(message, status="INFO"):
    """Registra eventos em arquivo de log."""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {status}: {message}"
    print(log_entry)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(log_entry + "\n")


def load_group_queue(queue_path):
    """Carrega a fila de grupos do CSV."""
    if not queue_path.exists():
        raise FileNotFoundError(f"Fila nao encontrada: {queue_path}")

    with queue_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def click_text_if_visible(page, text, timeout=1500):
    """Clica em um elemento visivel com exato match de texto."""
    try:
        locator = page.get_by_text(text, exact=True)
        if locator.count() >= 1:
            locator.first.click(timeout=timeout)
            return True
    except Exception:
        return False
    return False


def find_and_click_button(page, texts):
    """Tenta clicar em um botao procurando por multiplos textos possiveis."""
    for text in texts:
        try:
            if click_text_if_visible(page, text, timeout=2500):
                return True
        except Exception:
            pass
    return False


def wait_for_element_then_click(page, selector, timeout=3000):
    """Aguarda um elemento e clica."""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector, timeout=timeout)
        return True
    except Exception:
        return False


def fill_text_input_by_label(page, label_text, value, timeout=2500):
    """Preenche input de texto procurando por label."""
    try:
        locator = page.get_by_label(label_text, exact=False)
        if locator.count() >= 1:
            locator.first.fill(value, timeout=timeout)
            return True
    except Exception:
        pass
    return False


def post_to_group(page, group_row, publish=False, dry_run=False):
    """
    Publica um item em um grupo do Facebook.

    Fluxo:
    1. Navega para o grupo (via URL armazenada em grupo_url)
    2. Clica em "Criar post" ou similar
    3. Preenche o texto (titulo_sugerido + referencia)
    4. Publica (ou para para revisao se nao estiver em publish mode)
    """
    grupo_url = group_row.get("grupo_url", "").strip()
    grupo_nome = group_row.get("grupo_nome", "[SEM NOME]")
    titulo = group_row.get("titulo_sugerido", "")
    referencia = group_row.get("referencia", "")
    ordem_global = group_row.get("ordem_global", "?")

    # Construir texto do post
    texto_post = f"{titulo}\n\n{referencia}" if referencia else titulo

    log_event(f"[{ordem_global}] Processando grupo '{grupo_nome}'", "INFO")

    if dry_run:
        log_event(f"[{ordem_global}] DRY-RUN: {texto_post[:100]}...", "PREVIEW")
        return True

    try:
        # Se ha URL do grupo, tentar navegar direto
        if grupo_url:
            log_event(f"[{ordem_global}] Navegando para: {grupo_url}", "NAVIGATE")
            page.goto(grupo_url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
        else:
            log_event(f"[{ordem_global}] Nenhuma URL disponivel para '{grupo_nome}'", "WARN")
            return False

        # Procurar botao "Criar publicacao" ou similar
        buttons_criar = ["Criar publicação", "Criar publicacao", "Postar", "Post", "Escrever algo"]
        found_create = False

        for btn_text in buttons_criar:
            try:
                if click_text_if_visible(page, btn_text, timeout=2000):
                    log_event(f"[{ordem_global}] Clicado: {btn_text}", "ACTION")
                    found_create = True
                    break
            except Exception:
                pass

        if not found_create:
            log_event(f"[{ordem_global}] Botao de criar post nao encontrado em '{grupo_nome}'", "WARN")
            return False

        page.wait_for_timeout(1000)

        # Procurar e preencher textarea/contenteditable do post
        try:
            # Tentar textarea
            textarea = page.locator("textarea").first
            if textarea.count() > 0:
                textarea.click(timeout=2000)
                textarea.fill(texto_post, timeout=2000)
                log_event(f"[{ordem_global}] Texto preenchido em textarea", "ACTION")
            else:
                # Tentar contenteditable
                editable = page.locator("[contenteditable='true']").first
                if editable.count() > 0:
                    editable.click(timeout=2000)
                    editable.fill(texto_post, timeout=2000)
                    log_event(f"[{ordem_global}] Texto preenchido em contenteditable", "ACTION")
                else:
                    log_event(f"[{ordem_global}] Nenhum campo de texto encontrado", "WARN")
                    return False
        except Exception as e:
            log_event(f"[{ordem_global}] Erro ao preencher texto: {e}", "ERROR")
            return False

        page.wait_for_timeout(500)

        if not publish:
            log_event(f"[{ordem_global}] REVISAO: formulario preenchido. Publicacao nao enviada porque --publish nao foi usado.", "REVIEW")
            return True

        # Procurar e clicar em botao de publicar
        botoes_publicar = ["Publicar", "Postar", "Enviar", "Compartilhar"]
        found_publish = False

        for btn_text in botoes_publicar:
            try:
                if click_text_if_visible(page, btn_text, timeout=2000):
                    log_event(f"[{ordem_global}] Clicado: {btn_text}", "PUBLISH")
                    found_publish = True
                    page.wait_for_timeout(2000)
                    break
            except Exception:
                pass

        if not found_publish:
            log_event(f"[{ordem_global}] Botao de publicar nao encontrado", "WARN")
            return False

        log_event(f"[{ordem_global}] PUBLICADO com sucesso em '{grupo_nome}'", "SUCCESS")
        return True

    except PlaywrightTimeoutError as e:
        log_event(f"[{ordem_global}] Timeout em '{grupo_nome}': {e}", "ERROR")
        return False
    except Exception as e:
        log_event(f"[{ordem_global}] Erro ao postar em '{grupo_nome}': {e}", "ERROR")
        return False


def main():
    parser = argparse.ArgumentParser(description="Publicador de grupos Facebook Impar")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE, help="Caminho da fila (CSV)")
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE, help="Perfil persistente do navegador")
    parser.add_argument("--browser-home", type=Path, default=DEFAULT_BROWSER_HOME, help="HOME do navegador")
    parser.add_argument("--headed", action="store_true", help="Abrir navegador visivel")
    parser.add_argument("--publish", action="store_true", help="Publicar de verdade (sem --publish, so revisao)")
    parser.add_argument("--batch-size", type=int, default=19, help="Grupos por lote (padrao: 19)")
    parser.add_argument("--batch-interval", type=int, default=120, help="Intervalo em segundos entre lotes (padrao: 120 = 2 min)")
    parser.add_argument("--start-index", type=int, default=1, help="Comeca do indice N (1-indexed)")
    parser.add_argument("--system-chrome", action="store_true", help="Usar Google Chrome do sistema")
    args = parser.parse_args()

    # Setup
    args.profile.mkdir(parents=True, exist_ok=True)
    args.browser_home.mkdir(parents=True, exist_ok=True)
    (args.browser_home / "Library/Application Support").mkdir(parents=True, exist_ok=True)
    (args.browser_home / "Library/Caches").mkdir(parents=True, exist_ok=True)

    log_event(f"Iniciando publicador de grupos", "START")
    log_event(f"Queue: {args.queue}", "CONFIG")
    log_event(f"Publish mode: {'ATIVO' if args.publish else 'DRY-RUN'}", "CONFIG")
    log_event(f"Lotes: {args.batch_size} grupos × {args.batch_interval}s", "CONFIG")

    queue = load_group_queue(args.queue)
    log_event(f"Fila carregada: {len(queue)} itens", "INFO")

    if not queue:
        log_event("Fila vazia!", "ERROR")
        sys.exit(1)

    # Filtrar para comecar do indice
    start_idx = max(0, args.start_index - 1)
    queue_slice = queue[start_idx:]

    if not queue_slice:
        log_event(f"Nenhum item a partir do indice {args.start_index}", "ERROR")
        sys.exit(1)

    log_event(f"Processando {len(queue_slice)} itens (a partir do indice {args.start_index})", "INFO")

    dry_run = not args.publish

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(args.profile),
            channel="chrome" if args.system_chrome else None,
            headless=not args.headed,
            viewport={"width": 1280, "height": 900},
            args=[
                "--disable-crash-reporter",
                "--disable-crashpad",
                "--disable-breakpad",
                "--no-default-browser-check",
                "--no-first-run",
            ],
            env={
                "HOME": str(args.browser_home),
                "TMPDIR": str(args.browser_home / "tmp"),
            },
        )

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(FACEBOOK_HOME, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        # Falha segura: sem sessao logada, aborta antes de queimar a fila.
        if page.locator('input[type="password"]').count() > 0:
            log_event("SESSAO_INVALIDA: perfil nao esta logado no Facebook. Abortando sem publicar.", "ERROR")
            browser.close()
            sys.exit(2)

        stats = {"total": 0, "success": 0, "failed": 0, "batches": 0}

        try:
            batch_idx = 0
            for idx, row in enumerate(queue_slice, start=start_idx + 1):
                stats["total"] += 1
                batch_idx += 1

                success = post_to_group(page, row, publish=args.publish, dry_run=dry_run)

                if success:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1

                # Aguardar intervalo entre lotes (apos cada grupo 19, 38, 57, etc)
                if batch_idx % args.batch_size == 0 and idx < len(queue):
                    stats["batches"] += 1
                    log_event(f"Lote {stats['batches']} completo. Aguardando {args.batch_interval}s antes do proximo...", "BATCH")
                    time.sleep(args.batch_interval)

            log_event(
                f"Finalizacao: {stats['success']}/{stats['total']} sucesso, {stats['failed']} falharam",
                "SUMMARY"
            )

            print(json.dumps(stats, ensure_ascii=False))

        except KeyboardInterrupt:
            log_event("Interrompido pelo usuario", "INTERRUPT")
            sys.exit(130)
        finally:
            if not args.headed:
                browser.close()
            else:
                log_event("Navegador mantido aberto para revisao. Feche manualmente quando terminar.", "INFO")


if __name__ == "__main__":
    main()
