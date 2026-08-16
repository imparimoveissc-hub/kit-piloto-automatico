#!/usr/bin/env python3
"""Publica no Marketplace os imoveis do DIA a partir da fila-postagens.csv.

Fonte: fila gerada por generate_queue.py (site imparimoveis.com, 7-10/dia).
Regras:
- Publica apenas linhas com data_sugerida == hoje e horario ja vencido (--due).
- Cooldown de 20 dias: imovel postado com sucesso so volta a fila apos 20 dias.
- Override manual (ordem por escrito): --force-codigos COD1,COD2
- Ordem 100% sequencial da fila.
- Fotos sao baixadas do site para uploads-diario/<codigo>/.
- Falha segura: para em login/checkpoint/bloqueio temporario.

Uso:
  python3 publish_daily_from_fila.py --due --publish               # rotina horaria
  python3 publish_daily_from_fila.py --due --publish --max 2       # cap por rodada
  python3 publish_daily_from_fila.py --due --publish \\
    --force-codigos AP123,AP456                                     # override manual
"""
import argparse
import csv
import datetime as dt
import json
import random
import re
import ssl
import time
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen

from playwright.sync_api import sync_playwright

from publish_marketplace_playwright import fill_listing, fill_listing_item, maybe_publish

TIPOS_IMOVEL_RESIDENCIAL = ("apartamento", "casa", "sobrado")
COOLDOWN_PADRAO_DIAS = 20

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace"
FILA_CSV = OUT_DIR / "fila-postagens.csv"
PUBLICADOS_CSV = OUT_DIR / "marketplace-publicados-log.csv"
PROFILE = OUT_DIR / "browser-profile"
UPLOADS = OUT_DIR / "uploads-diario"
SSL_CONTEXT = ssl._create_unverified_context()


def codigos_bloqueados(cooldown_dias: int = COOLDOWN_PADRAO_DIAS, forcar: Optional[set] = None) -> set:
    """Retorna códigos publicados com sucesso nos últimos `cooldown_dias` dias.

    Um imóvel só pode ser repostado após o cooldown. Para postar antes do prazo,
    passe os códigos em `forcar` (requer ordem manual por escrito via --force-codigos).
    """
    forcar = forcar or set()
    if not PUBLICADOS_CSV.exists():
        return set()
    corte = dt.date.today() - dt.timedelta(days=cooldown_dias)
    bloqueados = set()
    for r in csv.DictReader(PUBLICADOS_CSV.open(encoding="utf-8")):
        if r.get("status") != "ok":
            continue
        if r.get("codigo") in forcar:
            continue
        try:
            data_post = dt.date.fromisoformat(r["data"][:10])
        except (ValueError, KeyError):
            continue
        if data_post >= corte:
            bloqueados.add(r["codigo"])
    return bloqueados


def log_publicado(codigo, titulo, status, detalhe=""):
    novo = not PUBLICADOS_CSV.exists()
    with PUBLICADOS_CSV.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["data", "codigo", "titulo", "status", "detalhe"])
        w.writerow([dt.datetime.now().isoformat(timespec="seconds"), codigo, titulo, status, detalhe[:150]])


def baixar_fotos(row, max_fotos=10):
    codigo = row["codigo_imovel"]
    destino = UPLOADS / codigo
    destino.mkdir(parents=True, exist_ok=True)
    urls = []
    for campo in ("foto_principal", "fotos"):
        bruto = row.get(campo) or ""
        urls += re.findall(r"https?://[^\s,;'\"\]]+\.(?:jpg|jpeg|png)", bruto, re.I)

    # Filtrar por ID único: manter apenas primeira URL de cada ID
    seen_ids = set()
    unique_urls = []
    for url in urls:
        id_match = re.search(r'/(\d{10,})', url)
        if id_match:
            photo_id = id_match.group(1)
            if photo_id not in seen_ids:
                seen_ids.add(photo_id)
                unique_urls.append(url)
        else:
            # URLs sem ID numérico, manter se não temos muitas já
            if len(unique_urls) < max_fotos:
                unique_urls.append(url)

    # Manter apenas até max_fotos
    unique_urls = unique_urls[:max_fotos]

    locais = []
    for i, url in enumerate(unique_urls):
        alvo = destino / f"{i:02d}{Path(url).suffix.lower()}"
        if not alvo.exists():
            try:
                req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urlopen(req, timeout=30, context=SSL_CONTEXT) as resp:
                    alvo.write_bytes(resp.read())
            except Exception:
                continue
        if alvo.exists() and alvo.stat().st_size > 1000:
            locais.append(str(alvo))
    return locais


