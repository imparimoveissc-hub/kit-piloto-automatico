#!/usr/bin/env python3
"""Gera fila SOMENTE de imoveis a VENDA do site imparimoveis.com.

Fonte: https://www.imparimoveis.com/imovel/venda (todas as paginas).
Saida: fila-postagens-venda.csv (7-10/dia a partir de hoje) + imoveis-venda.csv.
Reusa as funcoes do generate_queue.py sem reordenacao extra.
"""
import os
from datetime import date

os.environ.setdefault("MARKETPLACE_START_DATE", date.today().isoformat())

import generate_queue as gq  # noqa: E402


def main():
    venda = gq.collect_operation("venda")

    fields_inventory = [
        "codigo", "ref", "operacao", "tipo", "cidade", "bairro", "preco",
        "titulo_site", "resumo_site", "url", "foto_principal", "fotos", "ordem_na_etapa",
    ]
    gq.write_csv(gq.OUT_DIR / "imoveis-venda.csv", venda, fields_inventory)

    queue = gq.build_queue([], venda)
    queue_fields = [
        "ordem_global", "data_sugerida", "horario_sugerido", "data_hora_sugerida",
        "dia_ciclo", "posicao_dia", "etapa", "codigo_imovel", "referencia", "tipo",
        "cidade", "bairro", "preco", "titulo_sugerido", "descricao_marketplace",
        "tags", "url_impar", "foto_principal", "fotos", "arquivo_rascunho",
        "status_publicacao", "publicado_marketplace", "grupos_publicados", "observacoes",
    ]
    gq.write_csv(gq.OUT_DIR / "fila-postagens-venda.csv", queue, queue_fields)
    print(f"Imoveis a venda coletados: {len(venda)}")
    print(f"Fila venda: {gq.OUT_DIR / 'fila-postagens-venda.csv'} ({len(queue)} linhas)")


if __name__ == "__main__":
    main()
