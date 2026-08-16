"""Cliente HTTP para a API do Asaas."""

import hmac
import hashlib
from typing import Optional

import httpx

from src.config import ASAAS_API_KEY, ASAAS_BASE_URL, ASAAS_WEBHOOK_TOKEN
from src.logger import log

# Status de pagamento que autorizam emissão de NF
STATUS_AUTORIZADOS = {"CONFIRMED", "RECEIVED"}


def validar_assinatura_webhook(payload: bytes, assinatura_recebida: str) -> bool:
    """Valida HMAC-SHA256 do webhook Asaas, se token configurado."""
    if not ASAAS_WEBHOOK_TOKEN:
        log.warning("ASAAS_WEBHOOK_TOKEN não configurado — assinatura não validada")
        return True

    esperada = hmac.new(
        ASAAS_WEBHOOK_TOKEN.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(esperada, assinatura_recebida)


def _headers() -> dict:
    return {
        "access_token": ASAAS_API_KEY,
        "Content-Type": "application/json",
    }


def buscar_pagamento(payment_id: str) -> dict:
    """Busca dados completos de um pagamento pelo ID."""
    url = f"{ASAAS_BASE_URL}/payments/{payment_id}"
    with httpx.Client(timeout=30) as client:
        r = client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json()


def buscar_cliente(customer_id: str) -> dict:
    """Busca dados do cliente pelo ID."""
    url = f"{ASAAS_BASE_URL}/customers/{customer_id}"
    with httpx.Client(timeout=30) as client:
        r = client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json()


def pagamento_autoriza_nota(pagamento: dict) -> tuple[bool, str]:
    """
    Retorna (True, "") se o pagamento autoriza emissão de NF.
    Retorna (False, motivo) caso contrário.
    """
    status = pagamento.get("status", "")
    if status not in STATUS_AUTORIZADOS:
        return False, f"Status '{status}' não autoriza emissão (aguarda CONFIRMED/RECEIVED)"

    billing_type = pagamento.get("billingType", "")
    # NF pode ser emitida para qualquer forma de pagamento confirmada
    return True, ""


def montar_dados_nota(pagamento: dict, cliente_asaas: dict, cliente_config: Optional[dict]) -> dict:
    """
    Combina dados do Asaas + config local para montar todos os campos da NF-em.

    IMPORTANTE: o cliente cadastrado no Asaas (cliente_asaas) é o INQUILINO —
    quem paga o boleto do aluguel. Mas o TOMADOR da nota fiscal é o
    PROPRIETÁRIO do imóvel, que só existe em clientes.json (cliente_config).
    Por isso os dados do tomador vêm exclusivamente de cliente_config — nunca
    de cliente_asaas — para nunca emitir a nota para a pessoa errada.
    """
    if cliente_config is None:
        nome_inquilino = cliente_asaas.get("name", "")
        raise ValueError(
            f"Proprietário não encontrado em clientes.json para o inquilino "
            f"'{nome_inquilino}' (CPF/CNPJ {cliente_asaas.get('cpfCnpj', '?')}). "
            "Cadastre o imóvel em config/clientes.json antes de emitir — "
            "a nota NÃO pode ser emitida para o inquilino."
        )

    cfg = cliente_config

    # Dados do tomador — exclusivamente do clientes.json (o proprietário)
    nome = cfg.get("nome_tomador", "")
    cpf_cnpj = cfg.get("cpf_cnpj", "")
    endereco = cfg.get("endereco", "")
    numero = cfg.get("numero", "")
    complemento = cfg.get("complemento", "")
    bairro = cfg.get("bairro", "")
    municipio = cfg.get("municipio", "Joinville")
    uf = cfg.get("uf", "SC")
    cep = cfg.get("cep", "")

    # Valor do serviço: usa o valor_referencia cadastrado (a comissão), NÃO o
    # valor do boleto pago pelo inquilino — o aluguel não é o valor da nota.
    valor = cfg.get("valor_referencia")
    if valor is None:
        raise ValueError(f"Campo 'valor_referencia' ausente em clientes.json para '{nome}'")

    # Descrição
    descricao = cfg.get("descricao_servico", "")

    data_pagamento = pagamento.get("paymentDate") or pagamento.get("confirmedDate") or ""

    campos_obrigatorios = {
        "nome_tomador": nome,
        "cpf_cnpj": cpf_cnpj,
        "valor": valor,
    }
    ausentes = [k for k, v in campos_obrigatorios.items() if not v]
    if ausentes:
        raise ValueError(f"Campos obrigatórios ausentes em clientes.json: {ausentes}")

    return {
        "payment_id": pagamento["id"],
        "customer_id": pagamento.get("customer", ""),
        # Tomador (proprietário)
        "nome_tomador": nome,
        "cpf_cnpj": cpf_cnpj,
        "endereco": endereco,
        "numero": numero,
        "complemento": complemento,
        "bairro": bairro,
        "municipio": municipio,
        "uf": uf,
        "cep": cep,
        # Reforço de cadastro — usado só se o NF-em tiver o CEP do tomador em
        # branco no próprio cadastro (bloqueia a emissão sem isso)
        "cep_tomador": cfg.get("cep_tomador", ""),
        "endereco_tomador": cfg.get("endereco_tomador", ""),
        "numero_tomador": cfg.get("numero_tomador", ""),
        "bairro_tomador": cfg.get("bairro_tomador", ""),
        "complemento_tomador": cfg.get("complemento_tomador", ""),
        # Serviço
        "descricao_servico": descricao,
        "valor_servico": float(valor),
        # Pagamento
        "data_pagamento": data_pagamento,
    }
