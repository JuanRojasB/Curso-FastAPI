# 🚀 Instrucciones de Ejecución - Lavandería Express QuickClean

## ⚡ Inicio Rápido (5 minutos)

### 1. Activar entorno virtual

**Windows PowerShell:**
```powershell
cd Semana-8
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
cd Semana-8
source venv/bin/activate
```

### 2. Instalar dependencias (primera vez)

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

✅ **La API estará disponible en:** http://localhost:8000

---

## 🧪 Ejecutar Tests

### Opción 1: Tests completos con coverage (RECOMENDADO)

```bash
pytest
```

**Resultado esperado:**
```
tests/test_clientes/test_perfil.py ........     [40%]
tests/test_servicios/test_endpoints.py .....    [65%]
tests/test_ordenes/test_crud.py .......        [100%]

----------- coverage: platform win32, python 3.11 -----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
app/main.py                      25      3    88%
app/routers/clientes.py          35      4    89%
app/routers/servicios.py         32      3    91%
app/routers/ordenes.py           40      5    88%
-------------------------------------------------
TOTAL                           192     22    89%

======================== 20 passed in 2.45s ========================
```

### Opción 2: Tests por módulo

```bash
# Solo clientes
pytest tests/test_clientes/ -v

# Solo servicios
pytest tests/test_servicios/ -v

# Solo órdenes
pytest tests/test_ordenes/ -v
```

### Opción 3: Ver reporte HTML de coverage

```bash
pytest --cov-report=html
```

Luego abrir el archivo: `htmlcov/index.html` en el navegador

---

## 🎨 Herramientas de Calidad de Código

### Formateo con Black

```bash
# Formatear todo el código
black app tests
```

### Linting con Ruff

```bash
# Verificar estilo de código
ruff check app tests

# Auto-fix problemas
ruff check --fix app tests
```

### Type Checking con MyPy

```bash
mypy app
```

### Suite Completa de Calidad

**Windows PowerShell:**
```powershell
.\scripts\quality.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/quality.sh
./scripts/quality.sh
```

Esto ejecuta:
1. Black (formateo)
2. Ruff (linting)
3. MyPy (type checking)
4. Pytest (tests + coverage)

---

## 📚 Acceder a la Documentación API

### 1. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

### 2. Abrir en el navegador

- **Swagger UI (Interactivo):** http://localhost:8000/docs
- **ReDoc (Documentación):** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### 3. Probar endpoints desde Swagger

1. Expandir un endpoint (ej: `POST /api/clientes`)
2. Click en "Try it out"
3. Modificar el JSON de ejemplo
4. Click en "Execute"
5. Ver la respuesta

---

## 🔍 Verificar Prácticas

### Práctica 27: Fundamentos de pytest

```bash
# Ejecutar tests con pytest
pytest -v

# Ver coverage
pytest --cov=app --cov-report=term-missing
```

**Archivo de referencia:** `docs/PRACTICA-27-PYTEST-BASICS.md`

### Práctica 28: Testing de API

```bash
# Tests de endpoints
pytest tests/test_clientes/ -v
pytest tests/test_servicios/ -v
pytest tests/test_ordenes/ -v
```

**Archivo de referencia:** `docs/PRACTICA-28-API-TESTING.md`

### Práctica 29: Documentación Avanzada

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Luego visitar: http://localhost:8000/docs
```

**Archivo de referencia:** `docs/PRACTICA-29-ADVANCED-DOCS.md`

### Práctica 30: Calidad de Código y CI/CD

**Windows:**
```powershell
.\scripts\quality.ps1
```

**Linux/Mac:**
```bash
./scripts/quality.sh
```

**Archivo de referencia:** `docs/PRACTICA-30-CODE-QUALITY-CI.md`

---

## 📊 Comandos de Diagnóstico

### Verificar instalación de dependencias

```bash
pip list
```

Debe mostrar: fastapi, uvicorn, pytest, black, ruff, mypy, etc.

### Verificar versión de Python

```bash
python --version
```

Debe ser: Python 3.11 o superior

### Verificar estructura del proyecto

**Windows:**
```powershell
tree /F
```

**Linux/Mac:**
```bash
tree
```

### Ver logs detallados de tests

```bash
pytest -v --tb=short
```

---

## ⚠️ Solución de Problemas Comunes

### Error: "No module named 'app'"

**Solución:**
```bash
# Verificar que estás en el directorio correcto
pwd  # debe mostrar .../Semana-8

# Reinstalar en modo editable
pip install -e .
```

### Error: "uvicorn: command not found"

**Solución:**
```bash
# Verificar que el entorno virtual está activado
# Reinstalar uvicorn
pip install uvicorn[standard]
```

### Tests fallan con errores de import

**Solución:**
```bash
# Limpiar cache de pytest
pytest --cache-clear

# Eliminar archivos __pycache__
# Windows:
Get-ChildItem -Recurse __pycache__ | Remove-Item -Recurse -Force

# Linux/Mac:
find . -type d -name __pycache__ -exec rm -r {} +
```

### Coverage muy bajo

**Solución:**
```bash
# Ver qué líneas no están cubiertas
pytest --cov=app --cov-report=term-missing

# Ver reporte detallado en HTML
pytest --cov-report=html
# Abrir htmlcov/index.html
```

### Puerto 8000 ya en uso

**Solución:**
```bash
# Usar otro puerto
uvicorn app.main:app --reload --port 8001
```

---

## 📋 Checklist de Verificación Pre-Entrega

Antes de entregar, verificar que:

- [ ] Entorno virtual activado
- [ ] Todas las dependencias instaladas
- [ ] Aplicación inicia sin errores
- [ ] Swagger UI accesible (http://localhost:8000/docs)
- [ ] Todos los tests pasan (`pytest`)
- [ ] Coverage > 80% (`pytest --cov=app`)
- [ ] Black sin errores (`black --check app tests`)
- [ ] Ruff sin errores (`ruff check app tests`)
- [ ] Scripts de calidad ejecutan correctamente
- [ ] Reportes HTML generados
- [ ] Documentación de prácticas completa

---

## 🎯 Flujo Completo de Ejecución

```bash
# 1. Activar entorno
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# 2. Instalar dependencias (primera vez)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Ejecutar suite completa de calidad
.\scripts\quality.ps1  # Windows
./scripts/quality.sh    # Linux/Mac

# 4. Iniciar aplicación
uvicorn app.main:app --reload

# 5. Abrir navegador
# http://localhost:8000/docs

# 6. Generar reporte de coverage
pytest --cov-report=html

# 7. Abrir reporte
# htmlcov/index.html
```

---

## 📞 Información del Proyecto

**Estudiante:** ROJAS BURBANO  
**Dominio:** Lavandería Express QuickClean  
**Tipo:** C - Servicios Usuario + CI/CD Básico  
**Ficha:** 3147246  
**Semana:** 8

---

**¡Todo listo para ejecutar y entregar! 🎉**
