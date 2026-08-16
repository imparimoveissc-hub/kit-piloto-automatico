#!/usr/bin/env python3
"""
Marketplace Enhancement via OpenAI API
Improves titles and descriptions while maintaining factual accuracy.
"""

import os
import json
import random
import hashlib
from datetime import date
from pathlib import Path

# Ângulos criativos para variar títulos mesmo entre imóveis similares
_TITLE_ANGLES = [
    "foco no estilo de vida que o imóvel proporciona",
    "foco na localização privilegiada e praticidade do bairro",
    "foco no custo-benefício e oportunidade de preço",
    "foco no espaço e conforto para a família",
    "foco na tranquilidade e qualidade de vida",
    "foco na oportunidade de negócio (urgência suave)",
    "foco nos diferenciais do imóvel vs. outros no bairro",
    "foco no público jovem e praticidade do dia a dia",
]

try:
    from openai import OpenAI, APIError
except ImportError:
    raise RuntimeError("openai package required: pip install openai")


# Load .env file if it exists
def _load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


_load_env()

ENABLE_ENHANCE = os.getenv("ENHANCE_MARKETPLACE_ENABLED", "true").lower() == "true"
VERBOSE = os.getenv("ENHANCE_VERBOSE", "false").lower() == "true"
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Cache to avoid redundant API calls
CACHE_DIR = Path(__file__).parent / ".enhance_cache"
CACHE_DIR.mkdir(exist_ok=True)

client = None
if ENABLE_ENHANCE and API_KEY:
    try:
        client = OpenAI(api_key=API_KEY)
    except Exception as e:
        if VERBOSE:
            print(f"⚠️ OpenAI client init failed: {e}")


def _get_cache_path(prompt_hash):
    """Get cache file path for a prompt."""
    return CACHE_DIR / f"{prompt_hash}.json"


def _hash_prompt(text):
    """Create hash of prompt for caching."""
    return hashlib.md5(text.encode()).hexdigest()


def _load_cache(prompt_hash):
    """Load cached response if exists."""
    cache_path = _get_cache_path(prompt_hash)
    if cache_path.exists():
        try:
            data = json.loads(cache_path.read_text())
            if VERBOSE:
                print(f"✅ Cache hit for {prompt_hash[:8]}")
            return data.get("response")
        except Exception as e:
            if VERBOSE:
                print(f"⚠️ Cache read error: {e}")
    return None


def _save_cache(prompt_hash, response):
    """Save response to cache."""
    try:
        cache_path = _get_cache_path(prompt_hash)
        cache_path.write_text(json.dumps({"response": response, "hash": prompt_hash}))
    except Exception as e:
        if VERBOSE:
            print(f"⚠️ Cache write error: {e}")


def enhance_title(prop):
    """
    Enhance marketplace title using OpenAI.
    Returns more attractive title without inventing facts.
    Each queue position gets a different angle so repeated listings are always unique.
    """
    if not ENABLE_ENHANCE or not client:
        return None

    original_title = f"{prop['tipo']} para {'locacao' if prop['operacao'] == 'locacao' else 'venda'} no {prop['bairro']} - {prop['cidade']}"

    iso_week = date.today().isocalendar()[1]
    # _queue_position é injetado pelo build_queue() — garante título único por postagem
    queue_pos = prop.get('_queue_position', prop.get('ordem_na_etapa', 0))
    angle_seed = hash(f"{prop.get('ref', prop.get('codigo', ''))}_{iso_week}_{queue_pos}") % len(_TITLE_ANGLES)
    angle = _TITLE_ANGLES[angle_seed]

    prompt = f"""Reescreva este título de imóvel no marketplace deixando mais atrativo, mas SEM inventar nada.
Mantenha apenas informações FACTUAIS do imóvel: tipo, operação, bairro, cidade, preço se houver.
Use emojis estratégicos para chamar atenção.
Máximo 120 caracteres.
IMPORTANTE: Preço deve ser copiado EXATAMENTE como está (com casas decimais e formatação original).

Ângulo criativo a usar: {angle}

Dados do imóvel:
- Tipo: {prop['tipo']}
- Operação: {'Locação/Aluguel' if prop['operacao'] == 'locacao' else 'Venda/Compra'}
- Bairro: {prop['bairro']}
- Cidade: {prop['cidade']}
- Preço (COPIAR EXATAMENTE): {prop['preco']}
- Referência: {prop['ref']}
- Posição na fila: {queue_pos}

Título original: {original_title}

Responda APENAS com o novo título, nada mais."""

    # Hash inclui posição na fila — mesmo imóvel re-postado recebe título diferente
    prompt_hash = _hash_prompt(f"w{iso_week}_pos{queue_pos}_{prompt}")

    cached = _load_cache(prompt_hash)
    if cached:
        return cached

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        enhanced = response.choices[0].message.content.strip()
        _save_cache(prompt_hash, enhanced)
        if VERBOSE:
            print(f"✨ Title enhanced: {original_title[:40]}... → {enhanced[:40]}...")
        return enhanced
    except APIError as e:
        if VERBOSE:
            print(f"❌ OpenAI error enhancing title: {e}")
        return None


