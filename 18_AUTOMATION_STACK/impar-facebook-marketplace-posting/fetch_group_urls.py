#!/usr/bin/env python3
"""
Coleta as URLs dos grupos do Facebook que o perfil logado participa.

Fluxo:
- abre o perfil persistente (mesmo da automacao do Marketplace);
- navega para facebook.com/groups/joins/ (lista de grupos que participa);
- rola a pagina para carregar todos;
- extrai nome + URL de cada grupo;
- casa com os nomes de grupos-aprovados.csv e preenche a coluna url_grupo.

Uso:
  python3 fetch_group_urls.py --headed          # so coleta e mostra
  python3 fetch_group_urls.py --headed --write  # coleta e grava no CSV
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "05_WORKSPACE" / "clientes" / "impar-imoveis" / "automacoes" / "facebook-marketplace"
GROUP_CATALOG = WORKSPACE / "grupos-aprovados.csv"
DEFAULT_PROFILE = WORKSPACE / "browser-profile"
DEFAULT_BROWSER_HOME = WORKSPACE / "browser-home"
OUTPUT_JSON = WORKSPACE / "grupos-descobertos.json"

JOINS_URL = "https://www.facebook.com/groups/joins/?nav_source=tab"


def normalize(text):
    """Normaliza para comparacao: minusculas, sem acentos, sem emoji/pontuacao extra."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9 ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def collect_groups(page, max_scrolls=30):
    """Rola a lista de grupos e extrai nome+href de todos os links /groups/."""
    page.goto(JOINS_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    if "login" in page.url or "checkpoint" in page.url:
        raise SystemExit("SESSAO_INVALIDA: o perfil nao esta logado no Facebook.")

    seen = {}
    stagnant = 0
    for _ in range(max_scrolls):
        links = page.eval_on_selector_all(
            'a[href*="/groups/"]',
            """els => els.map(el => ({
                href: el.href,
                text: (el.innerText || '').trim()
            }))""",
        )
        before = len(seen)
        for link in links:
            match = re.match(r"https://www\.facebook\.com/groups/([^/?]+)", link["href"])
            if not match:
                continue
            slug = match.group(1)
            if slug in {"joins", "discover", "feed", "create", "search"}:
                continue
            url = f"https://www.facebook.com/groups/{slug}/"
            name = link["text"].split("\n")[0].strip()
            if name and (url not in seen or len(name) > len(seen[url])):
                seen[url] = name

        if len(seen) == before:
            stagnant += 1
            if stagnant >= 3:
                break
        else:
            stagnant = 0

        page.mouse.wheel(0, 2500)
        page.wait_for_timeout(1200)

    return seen


def match_catalog(discovered, rows):
    """Casa nomes do catalogo com os grupos descobertos."""
    by_norm = {}
    for url, name in discovered.items():
        by_norm.setdefault(normalize(name), url)

    matched = 0
    for row in rows:
        if (row.get("url_grupo") or "").strip():
            continue
        alvo = normalize(row.get("nome_grupo", ""))
        if not alvo:
            continue
        url = by_norm.get(alvo)
        if not url:
            # fallback: containment nos dois sentidos
            for norm_name, candidate in by_norm.items():
                if alvo and norm_name and (alvo in norm_name or norm_name in alvo):
                    url = candidate
                    break
        if url:
            row["url_grupo"] = url
            matched += 1
    return matched


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--browser-home", type=Path, default=DEFAULT_BROWSER_HOME)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--write", action="store_true", help="Gravar URLs casadas no grupos-aprovados.csv")
    parser.add_argument("--system-chrome", action="store_true")
    args = parser.parse_args()

    args.browser_home.mkdir(parents=True, exist_ok=True)

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
        try:
            discovered = collect_groups(page)
        finally:
            browser.close()

    print(f"[INFO] Grupos descobertos no perfil: {len(discovered)}")
    OUTPUT_JSON.write_text(
        json.dumps([{"nome": n, "url": u} for u, n in discovered.items()], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[INFO] Lista completa salva em: {OUTPUT_JSON}")

    with GROUP_CATALOG.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    matched = match_catalog(discovered, rows)
    print(f"[INFO] URLs casadas com o catalogo: {matched}")

    if args.write:
        with GROUP_CATALOG.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        print(f"[SUCESSO] {GROUP_CATALOG} atualizado com {matched} URLs.")
    else:
        for row in rows[:25]:
            status = row.get("url_grupo") or "[SEM URL]"
            print(f"  {row.get('ordem','?'):>3} | {row.get('nome_grupo','')[:50]:<50} | {status}")
        print("[INFO] Rode com --write para gravar no CSV.")


if __name__ == "__main__":
    main()
