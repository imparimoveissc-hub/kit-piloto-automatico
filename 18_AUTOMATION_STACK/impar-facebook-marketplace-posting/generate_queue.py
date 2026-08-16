#!/usr/bin/env python3
import csv
import html
import math
import re
import shutil
import ssl
import os
import sys
import time
import random
from datetime import date, datetime, time as datetime_time, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

try:
    from openai_enhance import enhance_title, enhance_description, enhance_tags, is_enabled as is_enhance_enabled
except ImportError:
    enhance_title = None
    enhance_description = None
    enhance_tags = None
    is_enhance_enabled = lambda: False

BASE_URL = "https://www.imparimoveis.com"
ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace"
DRAFT_DIR = OUT_DIR / "rascunhos"
PUBLICADOS_CSV = OUT_DIR / "marketplace-publicados-log.csv"
START_DATE = date.fromisoformat(os.getenv("MARKETPLACE_START_DATE", (date.today() + timedelta(days=1)).isoformat()))
START_TIME = datetime_time.fromisoformat(os.getenv("MARKETPLACE_START_TIME", "09:00"))
POST_INTERVAL_MINUTES = int(os.getenv("MARKETPLACE_INTERVAL_MINUTES", "20"))
REPOST_COOLDOWN_DAYS = int(os.getenv("MARKETPLACE_REPOST_COOLDOWN_DAYS", "30"))
SSL_CONTEXT = ssl._create_unverified_context()

TIME_SLOTS = [
    {"periodo": "manhã", "inicio": datetime_time(8, 0), "fim": datetime_time(11, 0)},
    {"periodo": "tarde", "inicio": datetime_time(13, 30), "fim": datetime_time(16, 30)},
    {"periodo": "noite", "inicio": datetime_time(18, 30), "fim": datetime_time(21, 0)},
]

def get_posts_per_day(target_date):
    is_weekend = target_date.weekday() >= 5
    if is_weekend:
        return random.randint(7, 9)
    return random.randint(8, 10)

def get_random_interval():
    return random.randint(7, 20)

def calculate_scheduled_time(day_position, total_posts, target_date):
    posts_per_period = max(1, total_posts // 3)
    period_index = min(2, (day_position - 1) // posts_per_period)
    slot = TIME_SLOTS[period_index]
    start_minutes = int(slot["inicio"].hour * 60 + slot["inicio"].minute)
    end_minutes = int(slot["fim"].hour * 60 + slot["fim"].minute)
    position_in_period = (day_position - 1) % posts_per_period
    cumulative_minutes = sum(get_random_interval() for _ in range(position_in_period))
    random_minute = random.randint(start_minutes, max(start_minutes, end_minutes - cumulative_minutes))
    return datetime_time(random_minute // 60, random_minute % 60)


def fetch(url, attempts=3):
    last_error = None
    for attempt in range(attempts):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
                    )
                },
            )
            with urlopen(req, timeout=30, context=SSL_CONTEXT) as response:
                raw = response.read()
                charset = response.headers.get_content_charset() or "iso-8859-1"
                return raw.decode(charset, errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"Falha ao acessar {url}: {last_error}")


def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def first_match(pattern, content, flags=re.I | re.S):
    match = re.search(pattern, content, flags)
    return clean_text(match.group(1)) if match else ""


def slug_to_label(value):
    parts = [part for part in value.split("-") if part]
    return " ".join(part.capitalize() for part in parts)


def extract_price_precise(content):
    """
    Extrai preço com 100% de precisão, incluindo casas decimais.
    Não usa clean_text() para manter formatação original.
    """
    # Busca no seletor info__valor (campo principal de preço)
    match = re.search(r'class=["\']info__valor["\'][^>]*>(.*?)</h2>', content, re.S)
    if match:
        price_html = match.group(1)
        # Remove tags HTML mas mantém o texto exatamente como está
        price_text = re.sub(r'<[^>]+>', '', price_html)
        # Remove espaços em branco excessivos mas mantém estrutura
        price_text = re.sub(r'\s+', ' ', price_text).strip()
        if price_text:
            return price_text

    # Fallback: tenta outros formatos comuns
    match = re.search(r'R\$\s*([\d.,]+)', content)
    if match:
        return f"R$ {match.group(1)}"

    return "[A CONFERIR]"


