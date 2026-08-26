"""Controle de idempotência usando JSON persistido em disco.

Garante que a mesma cobrança do Asaas nunca gere duas notas fiscais.
"""

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.config import EMISSOES_DB
from src.logger import log


_lock = threading.Lock()


def _carregar() -> dict:
    if not EMISSOES_DB.exists():
        return {}
    with open(EMISSOES_DB, encoding="utf-8") as f:
        return json.load(f)


def _salvar(dados: dict) -> None:
    with open(EMISSOES_DB, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def ja_emitida(payment_id: str) -> bool:
    """Retorna True se já existe uma nota emitida para este pagamento."""
    with _lock:
        dados = _carregar()
        return dados.get(payment_id, {}).get("status") == "sucesso"


def registrar_emissao(
    payment_id: str,
    cliente: str,
    valor: float,
    data_pagamento: str,
    numero_nota: str,
    caminho_pdf: str,
    status: str = "sucesso",
    erro: Optional[str] = None,
) -> None:
    """Salva o registro da emissão."""
    with _lock:
        dados = _carregar()
        dados[payment_id] = {
            "cliente": cliente,
            "valor": valor,
            "data_pagamento": data_pagamento,
            "numero_nota": numero_nota,
            "caminho_pdf": caminho_pdf,
            "status": status,
            "erro": erro,
            "emitido_em": datetime.now().isoformat(),
        }
        _salvar(dados)
    log.info(
        "Emissão registrada | payment_id=%s | cliente=%s | nota=%s | status=%s",
        payment_id,
        cliente,
        numero_nota,
        status,
    )


def registrar_erro(payment_id: str, cliente: str, valor: float, erro: str) -> None:
    """Marca o pagamento como erro para permitir reprocessamento manual."""
    with _lock:
        dados = _carregar()
        # Só registra se ainda não foi bem-sucedido
        if payment_id not in dados or dados[payment_id].get("status") != "sucesso":
            dados[payment_id] = {
                "cliente": cliente,
                "valor": valor,
                "status": "erro",
                "erro": erro,
                "emitido_em": datetime.now().isoformat(),
            }
            _salvar(dados)
    log.error("Erro registrado | payment_id=%s | erro=%s", payment_id, erro)


def listar_erros() -> list[dict]:
    """Retorna todos os pagamentos que falharam na emissão."""
    dados = _carregar()
    return [
        {"payment_id": pid, **info}
        for pid, info in dados.items()
        if info.get("status") == "erro"
    ]


def resetar_para_reprocessamento(payment_id: str) -> None:
    """Remove o registro de erro para permitir nova tentativa."""
    with _lock:
        dados = _carregar()
        if payment_id in dados and dados[payment_id].get("status") == "erro":
            del dados[payment_id]
            _salvar(dados)
            log.info("Pagamento %s liberado para reprocessamento", payment_id)
