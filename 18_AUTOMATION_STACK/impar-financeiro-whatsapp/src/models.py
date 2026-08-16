from dataclasses import dataclass, field
from typing import Literal


MessageType = Literal["text", "audio", "image", "pdf", "mixed"]
DecisionStatus = Literal["confirmed", "needs_clarification", "duplicate", "blocked"]
EntityType = Literal["pj", "pf"]


@dataclass(slots=True)
class Attachment:
    file_name: str
    mime_type: str
    path: str


@dataclass(slots=True)
class IncomingMessage:
    message_id: str
    sender: str
    message_type: MessageType
    text: str = ""
    attachments: list[Attachment] = field(default_factory=list)
    timestamp: str = ""


@dataclass(slots=True)
class ExtractedExpense:
    amount: float = 0.0
    date: str = ""
    description: str = ""
    category: str = ""
    entity: EntityType = "pj"
    fingerprint: str = ""


@dataclass(slots=True)
class BridgeResult:
    status: DecisionStatus
    reply_text: str
    extracted: ExtractedExpense
    finance_payload: dict

