#!/bin/bash
# Script de Formateo - Lavandería Express QuickClean
# ROJAS BURBANO - Ficha 3147246

echo "🎨 Formateando código con Black..."
black app/ tests/

echo ""
echo "📦 Organizando imports con isort..."
isort app/ tests/

echo ""
echo "✅ Formateo completado exitosamente"
