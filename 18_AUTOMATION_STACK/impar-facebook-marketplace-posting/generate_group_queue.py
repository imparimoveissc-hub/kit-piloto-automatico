#!/usr/bin/env python3
"""Gera a fila de grupos a partir da fila diaria do Marketplace.

Regra operacional:
- usa os imoveis do dia informado (padrao: hoje);
- expande cada imovel em TODOS os grupos aprovados (sem limite);
- aplica cadencia de 3 minutos entre grupos;
- se a lista de grupos aprovados nao estiver completa, usa placeholders [A PREENCHER].

O script tambem marca a fila principal com um resumo de grupos planejados.

USO:
  # Gerar para hoje
  python3 generate_group_queue.py

  # Gerar para data especifica (após postagens de amanhã)
  python3 generate_group_queue.py 2026-07-18

  # Ou via variável de ambiente
  TARGET_DAY=2026-07-18 python3 generate_group_queue.py

Saída: fila-grupos-postagens.csv (pronta para browser/automacao de publicacao)
Obs: Cada imóvel será postado em TODOS os grupos configurados em grupos-aprovados.csv
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace"
MARKETPLACE_QUEUE = WORKSPACE / "fila-postagens.csv"
GROUP_QUEUE = WORKSPACE / "fila-grupos-postagens.csv"
GROUP_CATALOG = WORKSPACE / "grupos-aprovados.csv"

GROUP_INTERVAL_MINUTES = 3
GROUPS_PER_PROPERTY = None  # None = usar TODOS os grupos


@dataclass
class GroupTarget:
    ordem: int
    nome: str
    url: str = ""
    observacoes: str = ""


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_day(default: date | None = None) -> date:
    return default or date.today()


def parse_marketplace_datetime(row: dict[str, str], target_day: date) -> datetime:
    value = (row.get("data_hora_sugerida") or "").strip()
    if value:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            pass

    time_value = (row.get("horario_sugerido") or "09:00").strip()
    hour, minute = [int(part) for part in time_value.split(":")]
    return datetime.combine(target_day, datetime.min.time()).replace(hour=hour, minute=minute)


def load_group_catalog() -> list[GroupTarget]:
    if not GROUP_CATALOG.exists():
        GROUP_CATALOG.parent.mkdir(parents=True, exist_ok=True)
        with GROUP_CATALOG.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["ordem", "nome_grupo", "url_grupo", "observacoes"])
            for index in range(1, 20):
                writer.writerow([index, f"[A PREENCHER {index:02d}]", "", "Inserir nome/URL do grupo aprovado"])

    _, rows = load_csv(GROUP_CATALOG)
    catalog: list[GroupTarget] = []
    for fallback_index, row in enumerate(rows, start=1):
        nome = (row.get("nome_grupo") or "").strip() or f"[A PREENCHER {fallback_index:02d}]"
        url = (row.get("url_grupo") or "").strip()
        observacoes = (row.get("observacoes") or "").strip()
        catalog.append(GroupTarget(ordem=fallback_index, nome=nome, url=url, observacoes=observacoes))

    if GROUPS_PER_PROPERTY:
        return catalog[:GROUPS_PER_PROPERTY]
    return catalog


def expand_groups(target_day: date | None = None) -> list[dict[str, str]]:
    target_day = parse_day(target_day)
    marketplace_fields, marketplace_rows = load_csv(MARKETPLACE_QUEUE)
    group_catalog = load_group_catalog()

    todays_rows = [row for row in marketplace_rows if (row.get("data_sugerida") or "").strip() == target_day.isoformat()]
    if not todays_rows:
        available_dates = sorted(set(r.get("data_sugerida", "").strip() for r in marketplace_rows if r.get("data_sugerida", "").strip()))
        dates_msg = f" Datas disponíveis: {', '.join(available_dates[:5])}" if available_dates else ""
        raise SystemExit(f"Nenhum imovel encontrado em {target_day.isoformat()} na fila principal.{dates_msg}")

    group_rows: list[dict[str, str]] = []
    global_order = 1
    for marketplace_row in todays_rows:
        base_dt = parse_marketplace_datetime(marketplace_row, target_day)
        for group_index, target in enumerate(group_catalog, start=1):
            scheduled_dt = base_dt + timedelta(minutes=GROUP_INTERVAL_MINUTES * group_index)
            group_rows.append(
                {
                    "ordem_global": str(global_order),
                    "data_sugerida": scheduled_dt.date().isoformat(),
                    "horario_sugerido": scheduled_dt.strftime("%H:%M"),
                    "data_hora_sugerida": scheduled_dt.isoformat(timespec="minutes"),
                    "dia_ciclo": marketplace_row.get("dia_ciclo", ""),
                    "posicao_dia": marketplace_row.get("posicao_dia", ""),
                    "codigo_imovel": marketplace_row.get("codigo_imovel", ""),
                    "referencia": marketplace_row.get("referencia", ""),
                    "titulo_sugerido": marketplace_row.get("titulo_sugerido", ""),
                    "grupo_ordem": str(target.ordem),
                    "grupo_nome": target.nome,
                    "grupo_url": target.url,
                    "grupo_estado": "aguardando_confirmacao_humana" if target.nome.startswith("[A PREENCHER") else "pronto_para_publicar",
                    "status_publicacao": "rascunho_revisao_humana" if not target.nome.startswith("[A PREENCHER") else "aguardando_lista_de_grupos",
                    "observacoes": "Cadencia de 3 minutos por grupo. Nao publicar em massa sem aprovacao humana.",
                }
            )
            global_order += 1

    updated_marketplace_rows: list[dict[str, str]] = []
    for row in marketplace_rows:
        if (row.get("data_sugerida") or "").strip() == target_day.isoformat():
            row = dict(row)
            row["grupos_publicados"] = "19 planejados em fila-grupos-postagens.csv"
            current_notes = (row.get("observacoes") or "").strip()
            extra_note = "Grupos planejados em fila separada com cadencia de 3 minutos."
            row["observacoes"] = f"{current_notes} {extra_note}".strip()
        updated_marketplace_rows.append(row)

    if marketplace_fields:
        write_csv(MARKETPLACE_QUEUE, marketplace_fields, updated_marketplace_rows)

    group_fields = [
        "ordem_global",
        "data_sugerida",
        "horario_sugerido",
        "data_hora_sugerida",
        "dia_ciclo",
        "posicao_dia",
        "codigo_imovel",
        "referencia",
        "titulo_sugerido",
        "grupo_ordem",
        "grupo_nome",
        "grupo_url",
        "grupo_estado",
        "status_publicacao",
        "observacoes",
    ]
    write_csv(GROUP_QUEUE, group_fields, group_rows)
    return group_rows


def main() -> None:
    import os
    import sys

    day_arg = os.getenv("TARGET_DAY", "").strip()
    if not day_arg:
        day_arg = sys.argv[1] if len(sys.argv) > 1 else ""

    if day_arg:
        try:
            target_day = date.fromisoformat(day_arg)
        except ValueError:
            print(f"Erro: data inválida '{day_arg}'. Use formato YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        target_day = date.today()

    print(f"[INFO] Gerando fila de grupos para {target_day.isoformat()}...")

    try:
        if not MARKETPLACE_QUEUE.exists():
            print(
                f"Erro: fila do Marketplace nao encontrada em {MARKETPLACE_QUEUE}",
                file=sys.stderr
            )
            sys.exit(1)

        group_rows = expand_groups(target_day)

        total_grupos = len(set(r['grupo_ordem'] for r in group_rows))
        total_imoveis = len(set(r['codigo_imovel'] for r in group_rows))

        print(
            f"[SUCESSO] Fila de grupos gerada: {len(group_rows)} publicacoes "
            f"em {total_grupos} grupos × {total_imoveis} imoveis."
        )
        print(f"[INFO] Arquivo salvo em: {GROUP_QUEUE}")

        pending_count = sum(1 for r in group_rows if r.get("grupo_nome", "").startswith("[A PREENCHER"))
        if pending_count > 0:
            print(f"[AVISO] {pending_count} grupos ainda com placeholders — preencher grupos-aprovados.csv")

    except SystemExit as e:
        print(f"[ERRO] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO INESPERADO] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
