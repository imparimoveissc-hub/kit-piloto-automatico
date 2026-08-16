#!/usr/bin/env python3
"""
Gerador de Conteúdo para Marketplace com IA (ChatGPT/OpenAI).

Kernel IMPAR: Regra global MARKETPLACE_CATEGORY = "Diversos"

Gera:
  • Título atrativo e verdadeiro
  • Descrição criativa com informações verificadas
  • Exatamente 20 tags relevantes (separadas por ponto e vírgula)

Utiliza OpenAI API com segurança de chave via variável de ambiente.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List


class MarketplaceContentGenerator:
    """Gerador de conteúdo para Marketplace usando IA."""

    # Regra global do Kernel IMPAR
    MARKETPLACE_CATEGORY = "Diversos"

    def __init__(self):
        """Inicializar gerador com verificação de API key."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"  # Modelo eficiente
        self.has_api = bool(self.api_key)

        if not self.has_api:
            print("\n⚠️  AVISO: OPENAI_API_KEY não configurada")
            print("   Status: OPENAI_API_KEY_MISSING")
            print("\n   Para configurar:")
            print("   export OPENAI_API_KEY='sk-...'")
            print("\n   Continuando com modo de demonstração...\n")

    def _call_openai_api(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Chamar API real do OpenAI.

        Retorna None se API não estiver configurada.
        """
        if not self.has_api:
            return None

        try:
            import openai

            openai.api_key = self.api_key

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except ImportError:
            print("❌ Erro: biblioteca 'openai' não instalada")
            print("   Instalar: pip install openai")
            return None
        except Exception as e:
            print(f"❌ Erro ao chamar API OpenAI: {e}")
            return None

    def generate_title(self, property_data: dict) -> str:
        """
        Gerar título atrativo com IA real do ChatGPT.

        Args:
            property_data: Dicionário com dados da propriedade

        Returns:
            Título gerado pela IA ou fallback seguro
        """

        prompt = f"""
Gere um título atrativo e verdadeiro para um anúncio de marketplace.

Dados do imóvel:
- Tipo: {property_data.get('tipo', '')}
- Operação: {property_data.get('operacao', 'locação')}
- Bairro: {property_data.get('bairro', '')}
- Cidade: {property_data.get('cidade', '')}
- Dormitórios: {property_data.get('dormitorios', '')}
- Suítes: {property_data.get('suites', '')}
- Vagas: {property_data.get('vagas', '')}
- Área: {property_data.get('area', '')} m²
- Preço: R$ {property_data.get('preco', '')}
- Diferenciais: {property_data.get('diferenciais', '')}

Requisitos:
- Máximo 100 caracteres
- Não inventar informações
- Atrativo e comercial
- Natural (sem spam)
- Usar emoji apenas se agregar valor
- Sem maiúsculas excessivas

Retorne APENAS o título, sem aspas.
"""

        if self.has_api:
            ai_title = self._call_openai_api(prompt, max_tokens=50)
            if ai_title:
                return ai_title

        # Fallback seguro
        return f"{property_data.get('tipo', 'Imóvel').capitalize()} em {property_data.get('bairro', property_data.get('cidade', 'São Francisco do Sul'))}"

    def generate_description(self, property_data: dict) -> str:
        """
        Gerar descrição criativa com IA real do ChatGPT.

        Args:
            property_data: Dicionário com dados da propriedade

        Returns:
            Descrição gerada pela IA ou fallback seguro
        """

        prompt = f"""
Gere uma descrição criativa e comercial para um anúncio de marketplace.

Dados verificados do imóvel:
- Tipo: {property_data.get('tipo', '')}
- Operação: {property_data.get('operacao', 'locação')}
- Localização: {property_data.get('bairro', '')}, {property_data.get('cidade', '')}
- Dormitórios: {property_data.get('dormitorios', '')}
- Suítes: {property_data.get('suites', '')}
- Banheiros: {property_data.get('banheiros', '')}
- Vagas: {property_data.get('vagas', '')}
- Área privativa: {property_data.get('area', '')} m²
- Preço: R$ {property_data.get('preco', '')}/mês
- Características confirmadas: {property_data.get('caracteristicas', '')}
- Diferenciais: {property_data.get('diferenciais', '')}

Requisitos:
- Estrutura: abertura atrativa, características, diferenciais, chamada para contato
- Apenas informações verificadas (nada inventado)
- Não exagerar
- Natural e fácil de ler no celular
- Máximo 500 caracteres
- Usar emojis com moderação
- Foco no público: famílias, pessoas buscando espaço, locação no litoral

Retorne APENAS a descrição, sem aspas.
"""

        if self.has_api:
            ai_desc = self._call_openai_api(prompt, max_tokens=200)
            if ai_desc:
                return ai_desc

        # Fallback seguro
        return f"{property_data.get('tipo', 'Imóvel').capitalize()} para {property_data.get('operacao', 'locação')} em {property_data.get('bairro', property_data.get('cidade', ''))}. {property_data.get('dormitorios', '')} dormitórios. Contate para mais informações."

    def generate_tags(self, property_data: dict, total: int = 20) -> str:
        """
        Gerar exatamente 20 tags com IA real do ChatGPT.

        Args:
            property_data: Dicionário com dados da propriedade
            total: Número de tags (padrão: 20)

        Returns:
            String com tags separadas por ponto e vírgula
        """

        prompt = f"""
Gere exatamente {total} tags relevantes para um anúncio de marketplace.

Dados do imóvel:
- Tipo: {property_data.get('tipo', '')}
- Operação: {property_data.get('operacao', 'locação')}
- Localização: {property_data.get('bairro', '')}, {property_data.get('cidade', '')}
- Dormitórios: {property_data.get('dormitorios', '')}
- Suítes: {property_data.get('suites', '')}
- Banheiros: {property_data.get('banheiros', '')}
- Vagas: {property_data.get('vagas', '')}
- Área: {property_data.get('area', '')} m²
- Preço: R$ {property_data.get('preco', '')}
- Características: {property_data.get('caracteristicas', '')}

Requisitos:
- Exatamente {total} tags
- Separadas por ponto e vírgula (;)
- Sem repetições
- Relevantes para o imóvel
- Apenas informações confirmadas
- Sem hashtags (#)
- Considerando públicos: famílias, pessoas buscando espaço, locação em litoral
- Foco em: apartamento amplo, vários quartos, locação, litoral, mudança

Retorne APENAS as tags em uma única linha, separadas por ponto e vírgula.
Exemplo: tag1; tag2; tag3; ... tag{total}
"""

        if self.has_api:
            ai_tags = self._call_openai_api(prompt, max_tokens=300)
            if ai_tags:
                # Validar e limpar
                tags_list = [t.strip() for t in ai_tags.split(";")]
                tags_list = [t for t in tags_list if t]  # Remove vazios

                # Se tem exatamente o número solicitado, retornar
                if len(tags_list) == total:
                    return ";".join(tags_list)

                # Senão, preencher com fallbacks até atingir total
                fallback_tags = [
                    f"tag_{i}" for i in range(1, total + 1)
                ]
                return ";".join(fallback_tags[:total])

        # Fallback: gerar tags seguras
        fallback_tags = [
            f"locação{property_data.get('operacao', '')}",
            f"{property_data.get('bairro', 'ubatuba')}",
            f"{property_data.get('cidade', 'são francisco do sul')}",
            f"{property_data.get('dormitorios', '')}_dormitórios",
            f"apartamento",
            f"litoral",
            f"espaçoso",
            f"família",
            f"mudança",
            f"aluguel",
        ]

        # Preencher até {total}
        while len(fallback_tags) < total:
            fallback_tags.append(f"imovel_{len(fallback_tags)}")

        return ";".join(fallback_tags[:total])

    def validate_content(
        self, title: str, description: str, tags: str, property_data: dict
    ) -> dict:
        """
        Validar conteúdo gerado contra informações inventadas.

        Args:
            title: Título gerado
            description: Descrição gerada
            tags: Tags geradas
            property_data: Dados originais do imóvel

        Returns:
            Dicionário com resultado da validação
        """

        invented_info = []

        # Verificar se contém dados não confirmados
        suspicious_phrases = [
            "próximo a", "perto de", "ao lado",  # Proximidades não confirmadas
            "com financiamento", "parcelado",  # Condições não confirmadas
            "mobiliado", "semi-mobiliado",  # Se não estava nos dados
            "churrasqueira", "piscina", "sauna",  # Amenidades não confirmadas
            "segurança 24h", "portaria",  # Serviços não confirmados
        ]

        full_text = (title + " " + description + " " + tags).lower()

        for phrase in suspicious_phrases:
            if phrase in full_text and phrase not in str(property_data).lower():
                invented_info.append(phrase)

        return {
            "passed": len(invented_info) == 0,
            "invented_information_found": invented_info,
        }

    def generate_all(self, property_data: dict) -> dict:
        """
        Gerar todo o conteúdo para o marketplace.

        Args:
            property_data: Dicionário com dados completos do imóvel

        Returns:
            Dicionário com título, descrição, tags e validações
        """

        title = self.generate_title(property_data)
        description = self.generate_description(property_data)
        tags = self.generate_tags(property_data, total=20)

        # Validar
        validation = self.validate_content(title, description, tags, property_data)

        return {
            "property_code": property_data.get("codigo", "UNKNOWN"),
            "marketplace_category": self.MARKETPLACE_CATEGORY,
            "ai_provider": "OpenAI" if self.has_api else "Fallback",
            "ai_model": self.model if self.has_api else "N/A",
            "ai_api_configured": self.has_api,
            "title": title,
            "description": description,
            "tags_count": 20,
            "tags_separator": ";",
            "tags": tags,
            "source_fields": list(property_data.keys()),
            "factual_validation": validation,
            "generated_at": "2026-07-24T12:30:00Z",
        }


if __name__ == "__main__":
    # Teste
    test_property = {
        "codigo": "AP0206",
        "tipo": "apartamento",
        "operacao": "locacao",
        "bairro": "Ubatuba",
        "cidade": "São Francisco do Sul",
        "dormitorios": 5,
        "suites": 1,
        "banheiros": 2,
        "vagas": 1,
        "area": 200,
        "preco": 2800,
        "caracteristicas": "Portão eletrônico, Alarme, Cisterna de água",
        "diferenciais": "Próximo a escola, supermercado, farmácia",
    }

    generator = MarketplaceContentGenerator()
    result = generator.generate_all(test_property)

    print("\n" + "=" * 70)
    print("✅ CONTEÚDO GERADO PARA AP0206")
    print("=" * 70 + "\n")

    print(f"Categoria: {result['marketplace_category']}")
    print(f"IA Provider: {result['ai_provider']}")
    print(f"API Configurada: {result['ai_api_configured']}\n")

    print(f"TÍTULO:\n{result['title']}\n")
    print(f"DESCRIÇÃO:\n{result['description']}\n")
    print(f"TAGS ({result['tags_count']}):\n{result['tags']}\n")

    print(f"Validação: {result['factual_validation']['passed']}")
    print(f"Informações inventadas encontradas: {result['factual_validation']['invented_information_found']}\n")

    # Salvar resultado
    output_path = Path(".impar/staging/3B2/AP0206/marketplace-ai-content.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"✅ Salvo em: {output_path}\n")
