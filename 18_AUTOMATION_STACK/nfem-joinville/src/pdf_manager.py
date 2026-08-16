"""Gerencia salvamento dos PDFs de notas fiscais."""

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.config import NOTAS_BASE_DIR
from src.logger import log


def _sanitizar_nome(nome: str) -> str:
    """Remove caracteres inválidos para nomes de arquivo."""
    nome = nome.upper()
    # Remove caracteres especiais, mantém letras, números, espaços e hífens
    nome = re.sub(r"[^\w\s\-]", "", nome, flags=re.UNICODE)
    nome = re.sub(r"\s+", " ", nome).strip()
    return nome


def _pasta_mes_ano(data_emissao: Optional[datetime] = None) -> Path:
    """Retorna e cria a pasta MM-AAAA dentro de NOTAS_BASE_DIR."""
    dt = data_emissao or datetime.now()
    nome_pasta = dt.strftime("%m-%Y")
    pasta = NOTAS_BASE_DIR / nome_pasta
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def _nome_arquivo(mes_ano: str, nome_cliente: str, sufixo: int = 0) -> str:
    """Gera o nome do arquivo no padrão MM-AAAA-NOME DO CLIENTE.pdf"""
    base = f"{mes_ano}-{_sanitizar_nome(nome_cliente)}"
    if sufixo > 0:
        base = f"{base}-{sufixo}"
    return f"{base}.pdf"


def salvar_pdf(
    pdf_bytes: bytes,
    nome_cliente: str,
    payment_id: str,
    data_emissao: Optional[datetime] = None,
) -> Path:
    """
    Salva o PDF na pasta correta e retorna o caminho final.
    Nunca sobrescreve um arquivo de pagamento diferente.
    """
    pasta = _pasta_mes_ano(data_emissao)
    mes_ano = (data_emissao or datetime.now()).strftime("%m-%Y")

    # Tenta nome sem sufixo, depois com sufixo incremental
    for sufixo in range(0, 100):
        nome = _nome_arquivo(mes_ano, nome_cliente, sufixo)
        destino = pasta / nome

        if not destino.exists():
            destino.write_bytes(pdf_bytes)
            log.info("PDF salvo em: %s", destino)
            return destino

        # Arquivo já existe — é o mesmo pagamento? (verificação por tamanho simples)
        # Se for idêntico, retorna o caminho existente sem sobrescrever
        existente = destino.read_bytes()
        if existente == pdf_bytes:
            log.info("PDF idêntico já existe, reutilizando: %s", destino)
            return destino

    raise RuntimeError("Não foi possível salvar o PDF após 100 tentativas")


def caminho_esperado(nome_cliente: str, data_emissao: Optional[datetime] = None) -> Path:
    """Retorna o caminho onde o PDF seria salvo (sem criar)."""
    pasta = _pasta_mes_ano(data_emissao)
    mes_ano = (data_emissao or datetime.now()).strftime("%m-%Y")
    nome = _nome_arquivo(mes_ano, nome_cliente)
    return pasta / nome
