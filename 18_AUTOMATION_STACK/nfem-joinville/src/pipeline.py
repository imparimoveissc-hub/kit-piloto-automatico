"""
Orquestrador principal: recebe evento do Asaas e conduz emissão de NF.

Pode ser chamado via webhook (webhook_server.py) ou manualmente (cli.py).

Portal Nacional NFS-e (exclusivo): https://www.nfse.gov.br/EmissorNacional
Migração 20/07/2026: NF-em Joinville descontinuado
"""

import asyncio
from datetime import datetime
from typing import Optional

from src import asaas_client, idempotency, pdf_manager
from src.config import carregar_clientes
from src.nfse_nacional_automation import emitir_nota, emitir_notas_em_lote
from src.logger import log

log.info("Usando Portal Nacional da NFS-e para emissão (exclusivo a partir de 20/07/2026)")


def _so_digitos(valor: str) -> str:
    return "".join(ch for ch in valor if ch.isdigit())


def _encontrar_config_cliente(
    customer_id: str,
    cpf_cnpj_inquilino: str,
    nome_inquilino: str,
    valor_boleto: float = 0.0,
) -> Optional[dict]:
    """
    Busca em clientes.json o imóvel/proprietário correspondente ao pagamento.

    O cliente cadastrado no Asaas é sempre o INQUILINO (quem paga o boleto do
    aluguel), nunca o proprietário. Por isso a busca é pelo CPF/CNPJ do
    inquilino (campo inquilino_cpf_cnpj em clientes.json). Normalmente um
    inquilino não se repete em mais de um imóvel, mas quando isso acontece
    (ex: a mesma empresa aluga duas salas do mesmo locador), o valor do
    boleto pago é comparado com "valor_aluguel" de cada imóvel para
    desambiguar. Fallback por nome do inquilino é usado quando o CPF não
    está cadastrado.
    """
    clientes = carregar_clientes()
    nome_norm = nome_inquilino.upper().strip()
    cpf_i = _so_digitos(cpf_cnpj_inquilino)

    candidatos = []
    if cpf_i:
        candidatos = [c for c in clientes if _so_digitos(c.get("inquilino_cpf_cnpj") or "") == cpf_i]
    if not candidatos and nome_norm:
        candidatos = [c for c in clientes if (c.get("inquilino_nome") or "").upper().strip() == nome_norm]

    if not candidatos:
        return None
    if len(candidatos) == 1:
        return candidatos[0]

    for c in candidatos:
        valor_aluguel = c.get("valor_aluguel")
        if valor_aluguel is not None and abs(float(valor_aluguel) - valor_boleto) < 0.01:
            return c

    log.warning(
        "Inquilino %s tem %d imóveis cadastrados e o valor do boleto (R$%.2f) "
        "não bateu com nenhum valor_aluguel. Usando o primeiro encontrado — "
        "VERIFIQUE a descrição da nota antes de confiar no resultado.",
        nome_norm or cpf_i,
        len(candidatos),
        valor_boleto,
    )
    return candidatos[0]


