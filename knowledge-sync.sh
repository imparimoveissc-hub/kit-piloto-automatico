#!/bin/zsh
set -e

echo "🧠 Atualizando Knowledge Layer..."

START_TIME=$(date '+%Y-%m-%d %H:%M:%S')

graphify .
graphify cluster-only .

mkdir -p Knowledge/Code/graphify

rsync -a --delete graphify-out/ Knowledge/Code/graphify/

cat > Knowledge/Code/graphify/LAST_SYNC.md <<EOL
# Last Knowledge Sync

- Última atualização: $START_TIME
- Estratégia: Graphify + Knowledge Layer
- Objetivo: reduzir leitura manual de arquivos e diminuir uso de tokens no Claude Code.

## Ordem recomendada de consulta

1. Knowledge/Code/graphify/GRAPH_REPORT.md
2. Knowledge/Code/graphify/graph.json
3. Knowledge/Code/graphify/manifest.json
4. Knowledge/Decisions/ADR/
5. Knowledge/Business/
6. Knowledge/Memory/
7. Código-fonte somente se necessário.
EOL

echo ""
echo "✅ Knowledge Layer atualizado"
echo "✅ Graphify sincronizado"
echo "✅ LAST_SYNC.md criado"
echo ""
ls -lh Knowledge/Code/graphify/GRAPH_REPORT.md Knowledge/Code/graphify/graph.json Knowledge/Code/graphify/graph.html