def bloqueado(page):
    try:
        texto = page.evaluate("() => document.body.innerText.slice(0, 4000)").lower()
        return "bloqueado temporariamente" in texto
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fila", type=Path, default=FILA_CSV, help="CSV da fila (default fila-postagens.csv)")
    ap.add_argument("--due", action="store_true", help="somente horarios ja vencidos de hoje")
    ap.add_argument("--publish", action="store_true", help="publicar de verdade")
    ap.add_argument("--max", type=int, default=2, help="max publicacoes por rodada")
    ap.add_argument("--headed", action="store_true")
    ap.add_argument(
        "--cooldown", type=int, default=COOLDOWN_PADRAO_DIAS,
        help=f"dias minimos entre postagens do mesmo imovel (padrao {COOLDOWN_PADRAO_DIAS})",
    )
    ap.add_argument(
        "--force-codigos", default="",
        help="ORDEM MANUAL: codigos separados por virgula que ignoram o cooldown nesta rodada",
    )
    args = ap.parse_args()

    forcar = {c.strip() for c in args.force_codigos.split(",") if c.strip()}
    if forcar:
        print(f"[OVERRIDE MANUAL] Cooldown ignorado para: {', '.join(sorted(forcar))}")

    hoje = dt.date.today().isoformat()
    agora = dt.datetime.now().strftime("%H:%M")
    bloqueados = codigos_bloqueados(cooldown_dias=args.cooldown, forcar=forcar)

    rows = [r for r in csv.DictReader(args.fila.open(encoding="utf-8")) if r["data_sugerida"] == hoje]
    if args.due:
        rows = [r for r in rows if r["horario_sugerido"] <= agora]
    rows = [r for r in rows if r["codigo_imovel"] not in bloqueados]
    rows = rows[: args.max]
    print(
        f"Pendentes nesta rodada: {len(rows)} "
        f"(hoje={hoje} agora={agora} cooldown={args.cooldown}d bloqueados={len(bloqueados)})"
    )
    if not rows:
        return

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(PROFILE), headless=not args.headed, viewport={"width": 1280, "height": 900}
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            for i, row in enumerate(rows):
                fotos = baixar_fotos(row)
                if not fotos:
                    log_publicado(row["codigo_imovel"], row["titulo_sugerido"], "sem_fotos")
                    print(f"SEM FOTOS: {row['codigo_imovel']}")
                    continue
                listing = {
                    "codigo": row["codigo_imovel"],
                    "tipo": row["tipo"],
                    "titulo": row["titulo_sugerido"],
                    "preco": row["preco"],
                    "cidade": (row.get("cidade") or "Joinville").split("-")[0].strip(),
                    "descricao": row["descricao_marketplace"],
                    "url": row["url_impar"],
                    "fotos": fotos,
                }
                # Regra (Jonata 19/07): VENDA sempre como ITEM (titulo custom +
                # categoria Diversos). Fluxo residencial so para LOCACAO de
                # apartamento/casa/sobrado.
                operacao = (row.get("etapa") or "").lower()
                residencial = "venda" not in operacao and any(
                    t in listing["tipo"].lower() for t in TIPOS_IMOVEL_RESIDENCIAL
                )
                try:
                    if residencial:
                        fill_listing(page, listing)
                    else:
                        fill_listing_item(page, listing)
                    if bloqueado(page):
                        log_publicado(listing["codigo"], listing["titulo"], "bloqueio_temporario")
                        print("BLOQUEIO_TEMPORARIO: parando.")
                        break
                    maybe_publish(page, args.publish)
                    status = "ok" if args.publish else "revisao"
                    log_publicado(listing["codigo"], listing["titulo"], status)
                    print(f"[{i+1}/{len(rows)}] {status.upper()}: {listing['codigo']} {listing['titulo'][:50]}")
                except Exception as e:
                    log_publicado(listing["codigo"], listing["titulo"], "falha", str(e))
                    print(f"[{i+1}/{len(rows)}] FALHA: {listing['codigo']} {e}")
                    if bloqueado(page):
                        print("BLOQUEIO_TEMPORARIO: parando.")
                        break
                if i < len(rows) - 1:
                    time.sleep(random.randint(45, 120))
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