async def processar_pagamento(payment_id: str, evento: str = "") -> dict:
    """
    Processa um pagamento e emite a NF se aplicável.
    Retorna dict com resultado.
    """
    log.info("Iniciando processamento | payment_id=%s | evento=%s", payment_id, evento)

    # 1. Idempotência
    if idempotency.ja_emitida(payment_id):
        log.info("Nota já emitida para payment_id=%s — ignorando", payment_id)
        return {"status": "ja_emitida", "payment_id": payment_id}

    # 2. Buscar dados completos no Asaas
    try:
        pagamento = asaas_client.buscar_pagamento(payment_id)
    except Exception as e:
        msg = f"Erro ao buscar pagamento no Asaas: {e}"
        log.error(msg)
        idempotency.registrar_erro(payment_id, "", 0.0, msg)
        return {"status": "erro", "payment_id": payment_id, "erro": msg}

    # 3. Verificar se status autoriza emissão
    autorizado, motivo = asaas_client.pagamento_autoriza_nota(pagamento)
    if not autorizado:
        log.info("Pagamento %s não autoriza NF: %s", payment_id, motivo)
        return {"status": "ignorado", "payment_id": payment_id, "motivo": motivo}

    # 4. Buscar dados do cliente
    customer_id = pagamento.get("customer", "")
    try:
        cliente_asaas = asaas_client.buscar_cliente(customer_id) if customer_id else {}
    except Exception as e:
        log.warning("Não foi possível buscar cliente %s: %s", customer_id, e)
        cliente_asaas = {}

    # 5. Config local do cliente (cliente Asaas = inquilino; buscamos o imóvel/proprietário)
    cpf_cnpj = cliente_asaas.get("cpfCnpj", "")
    nome = cliente_asaas.get("name", "")
    valor_boleto = float(pagamento.get("value", 0.0))
    cliente_config = _encontrar_config_cliente(customer_id, cpf_cnpj, nome, valor_boleto)

    if not cliente_config:
        log.warning(
            "Inquilino %s (%s) não encontrado em clientes.json — a nota não será emitida "
            "até que o imóvel seja cadastrado",
            nome,
            customer_id,
        )

    # 6. Montar dados da NF
    try:
        dados_nf = asaas_client.montar_dados_nota(pagamento, cliente_asaas, cliente_config)
    except ValueError as e:
        msg = f"Dados obrigatórios ausentes: {e}"
        log.error(msg)
        idempotency.registrar_erro(payment_id, nome, pagamento.get("value", 0), msg)
        return {"status": "erro", "payment_id": payment_id, "erro": msg}

    # 7. Emitir NF via Playwright (Portal Nacional ou Joinville conforme config)
    try:
        pdf_bytes, numero_nota = await emitir_nota(dados_nf)
    except Exception as e:
        msg = f"Erro na emissão da NF: {e}"
        log.error(msg)
        idempotency.registrar_erro(
            payment_id,
            dados_nf["nome_tomador"],
            dados_nf["valor_servico"],
            msg,
        )
        return {"status": "erro", "payment_id": payment_id, "erro": msg}

    # 8. Salvar PDF
    try:
        data_pag = dados_nf.get("data_pagamento", "")
        dt_emissao = datetime.fromisoformat(data_pag) if data_pag else None
        caminho = pdf_manager.salvar_pdf(
            pdf_bytes,
            dados_nf["nome_tomador"],
            payment_id,
            dt_emissao,
        )
    except Exception as e:
        msg = f"Erro ao salvar PDF: {e}"
        log.error(msg)
        idempotency.registrar_erro(
            payment_id,
            dados_nf["nome_tomador"],
            dados_nf["valor_servico"],
            msg,
        )
        return {"status": "erro", "payment_id": payment_id, "erro": msg}

    # 9. Registrar emissão bem-sucedida
    idempotency.registrar_emissao(
        payment_id=payment_id,
        cliente=dados_nf["nome_tomador"],
        valor=dados_nf["valor_servico"],
        data_pagamento=dados_nf.get("data_pagamento", ""),
        numero_nota=numero_nota,
        caminho_pdf=str(caminho),
    )

    log.info(
        "NF emitida com sucesso | payment_id=%s | cliente=%s | nota=%s | pdf=%s",
        payment_id,
        dados_nf["nome_tomador"],
        numero_nota,
        caminho,
    )

    return {
        "status": "sucesso",
        "payment_id": payment_id,
        "cliente": dados_nf["nome_tomador"],
        "valor": dados_nf["valor_servico"],
        "numero_nota": numero_nota,
        "caminho_pdf": str(caminho),
    }


