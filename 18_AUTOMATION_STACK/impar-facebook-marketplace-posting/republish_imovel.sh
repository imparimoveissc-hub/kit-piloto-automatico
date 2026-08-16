#!/bin/bash
# republish_imovel.sh — Re-publicar um imóvel que já foi publicado
#
# USO:
#   ./republish_imovel.sh CS0104       # Remove CS0104 do log e libera para re-publicação
#   ./republish_imovel.sh CS0104 true  # Mesma coisa + rodar publicação agora
#
# REQUISITO: Jonata deve CONFIRMAR manualmente a exceção

set -e

CODIGO="${1:-}"
AUTO_PUBLISH="${2:-false}"

if [ -z "$CODIGO" ]; then
    echo "❌ Uso: $0 CODIGO [true]"
    echo ""
    echo "Exemplos:"
    echo "  $0 CS0104           # Remover CS0104 do log"
    echo "  $0 CS0104 true      # Remover + publicar agora"
    exit 1
fi

# Caminho do log
LOG="05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/marketplace-publicados-log.csv"
FILA="05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/fila-postagens-venda.csv"

if [ ! -f "$LOG" ]; then
    echo "❌ Log não encontrado: $LOG"
    exit 1
fi

# Verificar se o código foi publicado
if ! grep -q ",${CODIGO}," "$LOG"; then
    echo "⚠️  Código $CODIGO NÃO encontrado no log de publicados."
    echo "   Nada para remover."
    exit 0
fi

echo "🔍 Encontrado $CODIGO no log de publicados:"
grep ",${CODIGO}," "$LOG" | tail -1

# Confirmar
read -p "⚠️  Remover $CODIGO do log e liberar para re-publicação? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "❌ Cancelado."
    exit 0
fi

# Remover do log
TEMP="/tmp/republish_${CODIGO}_$$.csv"
grep -v ",${CODIGO}," "$LOG" > "$TEMP"
mv "$TEMP" "$LOG"

echo "✅ $CODIGO removido do log de publicados."
echo ""

if [ "$AUTO_PUBLISH" = "true" ]; then
    echo "🚀 Iniciando publicação..."
    cd "$(dirname "$0")" || exit 1
    python3 publish_daily_from_fila.py --fila "$FILA" --due --publish --max 1
else
    echo "📌 Próximas etapas:"
    echo "   1. Confirme que $CODIGO está na fila com data_sugerida = hoje"
    echo "   2. Execute: python3 publish_daily_from_fila.py --due --publish"
    echo ""
    echo "   Ou faça tudo de uma vez:"
    echo "   ./$0 $CODIGO true"
fi