def enhance_description(prop):
    """
    Enhance marketplace description using OpenAI.
    Returns more compelling description without inventing facts.
    """
    if not ENABLE_ENHANCE or not client:
        return None

    original_desc = prop.get("resumo_site", "") or prop.get("detalhes", "")

    iso_week = date.today().isocalendar()[1]
    angle_seed = hash(f"desc_{prop.get('ref', prop.get('codigo', ''))}_{iso_week}") % len(_TITLE_ANGLES)
    angle = _TITLE_ANGLES[angle_seed]

    prompt = f"""Reescreva esta descrição de imóvel para o marketplace deixando MAIS ATRATIVA.
Regras:
1. SEM inventar nada - só use dados que já estão aqui
2. Estruture com emojis estratégicos
3. Seja conciso e impactante
4. Mantenha o tom profissional mas amigável
5. Inclua call-to-action para WhatsApp/contato
6. IMPORTANTE: Preço deve ser EXATAMENTE como está (com casas decimais e formatação original)
7. Ângulo criativo a usar: {angle}

Dados do imóvel:
- Tipo: {prop['tipo']}
- Operação: {'Locação/Aluguel' if prop['operacao'] == 'locacao' else 'Venda/Compra'}
- Bairro: {prop['bairro']}
- Cidade: {prop['cidade']}
- Preço (COPIAR EXATAMENTE): {prop['preco']}
- Referência: {prop['ref']}
- Descrição original: {original_desc}

Responda APENAS com a nova descrição, nada mais."""

    prompt_hash = _hash_prompt(f"w{iso_week}_{prompt}")

    cached = _load_cache(prompt_hash)
    if cached:
        return cached

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        enhanced = response.choices[0].message.content.strip()
        _save_cache(prompt_hash, enhanced)
        if VERBOSE:
            print(f"✨ Description enhanced (from {len(original_desc)} → {len(enhanced)} chars)")
        return enhanced
    except APIError as e:
        if VERBOSE:
            print(f"❌ OpenAI error enhancing description: {e}")
        return None


def enhance_tags(prop):
    """
    Generate 20 SEO-optimized tags via OpenAI, separated by semicolons.
    Each queue position gets a different seed so re-posts have varied tags.
    """
    if not ENABLE_ENHANCE or not client:
        return None

    iso_week = date.today().isocalendar()[1]
    queue_pos = prop.get('_queue_position', prop.get('ordem_na_etapa', 0))

    prompt = f"""Gere exatamente 20 tags para este imóvel no Facebook Marketplace.
Regras:
1. Separadas por ponto e vírgula (;) sem espaço antes do ponto e vírgula
2. Em português, sem acentos, tudo minúsculo
3. Mix variado: tipo de imóvel, operação, bairro, cidade, estado, termos de busca
4. Inclua: "impar imoveis", "joinville sc", "imovel sc" entre as tags
5. Sem repetição de tag
6. Cada tag com no máximo 4 palavras
7. Responda SOMENTE com as 20 tags separadas por ; sem nenhum texto adicional

Dados do imóvel:
- Tipo: {prop['tipo']}
- Operação: {'locacao aluguel' if prop['operacao'] == 'locacao' else 'venda compra'}
- Bairro: {prop['bairro']}
- Cidade: {prop['cidade']}
- Referência: {prop.get('ref', prop.get('codigo', ''))}
- Variação: {queue_pos}"""

    prompt_hash = _hash_prompt(f"tags_w{iso_week}_pos{queue_pos}_{prompt}")

    cached = _load_cache(prompt_hash)
    if cached:
        return cached

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content.strip()
        tags = [t.strip().lower() for t in raw.split(';') if t.strip()]
        if len(tags) >= 15:
            result = '; '.join(tags[:20])
            _save_cache(prompt_hash, result)
            if VERBOSE:
                print(f"🏷️ Tags enhanced: {len(tags)} tags geradas")
            return result
        if VERBOSE:
            print(f"⚠️ Tags: resposta insuficiente ({len(tags)} tags), usando fallback")
        return None
    except APIError as e:
        if VERBOSE:
            print(f"❌ OpenAI error enhancing tags: {e}")
        return None


def is_enabled():
    """Check if enhancement is enabled."""
    return ENABLE_ENHANCE and client is not None