def discover_listing_pages(operation):
    first_url = f"{BASE_URL}/imovel/{operation}/?pag=1"
    content = fetch(first_url)
    first_page_links = extract_listing_links(content, operation)
    total_found = first_match(r'topsearch__total["\'][^>]*>\s*<strong>(\d+)</strong>', content)
    if total_found and first_page_links:
        total_pages = math.ceil(int(total_found) / len(first_page_links))
        return [f"{BASE_URL}/imovel/{operation}/?pag={page}" for page in range(1, total_pages + 1)]

    pages = {1}
    for page in re.findall(rf"/imovel/{operation}/\?pag=(\d+)", content, re.I):
        pages.add(int(page))
    return [f"{BASE_URL}/imovel/{operation}/?pag={page}" for page in range(1, max(pages) + 1)]


def extract_listing_links(content, operation):
    links = []
    seen = set()
    for path in re.findall(r'href=["\']([^"\']*/imovel/\d+/[^"\']+)["\']', content, re.I):
        if f"-{operation}-" in path:
            url = urljoin(BASE_URL, path)
            if url not in seen:
                seen.add(url)
                links.append(url)
    return links


def collect_links(operation):
    links = []
    seen = set()
    for page_url in discover_listing_pages(operation):
        content = fetch(page_url)
        for url in extract_listing_links(content, operation):
            if url not in seen:
                seen.add(url)
                links.append(url)
    return links


def extract_property(url, operation, position):
    content = fetch(url)
    slug = url.rstrip("/").split("/")[-1]
    code_match = re.search(r"/imovel/(\d+)/", url)
    code = code_match.group(1) if code_match else ""
    kind_slug = slug.split(f"-{operation}-")[0]
    rest_slug = slug.split(f"-{operation}-", 1)[1] if f"-{operation}-" in slug else ""
    city_slug = "-".join(rest_slug.split("-")[:2]) if rest_slug else ""

    name = first_match(r'itemprop=["\']name["\'][^>]*>(.*?)</span>', content)
    title = name or first_match(r"<title>(.*?)</title>", content)
    meta_description = first_match(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content
    )
    price = extract_price_precise(content)
    neighborhood = first_match(r"Bairro:\s*<b>(.*?)</b>", content)
    ref = first_match(r"<b>\s*Ref:\s*([^,<]+).*?</b>", content)
    summary_line = first_match(r"<span><b>\s*Ref:.*?</b>(.*?)</span>", content)

    image_urls = []
    # Extrair todas as URLs de imagens do site
    all_urls = re.findall(r'https?://[^\s"\'<>]+/imagens/imoveis/[^\s"\'<>]+\.(?:jpg|jpeg|png)', content, re.I)

    # Manter apenas a primeira URL por photo_id único (deduplicação sem descartar fotos)
    seen_photo_ids = set()
    for url_img in all_urls:
        id_match = re.search(r'/(\d{10,})', url_img)
        if id_match:
            photo_id = id_match.group(1)
            if photo_id not in seen_photo_ids:
                seen_photo_ids.add(photo_id)
                image_urls.append(url_img)
        elif url_img not in image_urls:
            image_urls.append(url_img)

    # Garantir og:image na primeira posição se ainda não está incluída
    og_image = first_match(r'property=["\']og:image["\']\s+content=["\'](.*?)["\']', content)
    if og_image and og_image not in image_urls:
        image_urls.insert(0, og_image)

    kind = slug_to_label(kind_slug)
    city = slug_to_label(city_slug).replace(" Sc", " SC")
    if not neighborhood and rest_slug:
        neighborhood = slug_to_label("-".join(rest_slug.split("-")[2:]))

    return {
        "codigo": code,
        "ref": ref,
        "operacao": operation,
        "tipo": kind,
        "cidade": city or "Joinville SC",
        "bairro": neighborhood or "[A CONFERIR]",
        "titulo_site": title,
        "preco": price or "[A CONFERIR]",
        "resumo_site": meta_description or summary_line or title,
        "detalhes": summary_line,
        "url": url,
        "foto_principal": image_urls[0] if image_urls else "",
        "fotos": " | ".join(image_urls[:10]),
        "ordem_na_etapa": position,
    }


