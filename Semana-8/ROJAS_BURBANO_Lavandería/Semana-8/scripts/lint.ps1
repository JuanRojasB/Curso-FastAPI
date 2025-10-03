# Script de Linting - Lavandería Express QuickClean (PowerShell)
# ROJAS BURBANO - Ficha 3147246

Write-Host "🔍 Ejecutando flake8..." -ForegroundColor Cyan
flake8 app/ tests/

Write-Host ""
Write-Host "🔒 Ejecutando bandit (seguridad)..." -ForegroundColor Cyan
bandit -r app/

Write-Host ""
Write-Host "🏷️  Ejecutando mypy (tipos)..." -ForegroundColor Cyan
mypy app/

Write-Host ""
Write-Host "✅ Linting completado" -ForegroundColor Green
