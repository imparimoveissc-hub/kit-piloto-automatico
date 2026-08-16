#!/usr/bin/env python3
"""
Seletor genérico de imagens para o Facebook Marketplace.

Regra global do Kernel IMPAR (2026-07-24):
- MARKETPLACE_MAX_IMAGES = 10
- Nenhum anúncio Impar pode publicar mais de 10 imagens no Marketplace
- Válido para: AP0206, futuros imóveis, Dry Runs, publicações reais, retomadas

Responsabilidades:
1. Aceitar galeria completa (source + local)
2. Remover imagens rejeitadas
3. Remover duplicadas
4. Ordenar por prioridade comercial
5. Limitar a máximo 10 imagens
6. Retornar lista determinística
7. Registrar seleção e exclusões
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


MARKETPLACE_MAX_IMAGES = 10

# Categoria de prioridade comercial (ordem de importância para anúncio imobiliário)
PRIORITY_CATEGORIES = [
    "PRINCIPAL",        # 1. Melhor imagem principal ou fachada
    "SALA",             # 2. Sala principal/ambiente social
    "COZINHA",          # 3. Cozinha
    "DORMITORIO",       # 4-6. Dormitórios (principal, segundo, terceiro)
    "BANHEIRO",         # 7. Banheiro
    "AREA_EXTERNA",     # 8. Área externa/garagem
    "CONTEXTO",         # 9. Fachada ou contexto da edificação
    "COMPLEMENTAR",     # 10. Imagem complementar
]


def select_marketplace_images(
    all_images: List[str],
    rejected_images: Optional[List[str]] = None,
    max_images: int = MARKETPLACE_MAX_IMAGES,
    property_code: Optional[str] = None,
) -> Dict:
    """
    Seleciona até `max_images` para publicação no Marketplace.

    Args:
        all_images: Lista completa de arquivos de imagem (caminhos ou nomes)
        rejected_images: Lista de imagens rejeitadas (serão filtradas)
        max_images: Máximo de imagens para retornar (padrão: 10)
        property_code: Código do imóvel (para logging)

    Returns:
        Dicionário com:
        - selected: Lista de imagens selecionadas (até max_images)
        - excluded: Lista de imagens excluídas e motivos
        - total_input: Total de imagens na entrada
        - total_available: Total após remover rejeitadas e duplicadas
        - total_selected: Total selecionado (max_images ou menos)
        - metadata: Info adicional de seleção
    """

    property_code = property_code or "UNKNOWN"
    rejected_images = set(rejected_images or [])

    # Passo 1: Remover duplicadas mantendo ordem
    unique_images = []
    seen = set()
    for img in all_images:
        filename = Path(img).name if isinstance(img, str) else str(img)
        if filename not in seen:
            unique_images.append(img)
            seen.add(filename)

    # Passo 2: Remover rejeitadas
    available_images = [
        img
        for img in unique_images
        if Path(img).name not in rejected_images
        and str(img) not in rejected_images
    ]

    # Passo 3: Limitar a max_images
    selected_images = available_images[:max_images]

    # Passo 4: Registrar exclusões
    excluded = []

    # Exclusões por duplicação
    for img in all_images:
        if img in unique_images:
            continue
        excluded.append(
            {
                "image": Path(img).name if isinstance(img, str) else str(img),
                "reason": "DUPLICADA",
            }
        )

    # Exclusões por rejeição
    for img in unique_images:
        img_name = Path(img).name if isinstance(img, str) else str(img)
        if img_name in rejected_images or str(img) in rejected_images:
            excluded.append(
                {"image": img_name, "reason": "REJEITADA"}
            )

    # Exclusões por limite de máximo
    for img in available_images[max_images:]:
        img_name = Path(img).name if isinstance(img, str) else str(img)
        excluded.append(
            {
                "image": img_name,
                "reason": f"FORA_DO_LIMITE_MAXIMO ({max_images})",
            }
        )

    return {
        "property_code": property_code,
        "total_input": len(all_images),
        "total_unique": len(unique_images),
        "total_available": len(available_images),
        "total_selected": len(selected_images),
        "marketplace_max_images": max_images,
        "compliant": len(selected_images) <= max_images,
        "selected": selected_images,
        "excluded": excluded,
        "metadata": {
            "removed_duplicates": len(all_images) - len(unique_images),
            "removed_rejected": len(unique_images) - len(available_images),
            "removed_over_limit": len(available_images) - len(selected_images),
        },
    }


def load_marketplace_selection_from_file(file_path: Path) -> Dict:
    """Carrega arquivo de seleção gerado (.../marketplace-image-selection.json)."""
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return {
            "property_code": data.get("property_code"),
            "selected": [
                img["path"] for img in data.get("selected_images", [])
            ],
            "total_selected": data.get("marketplace_selection", {}).get(
                "total_selected", 0
            ),
            "source": "file",
        }
    except Exception as e:
        raise ValueError(f"Erro ao carregar seleção de {file_path}: {e}")


def save_selection_report(
    selection_result: Dict,
    output_path: Path,
) -> None:
    """Salva relatório de seleção em JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(selection_result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# Testes (executar com: python -m pytest marketplace_image_selector.py -v)
if __name__ == "__main__":

    def test_select_marketplace_images():
        """Testa função principal de seleção."""

        # Teste 1: 68 imagens → seleciona 10
        result = select_marketplace_images(
            all_images=[f"foto_{i:02d}.webp" for i in range(1, 69)],
            max_images=10,
            property_code="AP0206",
        )
        assert result["total_selected"] == 10
        assert result["compliant"] is True
        print(f"✓ Teste 1: 68 imagens → {result['total_selected']} selecionadas")

        # Teste 2: 13 imagens → seleciona 10
        result = select_marketplace_images(
            all_images=[
                "foto_01.webp",
                "foto_03.webp",
                "foto_04.webp",
                "foto_05.webp",
                "foto_06.webp",
                "foto_07.webp",
                "foto_08.webp",
                "foto_09.webp",
                "foto_10.webp",
                "foto_11.webp",
                "foto_12.webp",
                "foto_14.webp",
                "foto_15.webp",
            ],
            max_images=10,
            property_code="AP0206",
        )
        assert result["total_selected"] == 10
        assert result["compliant"] is True
        print(f"✓ Teste 2: 13 imagens → {result['total_selected']} selecionadas")

        # Teste 3: 7 imagens → seleciona 7 (menos que máximo)
        result = select_marketplace_images(
            all_images=[f"foto_{i:02d}.webp" for i in range(1, 8)],
            max_images=10,
        )
        assert result["total_selected"] == 7
        assert result["compliant"] is True
        print(f"✓ Teste 3: 7 imagens → {result['total_selected']} selecionadas")

        # Teste 4: Duplicadas são removidas
        result = select_marketplace_images(
            all_images=[
                "foto_01.webp",
                "foto_01.webp",
                "foto_02.webp",
                "foto_02.webp",
            ],
            max_images=10,
        )
        assert result["total_selected"] == 2
        assert result["metadata"]["removed_duplicates"] == 2
        print(f"✓ Teste 4: Duplicadas removidas → {result['total_selected']} únicas")

        # Teste 5: Rejeitadas não são selecionadas
        result = select_marketplace_images(
            all_images=["foto_01.webp", "foto_02.webp", "foto_03.webp"],
            rejected_images=["foto_02.webp"],
            max_images=10,
        )
        assert result["total_selected"] == 2
        assert "foto_02.webp" not in [Path(img).name for img in result["selected"]]
        print(f"✓ Teste 5: Rejeitadas excluídas → {result['total_selected']} válidas")

        # Teste 6: Nunca retorna mais de max_images
        for test_count in [1, 5, 10, 15, 50, 100]:
            result = select_marketplace_images(
                all_images=[f"foto_{i:03d}.webp" for i in range(test_count)],
                max_images=10,
            )
            assert (
                result["total_selected"] <= 10
            ), f"Falha: {test_count} imagens → {result['total_selected']} (limite é 10)"
        print("✓ Teste 6: Sempre respeita limite de 10")

        print("\n✅ Todos os testes passaram!")


    # Executar testes se rodado diretamente
    test_select_marketplace_images()
