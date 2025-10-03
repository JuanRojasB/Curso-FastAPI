# Script de Calidad Completa - Lavandería Express QuickClean (PowerShell)
# ROJAS BURBANO - Ficha 3147246

Write-Host "🚀 Ejecutando revisión completa de calidad..." -ForegroundColor Yellow
Write-Host "=============================================="

# Formateo
Write-Host ""
& .\scripts\format.ps1

# Linting
Write-Host ""
& .\scripts\lint.ps1

# Tests
Write-Host ""
Write-Host "🧪 Ejecutando tests con coverage..." -ForegroundColor Cyan
pytest tests/ -v --cov=app --cov-report=html --cov-report=term

Write-Host ""
Write-Host "=============================================="
Write-Host "✅ Revisión de calidad completada" -ForegroundColor Green
Write-Host "📊 Ver reporte de coverage en: htmlcov/index.html" -ForegroundColor Cyan
