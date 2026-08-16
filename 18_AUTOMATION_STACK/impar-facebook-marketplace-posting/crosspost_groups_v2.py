#!/usr/bin/env python3
"""Crosspost do anuncio publicado do Marketplace para grupos aprovados.

Fluxo por grupo: Seus classificados -> Compartilhar (1o card) -> Grupo ->
procurar grupo -> selecionar -> escrever texto -> Publicar.

Uso:
  python3 crosspost_groups_v2.py --limit 2 --cadence 30          # teste
  python3 crosspost_groups_v2.py --cadence 180                    # fila toda
Falha segura: para em checkpoint/captcha/login. Log CSV com resume
(grupos ja publicados hoje sao pulados).
"""
import argparse
import csv
import datetime as dt
import re
import json
import random
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace"
PROFILE = WORKSPACE / "browser-profile"
GROUPS_CSV = WORKSPACE / "grupos-aprovados.csv"
LOG_CSV = WORKSPACE / "crosspost-grupos-log.csv"
SELLING_URL = "https://www.facebook.com/marketplace/you/selling"
SHOT = "/tmp/crosspost-debug.png"


def log_row(grupo, status, detalhe=""):
    new = not LOG_CSV.exists()
    with LOG_CSV.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["data", "grupo", "status", "detalhe"])
        w.writerow([dt.datetime.now().isoformat(timespec="seconds"), grupo, status, detalhe])


def ja_publicado_hoje(grupo):
    if not LOG_CSV.exists():
        return False
    hoje = dt.date.today().isoformat()
    for row in csv.DictReader(LOG_CSV.open(encoding="utf-8")):
        if row["grupo"] == grupo and row["status"] == "ok" and row["data"].startswith(hoje):
            return True
    return False


def sessao_invalida(page):
    url = page.url
    if "login" in url or "checkpoint" in url:
        return True
    try:
        if page.locator("input[type='password']").count() > 0:
            return True
    except Exception:
        pass
    return False


def bloqueio_temporario(page):
    """Detecta o aviso 'Você está bloqueado temporariamente' do Facebook."""
    try:
        texto = page.evaluate("() => document.body.innerText.slice(0, 4000)")
        return "bloqueado temporariamente" in texto.lower()
    except Exception:
        return False


def rate_limit_grupos(page):
    """Detecta aviso de frequência limitada em grupos em qualquer dialog visível."""
    try:
        texto = page.get_by_role("dialog").inner_text(timeout=2000)
        t = texto.lower()
        return "limitamos a frequência" in t or "você pode tentar novamente mais tarde" in t
    except Exception:
        pass
    # Verifica também no body (rate-limit pode aparecer fora do dialog)
    try:
        corpo = page.evaluate("() => document.body.innerText.slice(0, 6000)").lower()
        return "limitamos a frequência" in corpo or "você pode tentar novamente mais tarde" in corpo
    except Exception:
        return False


def fechar_dialogos(page):
    try:
        fechar = page.get_by_role("dialog").get_by_role("button", name="Fechar")
        for i in range(fechar.count()):
            if fechar.nth(i).is_visible():
                fechar.nth(i).click(timeout=1500)
                page.wait_for_timeout(800)
    except Exception:
        pass
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
    except Exception:
        pass


