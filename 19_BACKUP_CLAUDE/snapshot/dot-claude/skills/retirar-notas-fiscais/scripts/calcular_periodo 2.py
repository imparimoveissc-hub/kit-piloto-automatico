#!/usr/bin/env python3
"""
Calcula o período vigente para retirada de notas fiscais.
Dias de corte configurados: 20, 25, 29, 30 de cada mês.
"""

from datetime import date, timedelta
import json
import sys

DIAS_CORTE = [20, 25, 29, 30]

def ultimo_dia_mes(ano, mes):
    if mes == 12:
        return date(ano + 1, 1, 1) - timedelta(days=1)
    return date(ano, mes + 1, 1) - timedelta(days=1)

def ajustar_dia(ano, mes, dia):
    """Ajusta dia para o último dia do mês se necessário (ex: fev não tem dia 29/30)."""
    ultimo = ultimo_dia_mes(ano, mes).day
    return min(dia, ultimo)

def cortes_do_mes(ano, mes):
    """Retorna as datas de corte reais de um determinado mês."""
    datas = []
    for d in DIAS_CORTE:
        dia_real = ajustar_dia(ano, mes, d)
        dt = date(ano, mes, dia_real)
        if dt not in datas:
            datas.append(dt)
    return sorted(datas)

def calcular_periodo(hoje=None):
    if hoje is None:
        hoje = date.today()

    # Busca todos os cortes do mês atual e anterior para montar janelas
    cortes = []
    for delta_mes in [-1, 0, 1]:
        mes = hoje.month + delta_mes
        ano = hoje.year
        if mes <= 0:
            mes += 12
            ano -= 1
        elif mes > 12:
            mes -= 12
            ano += 1
        cortes += cortes_do_mes(ano, mes)

    cortes = sorted(set(cortes))

    # Encontra o corte imediatamente anterior ou igual a hoje (início do período vigente)
    inicio = None
    fim = None
    for i, c in enumerate(cortes):
        if c <= hoje:
            inicio = c
            fim = cortes[i + 1] - timedelta(days=1) if i + 1 < len(cortes) else None
        else:
            if inicio is None:
                # hoje está antes do primeiro corte conhecido
                inicio = cortes[0]
                fim = c - timedelta(days=1)
            break

    # Próximo corte
    proximo = None
    for c in cortes:
        if c > hoje:
            proximo = c
            break

    resultado = {
        "hoje": hoje.isoformat(),
        "periodo_inicio": inicio.isoformat() if inicio else None,
        "periodo_fim": fim.isoformat() if fim else None,
        "proximo_corte": proximo.isoformat() if proximo else None,
        "dias_ate_proximo_corte": (proximo - hoje).days if proximo else None,
        "dias_corte_configurados": DIAS_CORTE,
        "descricao": (
            f"Período vigente: {inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}"
            if inicio and fim else
            f"Período a partir de {inicio.strftime('%d/%m/%Y')}" if inicio else "Período indeterminado"
        )
    }

    return resultado

if __name__ == "__main__":
    hoje = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    r = calcular_periodo(hoje)
    print(json.dumps(r, ensure_ascii=False, indent=2))
