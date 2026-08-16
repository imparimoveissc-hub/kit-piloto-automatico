#!/usr/bin/env python3
"""
Publica anúncios do Marketplace apenas no período noturno (18:30-21:00) de hoje.
Registra cada tentativa de publicação e resultado no log.
"""

import json
import subprocess
import sys
from datetime import datetime, date, time as datetime_time
from pathlib import Path
import logging

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace"
LOG_DIR = ROOT / "07_LOGS"
LOG_FILE = LOG_DIR / "marketplace-evening-publicacoes.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

EVENING_START = datetime_time(18, 30)
EVENING_END = datetime_time(21, 0)

def load_queue():
    queue_path = OUT_DIR / "fila-postagens.csv"
    if not queue_path.exists():
        logger.error(f"Fila não encontrada: {queue_path}")
        return []

    import csv
    with open(queue_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def filter_evening_posts(queue):
    today = date.today()
    evening_posts = []

    for item in queue:
        scheduled_date_str = item.get('data_sugerida', '')
        scheduled_time_str = item.get('horario_sugerido', '')

        if scheduled_date_str != today.isoformat():
            continue

        try:
            scheduled_time = datetime_time.fromisoformat(scheduled_time_str)
            if EVENING_START <= scheduled_time <= EVENING_END:
                evening_posts.append(item)
        except ValueError:
            continue

    return sorted(evening_posts, key=lambda x: x.get('horario_sugerido', ''))

def publish_listing(index, listing_data):
    try:
        publisher_path = Path(__file__).parent / "publish_marketplace_playwright.py"
        if not publisher_path.exists():
            return False, f"Publisher script não encontrado: {publisher_path}"

        result = subprocess.run(
            [
                "python3",
                str(publisher_path),
                "--index", str(index),
                "--headed",
                "--publish"
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                if output.get("ok"):
                    return True, f"Publicado com sucesso - URL: {output.get('url', 'N/A')}"
            except json.JSONDecodeError:
                pass
            return True, "Publicação completada"
        else:
            return False, f"Erro na execução: {result.stderr}"

    except subprocess.TimeoutExpired:
        return False, "Timeout na publicação (>120s)"
    except Exception as e:
        return False, str(e)

def main():
    logger.info("=" * 80)
    logger.info(f"INÍCIO - Programação noturna de {date.today()}")
    logger.info("=" * 80)

    queue = load_queue()
    if not queue:
        logger.warning("Nenhuma fila de publicação encontrada")
        return 1

    evening_posts = filter_evening_posts(queue)
    if not evening_posts:
        logger.info(f"Nenhum anúncio programado para o período noturno ({EVENING_START.strftime('%H:%M')}-{EVENING_END.strftime('%H:%M')}) de hoje")
        return 0

    logger.info(f"Encontrados {len(evening_posts)} anúncios para publicar hoje à noite")
    logger.info("-" * 80)

    success_count = 0
    failed_count = 0

    for i, post in enumerate(evening_posts, 1):
        scheduled_time = post.get('horario_sugerido', 'N/A')
        codigo = post.get('codigo_imovel', 'N/A')
        titulo = post.get('titulo_sugerido', 'N/A')
        ordem_global = post.get('ordem_global', '?')

        logger.info(f"\n[{i}/{len(evening_posts)}] {scheduled_time} | Ref: {codigo}")
        logger.info(f"       Título: {titulo}")
        logger.info(f"       Ordem global: {ordem_global}")

        success, message = publish_listing(ordem_global, post)

        if success:
            logger.info(f"       ✓ SUCESSO - {message}")
            success_count += 1
        else:
            logger.error(f"       ✗ FALHA - {message}")
            failed_count += 1

    logger.info("\n" + "=" * 80)
    logger.info(f"RESUMO - Noite de {date.today()}")
    logger.info(f"  Totais: {len(evening_posts)} anúncios programados")
    logger.info(f"  Sucesso: {success_count}")
    logger.info(f"  Falhas: {failed_count}")
    logger.info("=" * 80)

    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("\nInterrompido pelo usuário")
        sys.exit(130)
    except Exception as exc:
        logger.exception(f"Erro fatal: {exc}")
        sys.exit(1)
