#!/bin/bash
# Script de Linting - Lavandería Express QuickClean
# ROJAS BURBANO - Ficha 3147246

echo "🔍 Ejecutando flake8..."
flake8 app/ tests/

echo ""
echo "🔒 Ejecutando bandit (seguridad)..."
bandit -r app/

echo ""
echo "🏷️  Ejecutando mypy (tipos)..."
mypy app/

echo ""
echo "✅ Linting completado"