def compartilhar_no_grupo(page, grupo, mensagem):
    page.goto(SELLING_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(6000)
    if sessao_invalida(page):
        raise SystemExit("SESSAO_INVALIDA")
    if bloqueio_temporario(page):
        raise SystemExit("BLOQUEIO_TEMPORARIO")
    # Regra: so compartilhar imovel ANUNCIADO nos ultimos 7 dias.
    janela = {(dt.date.today() - dt.timedelta(days=i)).strftime("%d/%m") for i in range(7)}
    try:
        texto = page.evaluate("() => document.body.innerText.slice(0, 6000)")
        m = re.search(r"Anunciado em (\d{2}/\d{2})", texto)
    except Exception:
        m = None
    if not m or m.group(1) not in janela:
        raise SystemExit("SEM_ANUNCIO_DO_DIA")

    # Fecha overlays/banners residuais (cookies, notificacoes) que podem
    # interceptar o clique no botao "Compartilhar".
    fechar_dialogos(page)
    compartilhar = page.get_by_role("button", name="Compartilhar").first
    compartilhar.scroll_into_view_if_needed(timeout=5000)
    try:
        compartilhar.click(timeout=8000)
    except Exception:
        # Locator resolve mas o clique nao completa: normalmente um overlay
        # esta interceptando o clique. Fecha de novo e forca o clique.
        fechar_dialogos(page)
        compartilhar.click(timeout=8000, force=True)

    # Aguarda o painel de compartilhamento aparecer — FB pode usar dialog ou sheet.
    SELETORES_DIALOG = [
        "[role='dialog']",
        "[aria-modal='true']",
        "[aria-label='Compartilhar']",
        "div[data-testid='share-dialog']",
    ]
    dialog_encontrado = False
    for sel in SELETORES_DIALOG:
        try:
            page.wait_for_selector(sel, timeout=6000)
            dialog_encontrado = True
            break
        except Exception:
            pass
    if not dialog_encontrado:
        # Ultima tentativa: aguarda mais 10s e captura screenshot para diagnostico.
        page.wait_for_timeout(10000)
        page.screenshot(path=SHOT)
        # Tenta continuar mesmo sem confirmar o seletor (UI pode ter mudado).
    else:
        page.wait_for_timeout(1500)

    # Rate-limit pode aparecer logo ao abrir o dialog (bloqueia antes de "Grupo" aparecer).
    if rate_limit_grupos(page):
        page.screenshot(path=SHOT)
        raise SystemExit("RATE_LIMIT_GRUPOS")

    # Tenta encontrar a opcao "Grupo" no painel — FB alterna entre singular e plural.
    dialog = page.get_by_role("dialog")
    grupo_btn = None
    for texto_grupo in ("Grupo", "Grupos", "Group", "Groups"):
        try:
            candidato = dialog.get_by_text(texto_grupo, exact=True).first
            if candidato.count() and candidato.is_visible(timeout=2000):
                grupo_btn = candidato
                break
        except Exception:
            pass
    if grupo_btn is None:
        # Fallback: procura link/button que contenha "grupo" no texto (case-insensitive).
        try:
            grupo_btn = dialog.locator("role=button >> text=/grupo/i").first
            grupo_btn.wait_for(timeout=3000)
        except Exception:
            page.screenshot(path=SHOT)
            raise Exception("Opcao 'Grupo' nao encontrada no dialog de compartilhamento")
    grupo_btn.click(timeout=8000)

    # Aguarda o painel de grupos carregar antes de interagir.
    page.wait_for_timeout(2000)

    if rate_limit_grupos(page):
        page.screenshot(path=SHOT)
        raise SystemExit("RATE_LIMIT_GRUPOS")

    busca = page.get_by_role("dialog").locator(
        "input[aria-label='Procurar grupos'], input[placeholder='Procurar grupos']"
    ).first
    busca.click(timeout=5000)
    busca.fill(grupo, timeout=5000)

    # Aguarda resultados de busca aparecerem.
    page.wait_for_timeout(3000)

    # Selecionar o resultado que casa com o nome (primeiro item da lista).
    resultado = page.get_by_role("dialog").get_by_text(grupo, exact=False).first
    resultado.click(timeout=6000)

    # Aguarda o composer "Criar post" carregar com o botão Postar visível.
    page.wait_for_timeout(2000)

    # Composer final: caixa de texto opcional + botao Publicar.
    if mensagem:
        try:
            caixa = page.get_by_role("dialog").locator("[contenteditable='true'][role='textbox']").first
            if caixa.is_visible():
                caixa.click(timeout=3000)
                caixa.type(mensagem, delay=15)
                page.wait_for_timeout(800)
        except Exception:
            pass

    publicar = page.get_by_role("dialog").get_by_role(
        "button", name=re.compile(r"^(Postar|Publicar)$")
    ).first
    publicar.click(timeout=8000)
    page.wait_for_timeout(8000)

    # Detecta rate-limit no composer (aparece APÓS tentar postar).
    if rate_limit_grupos(page):
        page.screenshot(path=SHOT)
        fechar_dialogos(page)
        raise SystemExit("RATE_LIMIT_GRUPOS")

    # Sucesso: o composer "Criar post" sumiu (botão Postar não está mais visível).
    # O FB mantém outros dialogs na página (sidebar Marketplace) — não conta dialogs,
    # verifica se o botão Postar ainda existe no contexto de qualquer dialog.
    try:
        ainda_postar = page.get_by_role("dialog").get_by_role(
            "button", name=re.compile(r"^(Postar|Publicar)$")
        ).count()
    except Exception:
        ainda_postar = 0

    if ainda_postar:
        page.screenshot(path=SHOT)
        fechar_dialogos(page)
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="max grupos nesta rodada (0 = usa teto diario)")
    ap.add_argument("--max-dia", type=int, default=30, help="teto de posts OK por dia (saude da conta)")
    ap.add_argument("--cadence", type=int, default=420, help="segundos entre grupos (default 7 min)")
    ap.add_argument("--mensagem", default="", help="texto opcional do post")
    args = ap.parse_args()

    # Teto diario: conta os OK de hoje e publica no maximo ate o teto.
    ok_hoje = 0
    if LOG_CSV.exists():
        hoje = dt.date.today().isoformat()
        for row in csv.DictReader(LOG_CSV.open(encoding="utf-8")):
            if row["status"] == "ok" and row["data"].startswith(hoje):
                ok_hoje += 1
    restante_dia = max(0, args.max_dia - ok_hoje)

    grupos = []
    for row in csv.DictReader(GROUPS_CSV.open(encoding="utf-8")):
        nome = (row.get("nome_grupo") or row.get("grupo_nome") or row.get("nome") or "").strip()
        if nome and not ja_publicado_hoje(nome):
            grupos.append(nome)
    teto = args.limit if args.limit else restante_dia
    grupos = grupos[:teto]
    if not grupos:
        print(f"Teto diario atingido ({ok_hoje}/{args.max_dia} ok hoje) ou nada pendente.")
    print(f"Grupos a publicar nesta rodada: {len(grupos)}")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE), headless=True, viewport={"width": 1280, "height": 900}
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        ok = 0
        falha = 0
        try:
            for i, grupo in enumerate(grupos, 1):
                try:
                    sucesso = compartilhar_no_grupo(page, grupo, args.mensagem)
                except SystemExit as stop:
                    motivo = str(stop) or "sessao_invalida"
                    log_row(grupo, motivo.lower())
                    print(f"{motivo}: parando com falha segura (nao retentar hoje).")
                    break
                except Exception as e:
                    sucesso = False
                    detalhe = (str(e) or repr(e))[:150]
                    try:
                        page.screenshot(path=SHOT)
                    except Exception:
                        pass
                    fechar_dialogos(page)
                else:
                    detalhe = ""
                if sucesso:
                    ok += 1
                    log_row(grupo, "ok")
                    print(f"[{i}/{len(grupos)}] OK: {grupo}")
                else:
                    falha += 1
                    log_row(grupo, "falha", detalhe)
                    print(f"[{i}/{len(grupos)}] FALHA: {grupo} {detalhe}")
                    if falha >= 5 and ok == 0:
                        print("5 falhas seguidas sem sucesso: parando com falha segura.")
                        break
                if i < len(grupos):
                    espera = args.cadence + random.randint(-20, 25)
                    time.sleep(max(20, espera))
        finally:
            ctx.close()
        print(json.dumps({"ok": ok, "falha": falha}, ensure_ascii=False))


if __name__ == "__main__":
    main()
