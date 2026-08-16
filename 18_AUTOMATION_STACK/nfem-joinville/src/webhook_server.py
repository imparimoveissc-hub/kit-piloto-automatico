"""
Servidor FastAPI que recebe webhooks do Asaas e dispara o pipeline de emissão.

Endpoint: POST /webhook/asaas
"""

import asyncio
import hmac
import hashlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from src.config import ASAAS_WEBHOOK_TOKEN
from src.logger import log
from src.pipeline import processar_pagamento

# Eventos do Asaas que autorizam emissão de NF
EVENTOS_PAGAMENTO = {
    "PAYMENT_CONFIRMED",
    "PAYMENT_RECEIVED",
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Servidor webhook iniciado — aguardando eventos do Asaas")
    yield
    log.info("Servidor webhook encerrado")


app = FastAPI(title="NF-em Joinville — Webhook Asaas", lifespan=lifespan)


def _validar_assinatura(payload: bytes, assinatura: str) -> bool:
    if not ASAAS_WEBHOOK_TOKEN:
        return True  # sem token configurado, aceita qualquer requisição
    esperada = hmac.new(
        ASAAS_WEBHOOK_TOKEN.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(esperada, assinatura)


@app.post("/webhook/asaas")
async def webhook_asaas(request: Request, background: BackgroundTasks):
    payload = await request.body()

    # Valida assinatura Asaas (header Asaas-Signature ou x-asaas-signature)
    assinatura = (
        request.headers.get("Asaas-Signature")
        or request.headers.get("x-asaas-signature")
        or ""
    )
    if ASAAS_WEBHOOK_TOKEN and not _validar_assinatura(payload, assinatura):
        log.warning("Assinatura inválida no webhook — requisição rejeitada")
        raise HTTPException(status_code=401, detail="Assinatura inválida")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Corpo JSON inválido")

    evento = body.get("event", "")
    payment = body.get("payment", {})
    payment_id = payment.get("id", "")

    log.info("Webhook recebido | evento=%s | payment_id=%s", evento, payment_id)

    if evento not in EVENTOS_PAGAMENTO:
        log.info("Evento '%s' ignorado — não é pagamento confirmado", evento)
        return JSONResponse({"status": "ignorado", "motivo": f"evento '{evento}' não processado"})

    if not payment_id:
        raise HTTPException(status_code=400, detail="payment.id ausente no payload")

    # Processa em background para retornar 200 imediatamente ao Asaas
    background.add_task(_processar_em_background, payment_id, evento)

    return JSONResponse({"status": "recebido", "payment_id": payment_id})


async def _processar_em_background(payment_id: str, evento: str) -> None:
    try:
        resultado = await processar_pagamento(payment_id, evento)
        log.info("Resultado do processamento: %s", resultado)
    except Exception as e:
        log.error("Erro inesperado ao processar payment_id=%s: %s", payment_id, e)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/erros")
async def listar_erros():
    from src.idempotency import listar_erros
    return {"erros": listar_erros()}


@app.post("/reprocessar/{payment_id}")
async def reprocessar(payment_id: str, background: BackgroundTasks):
    from src.idempotency import resetar_para_reprocessamento, listar_erros
    erros = {e["payment_id"] for e in listar_erros()}
    if payment_id not in erros:
        raise HTTPException(status_code=404, detail="Payment ID não encontrado nos erros")
    resetar_para_reprocessamento(payment_id)
    background.add_task(_processar_em_background, payment_id, "REPROCESSAMENTO_MANUAL")
    return {"status": "reprocessando", "payment_id": payment_id}