async def processar_lote(payment_ids: list[str]) -> list[dict]:
    """
    Processa vários pagamentos em uma única sessão do navegador (um único
    login/captcha para todas as notas). Cada pagamento passa pelas mesmas
    validações de processar_pagamento (idempotência, status, cadastro do
    proprietário) antes de entrar na fila de emissão.

    Uma falha em uma nota não interrompe as demais.
    """
    prontos = []  # [(payment_id, dados_nf)]
    resultados: dict[str, dict] = {}

    # Fase 1: validar e montar dados de cada pagamento (sem abrir navegador)
    for payment_id in payment_ids:
        if idempotency.ja_emitida(payment_id):
            resultados[payment_id] = {"status": "ja_emitida", "payment_id": payment_id}
            continue

        try:
            pagamento = asaas_client.buscar_pagamento(payment_id)
        except Exception as e:
            msg = f"Erro ao buscar pagamento no Asaas: {e}"
            idempotency.registrar_erro(payment_id, "", 0.0, msg)
            resultados[payment_id] = {"status": "erro", "payment_id": payment_id, "erro": msg}
            continue

        autorizado, motivo = asaas_client.pagamento_autoriza_nota(pagamento)
        if not autorizado:
            resultados[payment_id] = {"status": "ignorado", "payment_id": payment_id, "motivo": motivo}
            continue

        customer_id = pagamento.get("customer", "")
        try:
            cliente_asaas = asaas_client.buscar_cliente(customer_id) if customer_id else {}
        except Exception as e:
            cliente_asaas = {}

        cpf_cnpj = cliente_asaas.get("cpfCnpj", "")
        nome = cliente_asaas.get("name", "")
        valor_boleto = float(pagamento.get("value", 0.0))
        cliente_config = _encontrar_config_cliente(customer_id, cpf_cnpj, nome, valor_boleto)

        try:
            dados_nf = asaas_client.montar_dados_nota(pagamento, cliente_asaas, cliente_config)
        except ValueError as e:
            msg = f"Dados obrigatórios ausentes: {e}"
            idempotency.registrar_erro(payment_id, nome, pagamento.get("value", 0), msg)
            resultados[payment_id] = {"status": "erro", "payment_id": payment_id, "erro": msg}
            continue

        prontos.append((payment_id, dados_nf))

    if not prontos:
        log.info("Nenhum pagamento pronto para emissão em lote")
        return [resultados[pid] for pid in payment_ids]

    # Fase 2: emitir todas as notas prontas em uma única sessão do navegador
    log.info("Iniciando emissão em lote de %d notas", len(prontos))
    lista_dados = [dados for _, dados in prontos]
    resultados_emissao = await emitir_notas_em_lote(lista_dados)

    # Fase 3: salvar PDFs e registrar idempotência
    for (payment_id, dados_nf), resultado in zip(prontos, resultados_emissao):
        if not resultado["sucesso"]:
            msg = f"Erro na emissão da NF: {resultado['erro']}"
            idempotency.registrar_erro(payment_id, dados_nf["nome_tomador"], dados_nf["valor_servico"], msg)
            resultados[payment_id] = {"status": "erro", "payment_id": payment_id, "erro": msg}
            continue

        numero_nota = resultado["numero_nota"]
        pdf_bytes = resultado["pdf_bytes"]

        try:
            data_pag = dados_nf.get("data_pagamento", "")
            dt_emissao = datetime.fromisoformat(data_pag) if data_pag else None
            caminho = pdf_manager.salvar_pdf(pdf_bytes, dados_nf["nome_tomador"], payment_id, dt_emissao)
        except Exception as e:
            msg = f"Nota {numero_nota} emitida mas erro ao salvar PDF: {e}"
            idempotency.registrar_erro(payment_id, dados_nf["nome_tomador"], dados_nf["valor_servico"], msg)
            resultados[payment_id] = {"status": "erro", "payment_id": payment_id, "erro": msg}
            continue

        idempotency.registrar_emissao(
            payment_id=payment_id,
            cliente=dados_nf["nome_tomador"],
            valor=dados_nf["valor_servico"],
            data_pagamento=dados_nf.get("data_pagamento", ""),
            numero_nota=numero_nota,
            caminho_pdf=str(caminho),
        )
        resultados[payment_id] = {
            "status": "sucesso",
            "payment_id": payment_id,
            "cliente": dados_nf["nome_tomador"],
            "valor": dados_nf["valor_servico"],
            "numero_nota": numero_nota,
            "caminho_pdf": str(caminho),
        }

    return [resultados[pid] for pid in payment_ids]
