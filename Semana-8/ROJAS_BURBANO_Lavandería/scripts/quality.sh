#!/bin/bash
# Script de Calidad Completa - Lavandería Express QuickClean
# ROJAS BURBANO - Ficha 3147246

echo "🚀 Ejecutando revisión completa de calidad..."
echo "=============================================="

# Formateo
echo ""
./scripts/format.sh

# Linting
echo ""
./scripts/lint.sh

# Tests
echo ""
echo "🧪 Ejecutando tests con coverage..."
pytest tests/ -v --cov=app --cov-report=html --cov-report=term

echo ""
echo "=============================================="
echo "✅ Revisión de calidad completada"
echo "📊 Ver reporte de coverage en: htmlcov/index.html"
