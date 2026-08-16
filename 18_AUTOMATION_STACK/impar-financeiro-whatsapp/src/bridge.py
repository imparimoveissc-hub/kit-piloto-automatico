from __future__ import annotations

from dataclasses import asdict

from .models import IncomingMessage
from .pipeline import FinanceWhatsAppPipeline


class WhatsAppFinanceBridge:
    """Adaptador da ponte WhatsApp -> OCR/transcricao -> financeiro local."""

    def __init__(self, pipeline: FinanceWhatsAppPipeline | None = None) -> None:
        self.pipeline = pipeline or FinanceWhatsAppPipeline()

    def handle_message(self, message: IncomingMessage) -> dict:
        result = self.pipeline.process(message)
        return {
            "status": result.status,
            "reply_text": result.reply_text,
            "extracted": asdict(result.extracted),
            "finance_payload": result.finance_payload,
        }
