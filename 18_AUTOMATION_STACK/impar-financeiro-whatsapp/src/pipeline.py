from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from .dedupe import DuplicateGuard
from .finance_client import FinanceApiClient
from .models import BridgeResult, ExtractedExpense, IncomingMessage
from .ocr import ReceiptOcr
from .transcription import AudioTranscriber

INTER_HINTS = ("banco inter", " conta inter", " no inter", " do inter", "inter ")
PF_HINTS = ("pessoal", "pf", "particular", "mercado", "casa", "uber", "ifood", "lazer")


class FinanceWhatsAppPipeline:
    def __init__(self, finance_client: FinanceApiClient | None = None) -> None:
        self.finance_client = finance_client or FinanceApiClient()
        self.ocr = ReceiptOcr()
        self.transcriber = AudioTranscriber()
        self.dedupe = DuplicateGuard()

    def process(self, message: IncomingMessage) -> BridgeResult:
        text = self._build_text(message)
        extracted = self._extract(text)
        fingerprint = self._fingerprint(message, extracted)
        extracted.fingerprint = fingerprint

        if not extracted.amount or not extracted.description:
            follow_up = self._clarification_text(message, text)
            return BridgeResult(
                status="needs_clarification",
                reply_text=follow_up,
                extracted=extracted,
                finance_payload={},
            )

        finance_payload = {
            "description": extracted.description,
            "amount": extracted.amount,
            "date": extracted.date or self._today(),
            "category": extracted.category or "Outras despesas",
            "entity": extracted.entity,
            "expenseKind": "one_off",
            "note": f"fingerprint:{fingerprint}",
            "sourceRef": message.message_id,
        }

        if self._looks_duplicate(fingerprint, message):
            return BridgeResult(
                status="duplicate",
                reply_text="Esse comprovante parece ja ter sido registrado. Quer que eu confira antes de salvar de novo?",
                extracted=extracted,
                finance_payload=finance_payload,
            )

        created = self.finance_client.create_transaction(finance_payload)
        self.dedupe.remember(fingerprint)
        return BridgeResult(
            status="confirmed",
            reply_text=self._confirmation_text(extracted, finance_payload),
            extracted=extracted,
            finance_payload={**finance_payload, "created_id": created.get("id", "")},
        )

    def _build_text(self, message: IncomingMessage) -> str:
        parts = [message.text.strip()]

        for attachment in message.attachments:
            if message.message_type == "audio" or attachment.mime_type.startswith("audio/"):
                parts.append(self.transcriber.transcribe(attachment.path))
            elif message.message_type in {"image", "pdf"} or attachment.mime_type in {
                "image/jpeg",
                "image/png",
                "application/pdf",
            }:
                parts.append(self.ocr.extract_text(attachment.path))
            else:
                parts.append(f"[anexo:{attachment.file_name}:{attachment.mime_type}]")
        return " ".join(part for part in parts if part)

    def _extract(self, text: str) -> ExtractedExpense:
        amount = self._find_amount(text)
        date = self._find_date(text)
        description = self._find_description(text)
        category = self._guess_category(text)
        entity = self._guess_entity(text)
        return ExtractedExpense(
            amount=amount,
            date=date,
            description=description,
            category=category,
            entity=entity,
        )

    def _find_amount(self, text: str) -> float:
        normalized = text.replace("BRL", "R$").replace("\n", " ")
        candidates = []
        for chunk in normalized.split():
            token = chunk.replace("R$", "").replace(".", "").replace(",", ".")
            try:
                value = float(token)
                if value > 0:
                    candidates.append(value)
            except ValueError:
                continue
        if candidates:
            return max(candidates)
        return 0.0

    def _find_date(self, text: str) -> str:
        today = self._today()
        return today

    def _find_description(self, text: str) -> str:
        lowered = text.lower()
        if any(hint in lowered for hint in INTER_HINTS):
            return "Comprovante Banco Inter"
        if "almoço" in lowered or "almoco" in lowered:
            return "Almoco"
        if "mercado" in lowered:
            return "Mercado"
        if "posto" in lowered:
            return "Combustivel"
        if "comprovante" in lowered:
            return "Comprovante de pagamento"
        words = [word for word in text.split() if any(ch.isalpha() for ch in word)]
        return " ".join(words[:4]).strip()

    def _guess_category(self, text: str) -> str:
        lowered = text.lower()
        if any(hint in lowered for hint in INTER_HINTS):
            return "Despesas operacionais"
        if "mercado" in lowered:
            return "Alimentacao"
        if "combust" in lowered:
            return "Transporte"
        if "internet" in lowered or "telefone" in lowered:
            return "Fixo"
        if "aluguel" in lowered:
            return "Fixo"
        return ""

    def _guess_entity(self, text: str) -> str:
        lowered = text.lower()
        if any(hint in lowered for hint in INTER_HINTS):
            return "pj"
        if any(hint in lowered for hint in PF_HINTS):
            return "pf"
        return "pj"

    def _confirmation_text(self, extracted: ExtractedExpense, finance_payload: dict) -> str:
        bank_hint = " Como apareceu como Banco Inter, marquei como PJ." if extracted.entity == "pj" else ""
        return (
            f"Perfeito. Registrei R$ {extracted.amount:.2f} como {finance_payload['category']}."
            f"{bank_hint} Se quiser, eu também separo por PF e PJ."
        )

    def _clarification_text(self, message: IncomingMessage, text: str) -> str:
        lowered = text.lower()
        if any(hint in lowered for hint in INTER_HINTS):
            return "Consigo ver que isso é do Banco Inter, mas ainda preciso do valor exato para salvar. Me manda o comprovante ou o valor."
        if message.message_type == "audio":
            return "Consigo ouvir seu áudio, mas ainda preciso do valor e do que foi gasto. Me fala isso em uma frase curta."
        if message.message_type in {"image", "pdf"}:
            return "Consigo ler o comprovante, mas ainda preciso entender o valor ou o tipo de gasto. Me confirma em uma frase curta?"
        return "Consigo ler sua mensagem, mas ainda preciso do valor e do que foi gasto. Me explica rapidinho?"

    def _fingerprint(self, message: IncomingMessage, extracted: ExtractedExpense) -> str:
        raw = "|".join(
            [
                message.sender,
                message.message_type,
                message.text.strip().lower(),
                f"{extracted.amount:.2f}",
                extracted.date,
                extracted.description.lower(),
            ]
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def _looks_duplicate(self, fingerprint: str, message: IncomingMessage) -> bool:
        return self.dedupe.seen(fingerprint)

    def _today(self) -> str:
        return datetime.now(timezone.utc).date().isoformat()
