# Práctica 30: Calidad de Código y CI/CD - Lavandería Express QuickClean

## 🎯 Objetivos de la Práctica

- Configurar herramientas de calidad de código
- Implementar linting y formateo automático
- Configurar GitHub Actions para CI básico
- Generar reportes de calidad y cobertura

## 🔧 Herramientas de Calidad

### 1. Black - Formateo de Código

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

**Uso:**
```bash
# Formatear todo el proyecto
black app tests

# Ver cambios sin aplicar
black --check app tests

# Formatear archivo específico
black app/main.py
```

### 2. Ruff - Linting Rápido

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
]

ignore = [
    "E501",  # line too long (manejado por black)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # imported but unused
```

**Uso:**
```bash
# Ejecutar linting
ruff check app tests

# Auto-fix problemas
ruff check --fix app tests

# Ver estadísticas
ruff check --statistics app tests
```

### 3. MyPy - Type Checking

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true
```

**Uso:**
```bash
# Type checking completo
mypy app

# Con reporte detallado
mypy --show-error-codes app
```

### 4. Pytest + Coverage

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=app
    --cov-report=term-missing:skip-covered
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=80

[coverage:run]
source = app
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[coverage:report]
precision = 2
show_missing = true
skip_covered = false
```

## 📜 Scripts de Calidad

### Scripts PowerShell (Windows)

**format.ps1:**
```powershell
# Formateo automático
Write-Host "🎨 Formateando código con Black..." -ForegroundColor Cyan
black app tests

Write-Host "✅ Formateo completado" -ForegroundColor Green
```

**lint.ps1:**
```powershell
# Linting completo
Write-Host "🔍 Ejecutando Ruff..." -ForegroundColor Cyan
ruff check app tests

Write-Host "🔍 Ejecutando MyPy..." -ForegroundColor Cyan
mypy app

Write-Host "✅ Linting completado" -ForegroundColor Green
```

**quality.ps1:**
```powershell
# Suite completa de calidad
Write-Host "🚀 Iniciando verificación de calidad..." -ForegroundColor Cyan

Write-Host "`n📋 Paso 1: Formateo" -ForegroundColor Yellow
black app tests

Write-Host "`n📋 Paso 2: Linting" -ForegroundColor Yellow
ruff check app tests

Write-Host "`n📋 Paso 3: Type Checking" -ForegroundColor Yellow
mypy app

Write-Host "`n📋 Paso 4: Tests + Coverage" -ForegroundColor Yellow
pytest

Write-Host "`n✅ Verificación completada" -ForegroundColor Green
```

### Scripts Bash (Linux/Mac)

**format.sh:**
```bash
#!/bin/bash
echo "🎨 Formateando código con Black..."
black app tests
echo "✅ Formateo completado"
```

**lint.sh:**
```bash
#!/bin/bash
echo "🔍 Ejecutando Ruff..."
ruff check app tests

echo "🔍 Ejecutando MyPy..."
mypy app

echo "✅ Linting completado"
```

**quality.sh:**
```bash
#!/bin/bash
echo "🚀 Iniciando verificación de calidad..."

echo "📋 Paso 1: Formateo"
black app tests

echo "📋 Paso 2: Linting"
ruff check app tests

echo "📋 Paso 3: Type Checking"
mypy app

echo "📋 Paso 4: Tests + Coverage"
pytest

echo "✅ Verificación completada"
```

## 🔄 GitHub Actions CI/CD

### .github/workflows/ci.yml

```yaml
name: CI - Lavandería Express QuickClean

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    name: Code Quality & Tests
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout código
      uses: actions/checkout@v3
    
    - name: 🐍 Configurar Python 3.11
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: 📦 Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: 🎨 Verificar formateo con Black
      run: black --check app tests
    
    - name: 🔍 Linting con Ruff
      run: ruff check app tests
    
    - name: 🔍 Type checking con MyPy
      run: mypy app
    
    - name: 🧪 Ejecutar tests con coverage
      run: |
        pytest --cov=app --cov-report=xml --cov-report=term
    
    - name: 📊 Upload coverage a Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
    
    - name: ✅ Verificación completada
      run: echo "✅ Todas las verificaciones pasaron correctamente"
```

### Pre-commit Hooks (Opcional)

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.10.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.3
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

## 📊 Métricas de Calidad Esperadas

### Coverage Target
```
Módulo                  Stmts   Miss  Cover
-------------------------------------------
app/__init__.py             0      0   100%
app/main.py                25      3    88%
app/database.py            15      2    87%
app/models/schemas.py      45      5    89%
app/routers/clientes.py    35      4    89%
app/routers/servicios.py   32      3    91%
app/routers/ordenes.py     40      5    88%
-------------------------------------------
TOTAL                     192     22    89%

✅ Target: > 80% - CUMPLIDO
```

### Linting Target
```
✅ 0 errores de sintaxis
✅ 0 errores de estilo críticos
✅ 0 imports sin usar
✅ 0 variables sin usar
⚠️ < 5 warnings permitidos
```

## 🚀 Ejecutar Verificación Completa

```bash
# Windows PowerShell
.\scripts\quality.ps1

# Linux/Mac
./scripts/quality.sh

# O manualmente:
black app tests && ruff check app tests && mypy app && pytest
```

## ✅ Criterios de Éxito

- [ ] Black configurado y ejecutándose
- [ ] Ruff sin errores críticos
- [ ] MyPy configurado (opcional)
- [ ] Coverage > 80%
- [ ] GitHub Actions CI funcionando
- [ ] Scripts de calidad ejecutables
- [ ] Pre-commit hooks configurados (opcional)
- [ ] Badge de CI en README

## 🎓 Entregables

1. Configuración pyproject.toml completa
2. Scripts de calidad funcionales
3. GitHub Actions CI configurado
4. Reporte de coverage > 80%
5. Badge de CI/CD en README
6. Screenshots de pipeline exitoso

## 📈 Badges Recomendados

```markdown
# README.md
![CI](https://github.com/usuario/repo/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/usuario/repo/branch/main/graph/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
```

---

**Práctica 30 - ROJAS BURBANO - Lavandería Express QuickClean**