def marketplace_title(prop):
    base_title = (
        f"{prop['tipo']} para locacao no {prop['bairro']} - {prop['cidade']}"
        if prop["operacao"] == "locacao"
        else f"{prop['tipo']} a venda no {prop['bairro']} - {prop['cidade']}"
    )

    if is_enhance_enabled() and enhance_title:
        enhanced = enhance_title(prop)
        if enhanced:
            return enhanced

    return base_title


def make_tags(prop):
    # Tenta OpenAI primeiro — gera 20 tags contextuais e variadas
    if is_enhance_enabled() and enhance_tags:
        ai_tags = enhance_tags(prop)
        if ai_tags:
            return ai_tags

    # Fallback local (sem OpenAI ou em caso de erro)
    operation_tags = {
        "locacao": ["locacao", "aluguel", "imovel para alugar", "alugar em joinville"],
        "venda": ["venda", "comprar imovel", "imovel a venda", "imoveis em joinville"],
    }
    base = [
        *operation_tags[prop["operacao"]],
        prop["tipo"].lower(),
        prop["bairro"].lower(),
        prop["cidade"].lower(),
        "impar imoveis",
        "joinville imoveis",
        "imobiliaria joinville",
        "oportunidade imobiliaria",
        "mercado imobiliario",
        "imovel sc",
        "santa catarina",
        "visita ao imovel",
        "negociacao imobiliaria",
        "imovel com fotos",
        "ref " + (prop["ref"].lower() if prop["ref"] else prop["codigo"]),
        "atendimento imobiliario",
        "imovel disponivel",
        "bairro " + prop["bairro"].lower(),
    ]
    cleaned = []
    for tag in base:
        tag = re.sub(r"\s+", " ", tag).strip(" ;,").lower()
        if tag and tag not in cleaned:
            cleaned.append(tag)
    while len(cleaned) < 20:
        cleaned.append(f"imovel disponivel sc {len(cleaned) + 1}")
    return "; ".join(cleaned[:20])


def make_description(prop):
    operation = "locacao" if prop["operacao"] == "locacao" else "venda"
    action = "alugar" if prop["operacao"] == "locacao" else "comprar"
    ref = prop["ref"] or prop["codigo"]
    details = prop["detalhes"] or prop["resumo_site"]

    base_description = (
        f"🏡 {marketplace_title(prop)}\n\n"
        f"Excelente opcao para quem busca {action} um imovel em {prop['bairro']}, "
        f"com localizacao em {prop['cidade']}.\n\n"
        f"💰 Valor: {prop['preco']}\n"
        f"📍 Bairro: {prop['bairro']}\n"
        f"🏷️ Referencia: {ref}\n\n"
        f"Detalhes do imovel: {details}\n\n"
        f"Quer mais informacoes ou agendar uma visita? Chame no WhatsApp e mencione a referencia {ref}.\n\n"
        f"Fonte: {prop['url']}"
    )

    if is_enhance_enabled() and enhance_description:
        enhanced = enhance_description(prop)
        if enhanced:
            return enhanced

    return base_description


