"""Centraliza carregamento de variáveis de ambiente e constantes da NF-em/NFS-e."""

import os
import json
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# ── Asaas ──────────────────────────────────────────────────────────────────────
ASAAS_API_KEY: str = os.environ["ASAAS_API_KEY"]
ASAAS_WEBHOOK_TOKEN: str = os.getenv("ASAAS_WEBHOOK_TOKEN", "")
ASAAS_ENV: str = os.getenv("ASAAS_ENV", "production")
ASAAS_BASE_URL: str = (
    "https://api.asaas.com/v3"
    if ASAAS_ENV == "production"
    else "https://sandbox.asaas.com/api/v3"
)

# ── Portal Nacional NFS-e (exclusivo) ──────────────────────────────────────────
# Migração 20/07/2026: apenas portal nacional (nfse.gov.br/EmissorNacional)
# Portal de Joinville descontinuado
NFSE_NACIONAL_USER: str = os.getenv("NFSE_NACIONAL_USER", "")
NFSE_NACIONAL_PASSWORD: str = os.getenv("NFSE_NACIONAL_PASSWORD", "")
NFSE_NACIONAL_URL: str = "https://www.nfse.gov.br/EmissorNacional"
NFSE_NACIONAL_ORIGIN: str = f"{urlparse(NFSE_NACIONAL_URL).scheme}://{urlparse(NFSE_NACIONAL_URL).netloc}"

# Certificado digital A1 (caminho relativo à raiz do projeto ou absoluto).
# Login por certificado dispensa captcha — é o caminho 100% automático.
_PROJECT_ROOT: Path = Path(__file__).parent.parent
_pfx_env = os.getenv("NFSE_CERT_PFX_PATH", "config/certs/impar_50886299000100.pfx")
NFSE_CERT_PFX_PATH: Path = (
    Path(_pfx_env) if Path(_pfx_env).is_absolute() else _PROJECT_ROOT / _pfx_env
)
NFSE_CERT_PASSWORD: str = os.getenv("NFSE_CERT_PASSWORD", "")
NFSE_CERT_PEM_PATH: Path = Path(
    os.getenv("NFSE_CERT_PEM_PATH", _PROJECT_ROOT / "config/certs/impar_cert.pem")
)
NFSE_CERT_KEY_PATH: Path = Path(
    os.getenv("NFSE_CERT_KEY_PATH", _PROJECT_ROOT / "config/certs/impar_key.pem")
)
NFSE_DANFSE_API_URL: str = os.getenv(
    "NFSE_DANFSE_API_URL",
    "https://adn.nfse.gov.br/danfse",
)


def certificado_digital_configurado() -> bool:
    """Indica se há certificado A1 pronto para uso no Portal Nacional."""
    return NFSE_CERT_PFX_PATH.exists() and bool(NFSE_CERT_PASSWORD)


def certificado_mtls_configurado() -> bool:
    """Indica se o certificado A1 está pronto para autenticar nas APIs do ADN."""
    return (
        NFSE_CERT_PEM_PATH.exists()
        and NFSE_CERT_KEY_PATH.exists()
        and bool(NFSE_CERT_PASSWORD)
    )


def client_certificates_nfse_nacional() -> list[dict]:
    """
    Monta a configuração de client certificates do Playwright.

    O Portal Nacional aceita TLS client authentication no mesmo origin do site.
    """
    if not certificado_digital_configurado():
        return []

    return [
        {
            "origin": NFSE_NACIONAL_ORIGIN,
            "pfxPath": str(NFSE_CERT_PFX_PATH),
            "passphrase": NFSE_CERT_PASSWORD,
        }
    ]

# ── Dados fixos do prestador ───────────────────────────────────────────────────
PRESTADOR_NOME: str = "IMPAR IMOVEIS LTDA"
PRESTADOR_CNPJ: str = "50.886.299/0001-00"
NATUREZA_OPERACAO: str = "107"          # ISS devido para Joinville - Simples Nacional
ITEM_LISTA_SERVICO: str = "17.12"       # Administração em geral
CODIGO_SERVICO: str = "1712"
ALIQUOTA_ISS: float = 5.0
MUNICIPIO_INCIDENCIA: str = "Joinville"
UF_INCIDENCIA: str = "SC"
ISS_RETIDO: bool = False

# Alíquota do Simples Nacional informada em "Valor aproximado dos tributos"
# (confirmada pelo Jonata em 20/07/2026: 6% fixo)
ALIQUOTA_SIMPLES: float = float(os.getenv("ALIQUOTA_SIMPLES", "6.0"))

# ── Itens NBS por situação (exigidos pelo Portal Nacional) ─────────────────────
# Cód. tributação 10.05 (intermediação/corretagem):
NBS_VENDA_IMOVEL: str = "1.1001.21.00"        # venda de imóvel, residencial ou não
NBS_CORRETAGEM_SEGUROS: str = "1.0906.11.00"  # comissões de seguro incêndio, fiança
                                              # locatícia, taxa setup, garantia Investe,
                                              # tomadores Loft/Zurich etc.
# Cód. tributação 17.12 (administração/locação — lote mensal do Asaas):
NBS_ALUGUEL_RESIDENCIAL: str = "1.0905.12.00"
NBS_ALUGUEL_NAO_RESIDENCIAL: str = "1.0905.12.00"


def nbs_para_aluguel(tipo_imovel: Optional[str]) -> str:
    """Resolve o item NBS do lote mensal a partir do tipo_imovel do clientes.json."""
    if (tipo_imovel or "").strip().lower() in ("nao_residencial", "não_residencial", "comercial"):
        return NBS_ALUGUEL_NAO_RESIDENCIAL
    return NBS_ALUGUEL_RESIDENCIAL

# ── Caminhos ───────────────────────────────────────────────────────────────────
NOTAS_BASE_DIR: Path = Path(
    os.getenv(
        "NOTAS_BASE_DIR",
        "/Users/user/Desktop/backup Jonata/contabilidade Impar imóveis/notas fiscais",
    )
)
DATA_DIR: Path = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

EMISSOES_DB: Path = DATA_DIR / "emissoes.json"
LOGS_DIR: Path = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Sessão "quente" do Portal Nacional: cookies de um login manual, reusados para pular o
# captcha enquanto a sessão do portal continuar válida (uso remoto/desassistido).
# Migração 20/07/2026: apenas portal nacional
NFSE_NACIONAL_SESSION_STATE: Path = DATA_DIR / "nfse_nacional_session.json"

# ── Servidor ───────────────────────────────────────────────────────────────────
WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", "8765"))

# ── Operação ───────────────────────────────────────────────────────────────────
DRY_RUN: bool = os.getenv("DRY_RUN", "true").lower() == "true"
BROWSER_HEADLESS: bool = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"

# ── Clientes ───────────────────────────────────────────────────────────────────
_CLIENTES_FILE: Path = Path(__file__).parent.parent / "config" / "clientes.json"

def carregar_clientes() -> list[dict]:
    if not _CLIENTES_FILE.exists():
        return []
    with open(_CLIENTES_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("clientes", [])
