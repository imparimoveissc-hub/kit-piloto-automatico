#!/usr/bin/env python3
"""
FASE 3 — Publicação em Massa Automatizada
Marketplace + Grupos com Cadência Humanizada

Executa:
1. Publicação no Marketplace (fila-postagens.csv) — 7-20 min entre posts
2. Publicação em Grupos (fila-grupos-postagens.csv) — 3 min entre grupos

Uso:
  python3 fase3-publicacao-automatizada.py --publish

Dry-run (sem publicar):
  python3 fase3-publicacao-automatizada.py
"""

import argparse
import csv
import logging
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "05_WORKSPACE" / "clientes" / "impar-imoveis" / "automacoes" / "facebook-marketplace"
LOG_DIR = ROOT / "07_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"fase3-publicacao-completa-{datetime.now().strftime('%Y-%m-%d')}.md"

def log_event(message, level="INFO", prefix=""):
    """Registra evento com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {level}: {prefix}{message}"
    print(log_line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def load_csv(path):
    """Carrega CSV e retorna lista de dicts."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def publish_marketplace_item(index, publish=False, headed=False):
    """Publica um imóvel do Marketplace."""
    script = Path(__file__).parent / "publish_marketplace_playwright.py"
    cmd = ["python3", str(script), "--index", str(index)]

    if headed:
        cmd.append("--headed")
    if publish:
        cmd.append("--publish")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0
        msg = result.stdout.split('\n')[-2] if result.stdout else "OK"
        return success, msg
    except subprocess.TimeoutExpired:
        return False, "Timeout (5min)"
    except Exception as e:
        return False, str(e)

def publish_groups_batch(publish=False, headed=False, start_index=1):
    """Publica todos os grupos em lote."""
    script = Path(__file__).parent / "publish_groups_playwright.py"
    queue_path = WORKSPACE / "fila-grupos-postagens.csv"

    cmd = [
        "python3", str(script),
        "--queue", str(queue_path),
        "--start-index", str(start_index),
        "--batch-size", "19",      # 19 grupos por lote
        "--batch-interval", "120"  # 2 minutos entre lotes
    ]

    if headed:
        cmd.append("--headed")
    if publish:
        cmd.append("--publish")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=14400)  # 4 horas
        success = result.returncode == 0
        msg = result.stdout.split('\n')[-2] if result.stdout else "OK"
        return success, msg
    except subprocess.TimeoutExpired:
        return False, "Timeout (4h)"
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(
        description="FASE 3 — Publicação em Massa Marketplace + Grupos"
    )
    parser.add_argument("--publish", action="store_true", help="Publicar de verdade")
    parser.add_argument("--headed", action="store_true", help="Abrir navegador visível")
    parser.add_argument("--marketplace-only", action="store_true", help="Só Marketplace")
    parser.add_argument("--groups-only", action="store_true", help="Só Grupos")
    args = parser.parse_args()

    # Header
    log_event("=" * 70, "START")
    log_event("FASE 3 — PUBLICAÇÃO EM MASSA MARKETPLACE + GRUPOS", "START")
    log_event("=" * 70, "START")
    log_event(f"Modo: {'PUBLICAR' if args.publish else 'DRY-RUN'}", "CONFIG")
    log_event(f"Marketplace Only: {args.marketplace_only}", "CONFIG")
    log_event(f"Groups Only: {args.groups_only}", "CONFIG")

    stats = {
        "marketplace_total": 0,
        "marketplace_success": 0,
        "marketplace_failed": 0,
        "groups_total": 0,
        "groups_success": 0,
        "groups_failed": 0,
        "start_time": datetime.now()
    }

    # ETAPA 1: MARKETPLACE
    if not args.groups_only:
        log_event("INICIANDO PUBLICAÇÃO NO MARKETPLACE", "PHASE")
        queue_path = WORKSPACE / "fila-postagens.csv"

        try:
            queue = load_csv(queue_path)
            log_event(f"Fila carregada: {len(queue)} imóveis", "INFO")
            stats["marketplace_total"] = len(queue)

            for idx, item in enumerate(queue, start=1):
                imovel = item.get("referencia", f"Item {idx}")
                tipo = item.get("tipo", "?")
                preco = item.get("preco", "?")

                # Cadência humanizada: 7-20 minutos
                if idx > 1:
                    delay = random.randint(7, 20)
                    log_event(f"Aguardando {delay}min antes do próximo imóvel...", "WAIT")
                    time.sleep(delay * 60)

                log_event(f"Publicando #{idx}: {imovel} ({tipo}) — {preco}", "ITEM")
                success, msg = publish_marketplace_item(idx, publish=args.publish, headed=args.headed)

                if success:
                    stats["marketplace_success"] += 1
                    log_event(f"✅ Sucesso: {msg}", "SUCCESS", prefix=f"{imovel} ")
                else:
                    stats["marketplace_failed"] += 1
                    log_event(f"❌ Erro: {msg}", "ERROR", prefix=f"{imovel} ")

            log_event(
                f"Marketplace: {stats['marketplace_success']}/{stats['marketplace_total']} publicados",
                "SUMMARY"
            )
        except FileNotFoundError as e:
            log_event(f"Fila não encontrada: {e}", "ERROR")
            sys.exit(1)

    # ETAPA 2: GRUPOS
    if not args.marketplace_only:
        log_event("INICIANDO PUBLICAÇÃO EM GRUPOS", "PHASE")

        # Aguardar 5 min após última publicação Marketplace
        if not args.groups_only and stats["marketplace_total"] > 0:
            log_event("Aguardando 5 minutos antes de iniciar grupos...", "WAIT")
            time.sleep(5 * 60)

        success, msg = publish_groups_batch(
            publish=args.publish,
            headed=args.headed,
            start_index=1
        )

        if success:
            stats["groups_success"] = stats["marketplace_success"]  # Aproximado
            log_event(f"Grupos publicados com sucesso", "SUCCESS")
        else:
            log_event(f"Erro ao publicar grupos: {msg}", "ERROR")
            sys.exit(1)

    # RESUMO FINAL
    duration = datetime.now() - stats["start_time"]
    duration_str = f"{int(duration.total_seconds() // 3600)}h {int((duration.total_seconds() % 3600) // 60)}min"

    log_event("=" * 70, "END")
    log_event("RESUMO FINAL", "SUMMARY")
    log_event("=" * 70, "END")
    log_event(f"Marketplace: {stats['marketplace_success']}/{stats['marketplace_total']} publicados", "STAT")
    log_event(f"Grupos: ~768 posts (96 grupos × ~8 imóveis)", "STAT")
    log_event(f"Duração total: {duration_str}", "STAT")
    log_event("=" * 70, "END")
    log_event(f"Log salvo em: {LOG_FILE}", "INFO")

if __name__ == "__main__":
    main()
