"""
Testes unitários do pipeline de emissão.

Executar: python -m pytest tests/ -v
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Configura variáveis mínimas para importação sem .env real
os.environ.setdefault("ASAAS_API_KEY", "fake_key")
os.environ.setdefault("NFEM_USER", "fake_user")
os.environ.setdefault("NFEM_PASSWORD", "fake_pass")
os.environ.setdefault("DRY_RUN", "true")
os.environ.setdefault("BROWSER_HEADLESS", "true")

# Redireciona pastas para temp
_tmp = tempfile.mkdtemp()
os.environ.setdefault("NOTAS_BASE_DIR", str(Path(_tmp) / "notas"))


# ── asaas_client ──────────────────────────────────────────────────────────────

def test_pagamento_autorizado():
    from src.asaas_client import pagamento_autoriza_nota
    ok, msg = pagamento_autoriza_nota({"status": "CONFIRMED"})
    assert ok

def test_pagamento_pendente_nao_autorizado():
    from src.asaas_client import pagamento_autoriza_nota
    ok, msg = pagamento_autoriza_nota({"status": "PENDING"})
    assert not ok

def test_pagamento_cancelado_nao_autorizado():
    from src.asaas_client import pagamento_autoriza_nota
    ok, msg = pagamento_autoriza_nota({"status": "CANCELLED"})
    assert not ok

@pytest.mark.parametrize("status", ["OVERDUE", "REFUNDED", "PARTIALLY_REFUNDED"])
def test_status_nao_autorizados(status):
    from src.asaas_client import pagamento_autoriza_nota
    ok, _ = pagamento_autoriza_nota({"status": status})
    assert not ok


# ── montagem de dados ─────────────────────────────────────────────────────────

def test_montar_dados_completos():
    from src.asaas_client import montar_dados_nota
    pag = {
        "id": "pay_001",
        "customer": "cus_001",
        "status": "CONFIRMED",
        "value": 1000.00,
        "paymentDate": "2026-06-01",
        "description": "Serviço teste",
    }
    cli = {
        "name": "FULANO INQUILINO",
        "cpfCnpj": "12345678900",
        "city": "Joinville",
        "state": "SC",
    }
    cfg = {
        "nome_tomador": "FULANO PROPRIETARIO",
        "cpf_cnpj": "98765432100",
        "valor_referencia": 250.0,
        "descricao_servico": "Administração de imóvel teste",
    }
    dados = montar_dados_nota(pag, cli, cfg)
    assert dados["payment_id"] == "pay_001"
    assert dados["nome_tomador"] == "FULANO PROPRIETARIO"
    assert dados["valor_servico"] == 250.0

def test_montar_dados_sem_config_levanta_erro():
    """Sem cliente_config (proprietário não cadastrado), não pode emitir para o inquilino."""
    from src.asaas_client import montar_dados_nota
    pag = {"id": "pay_002", "customer": "cus_002", "value": 500, "status": "CONFIRMED"}
    cli = {"name": "FULANO", "cpfCnpj": "11122233344"}
    with pytest.raises(ValueError):
        montar_dados_nota(pag, cli, None)


# ── idempotência ──────────────────────────────────────────────────────────────

def test_idempotencia(tmp_path, monkeypatch):
    monkeypatch.setattr("src.idempotency.EMISSOES_DB", tmp_path / "emissoes.json")
    from src.idempotency import ja_emitida, registrar_emissao

    assert not ja_emitida("pay_abc")
    registrar_emissao("pay_abc", "CLIENTE", 100.0, "2026-06-01", "001", "/tmp/f.pdf")
    assert ja_emitida("pay_abc")

def test_registro_erro_e_reset(tmp_path, monkeypatch):
    monkeypatch.setattr("src.idempotency.EMISSOES_DB", tmp_path / "emissoes.json")
    from src.idempotency import registrar_erro, listar_erros, resetar_para_reprocessamento, ja_emitida

    registrar_erro("pay_err", "CLI", 50.0, "falha simulada")
    erros = listar_erros()
    assert any(e["payment_id"] == "pay_err" for e in erros)

    resetar_para_reprocessamento("pay_err")
    assert not ja_emitida("pay_err")


# ── PDF manager ───────────────────────────────────────────────────────────────

def test_salvar_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pdf_manager.NOTAS_BASE_DIR", tmp_path)
    from src.pdf_manager import salvar_pdf
    from datetime import datetime

    caminho = salvar_pdf(b"%PDF fake", "FULANO DA SILVA", "pay_001", datetime(2026, 5, 10))
    assert caminho.exists()
    assert "05-2026" in str(caminho)
    assert "FULANO DA SILVA" in caminho.name

def test_salvar_pdf_sufixo_incremental(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pdf_manager.NOTAS_BASE_DIR", tmp_path)
    from src.pdf_manager import salvar_pdf
    from datetime import datetime

    dt = datetime(2026, 5, 10)
    p1 = salvar_pdf(b"%PDF v1", "FULANO", "pay_001", dt)
    p2 = salvar_pdf(b"%PDF v2", "FULANO", "pay_002", dt)
    assert p1 != p2
    assert "-2" in p2.name

def test_salvar_pdf_idempotente(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pdf_manager.NOTAS_BASE_DIR", tmp_path)
    from src.pdf_manager import salvar_pdf
    from datetime import datetime

    dt = datetime(2026, 5, 10)
    p1 = salvar_pdf(b"%PDF igual", "MARIO", "pay_001", dt)
    p2 = salvar_pdf(b"%PDF igual", "MARIO", "pay_001", dt)
    assert p1 == p2  # mesmo conteúdo → mesmo arquivo

def test_nome_sanitizado(tmp_path, monkeypatch):
    monkeypatch.setattr("src.pdf_manager.NOTAS_BASE_DIR", tmp_path)
    from src.pdf_manager import salvar_pdf
    from datetime import datetime

    caminho = salvar_pdf(b"%PDF x", "JOÃO/SILVA:TESTE?", "pay_x", datetime(2026, 5, 1))
    assert "/" not in caminho.name
    assert ":" not in caminho.name