def write_draft(prop, scheduled_date, day_cycle, day_position, scheduled_at):
    folder = DRAFT_DIR / prop["operacao"]
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{scheduled_date.isoformat()}_{day_position:02d}_{prop['codigo']}.md"
    path = folder / filename
    content = (
        f"# {marketplace_title(prop)}\n\n"
        f"Status: rascunho para revisao humana\n"
        f"Data sugerida: {scheduled_date.isoformat()}\n"
        f"Horario sugerido: {scheduled_at.strftime('%H:%M')}\n"
        f"Dia do ciclo: {day_cycle}\n"
        f"Posicao no dia: {day_position}\n\n"
        f"## Descricao Marketplace\n\n{make_description(prop)}\n\n"
        f"## Tags\n\n{make_tags(prop)}\n\n"
        f"## Fotos\n\n{prop['fotos'] or '[A CONFERIR]'}\n\n"
        f"## Checklist antes de publicar\n\n"
        f"- Conferir disponibilidade no site/CRM.\n"
        f"- Conferir preco, condominio, taxas e condicoes.\n"
        f"- Selecionar fotos permitidas e com boa qualidade.\n"
        f"- Publicar somente em Marketplace/grupos autorizados.\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def build_queue(locacao, venda):
    rows = []
    daily_queues = {}

    all_props = [*locacao, *venda]
    current_index = 0

    target_date = START_DATE
    while current_index < len(all_props):
        posts_today = get_posts_per_day(target_date)
        daily_queues[target_date] = posts_today

        for position in range(1, posts_today + 1):
            if current_index >= len(all_props):
                break

            prop = dict(all_props[current_index])  # cópia para não alterar o original
            prop['_queue_position'] = current_index + 1  # garante título/tags únicos por postagem
            scheduled_at = calculate_scheduled_time(position, posts_today, target_date)

            draft_path = write_draft(prop, target_date, ((current_index) // posts_today) + 1, position, scheduled_at)

            rows.append({
                "ordem_global": current_index + 1,
                "data_sugerida": target_date.isoformat(),
                "horario_sugerido": scheduled_at.strftime("%H:%M"),
                "data_hora_sugerida": datetime.combine(target_date, scheduled_at).isoformat(timespec="minutes"),
                "dia_ciclo": ((current_index) // posts_today) + 1,
                "posicao_dia": position,
                "etapa": prop["operacao"],
                "codigo_imovel": prop["codigo"],
                "referencia": prop["ref"],
                "tipo": prop["tipo"],
                "cidade": prop["cidade"],
                "bairro": prop["bairro"],
                "preco": prop["preco"],
                "titulo_sugerido": marketplace_title(prop),
                "descricao_marketplace": make_description(prop),
                "tags": make_tags(prop),
                "url_impar": prop["url"],
                "foto_principal": prop["foto_principal"],
                "fotos": prop["fotos"],
                "arquivo_rascunho": str(draft_path),
                "status_publicacao": "rascunho_revisao_humana",
                "publicado_marketplace": "nao",
                "grupos_publicados": "",
                "observacoes": "Publicacao real exige confirmacao humana.",
            })

            current_index += 1

        target_date += timedelta(days=1)

    return rows


def codigos_publicados():
    """Codigos ja publicados com sucesso (status 'ok' em marketplace-publicados-log.csv)."""
    if not PUBLICADOS_CSV.exists():
        return set()
    return {r["codigo"] for r in csv.DictReader(PUBLICADOS_CSV.open(encoding="utf-8")) if r.get("status") == "ok"}


def codigos_publicados_recentemente(cooldown_days=REPOST_COOLDOWN_DAYS):
    """Codigos publicados com sucesso dentro da janela de recarga."""
    if not PUBLICADOS_CSV.exists() or cooldown_days <= 0:
        return set()

    cutoff = datetime.now() - timedelta(days=cooldown_days)
    recentes = set()
    for row in csv.DictReader(PUBLICADOS_CSV.open(encoding="utf-8")):
        if row.get("status") != "ok":
            continue
        codigo = row.get("codigo", "").strip()
        if not codigo:
            continue
        try:
            publicado_em = datetime.fromisoformat(row.get("data", "").strip())
        except Exception:
            continue
        if publicado_em >= cutoff:
            recentes.add(codigo)
    return recentes


def collect_operation(operation):
    links = collect_links(operation)
    publicados = codigos_publicados()
    recentes = codigos_publicados_recentemente()
    props = []
    index = 0
    for url in links:
        index += 1
        code_match = re.search(r"/imovel/(\d+)/", url)
        code = code_match.group(1) if code_match else ""
        if code and (code in publicados or code in recentes):
            print(f"Pulando {operation} {index}/{len(links)}: {url} (ja publicado)")
            continue
        print(f"Coletando {operation} {index}/{len(links)}: {url}")
        prop = extract_property(url, operation, index)
        props.append(prop)
        time.sleep(0.25)
    return props


def main():
    shutil.rmtree(DRAFT_DIR / "locacao", ignore_errors=True)
    shutil.rmtree(DRAFT_DIR / "venda", ignore_errors=True)

    locacao = collect_operation("locacao")
    venda = collect_operation("venda")
    fields_inventory = [
        "codigo",
        "ref",
        "operacao",
        "tipo",
        "cidade",
        "bairro",
        "preco",
        "titulo_site",
        "resumo_site",
        "url",
        "foto_principal",
        "fotos",
        "ordem_na_etapa",
    ]
    write_csv(OUT_DIR / "imoveis-locacao.csv", locacao, fields_inventory)
    write_csv(OUT_DIR / "imoveis-venda.csv", venda, fields_inventory)

    queue = build_queue(locacao, venda)
    queue_fields = [
        "ordem_global",
        "data_sugerida",
        "horario_sugerido",
        "data_hora_sugerida",
        "dia_ciclo",
        "posicao_dia",
        "etapa",
        "codigo_imovel",
        "referencia",
        "tipo",
        "cidade",
        "bairro",
        "preco",
        "titulo_sugerido",
        "descricao_marketplace",
        "tags",
        "url_impar",
        "foto_principal",
        "fotos",
        "arquivo_rascunho",
        "status_publicacao",
        "publicado_marketplace",
        "grupos_publicados",
        "observacoes",
    ]
    write_csv(OUT_DIR / "fila-ciclo-marketplace.csv", queue, queue_fields)
    write_csv(OUT_DIR / "fila-postagens.csv", queue, queue_fields)

    avg_posts_per_day = len(queue) / max(1, len(set(row["data_sugerida"] for row in queue))) if queue else 0
    report = (
        "# Relatorio de coleta - Facebook Marketplace Impar\n\n"
        f"Data da coleta: {START_DATE.isoformat()}\n\n"
        f"- Locacao coletados: {len(locacao)}\n"
        f"- Venda coletados: {len(venda)}\n"
        f"- Total na fila: {len(queue)}\n"
        f"- Cadencia: 7-10 imoveis por dia (7-9 fins de semana, 8-10 dias uteis)\n"
        f"- Intervalo entre postagens: 7-20 minutos (aleatorio)\n"
        f"- Distribuicao: 3 periodos (manha 08:00-11:00, tarde 13:30-16:30, noite 18:30-21:00)\n"
        f"- Media de posts por dia: {avg_posts_per_day:.1f}\n"
        f"- Publicacao real: somente apos revisao/confirmacao humana.\n\n"
        "Arquivos gerados:\n"
        "- imoveis-locacao.csv\n"
        "- imoveis-venda.csv\n"
        "- fila-ciclo-marketplace.csv\n"
        "- fila-postagens.csv\n"
        "- rascunhos/locacao/\n"
        "- rascunhos/venda/\n"
    )
    (OUT_DIR / "relatorio-coleta.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)
