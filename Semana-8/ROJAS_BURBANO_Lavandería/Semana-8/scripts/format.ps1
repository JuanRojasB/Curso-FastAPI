# Script de Formateo - Lavandería Express QuickClean (PowerShell)
# ROJAS BURBANO - Ficha 3147246

Write-Host "🎨 Formateando código con Black..." -ForegroundColor Cyan
black app/ tests/

Write-Host ""
Write-Host "📦 Organizando imports con isort..." -ForegroundColor Cyan
isort app/ tests/

Write-Host ""
Write-Host "✅ Formateo completado exitosamente" -ForegroundColor Green
