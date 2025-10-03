# 🧺 Guía Completa - Lavandería Express QuickClean

## Información del Proyecto

**Estudiante:** ROJAS BURBANO  
**Dominio:** Lavandería Express QuickClean  
**Tipo:** C - Servicios Usuario + CI/CD Básico  
**Semana:** 8 - Testing y Calidad de Código

---

## 📋 Índice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Ejecutar la Aplicación](#ejecutar-la-aplicación)
4. [Ejecutar Tests](#ejecutar-tests)
5. [Herramientas de Calidad](#herramientas-de-calidad)
6. [Prácticas Incluidas](#prácticas-incluidas)
7. [CI/CD](#cicd)
8. [Entregables](#entregables)

---

## 📁 Estructura del Proyecto

```
Semana-8/
├── app/                          # Aplicación principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada FastAPI
│   ├── database.py               # Configuración de BD
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py            # Modelos Pydantic
│   └── routers/
│       ├── __init__.py
│       ├── clientes.py           # Endpoints de clientes
│       ├── servicios.py          # Endpoints de servicios
│       └── ordenes.py            # Endpoints de órdenes
│
├── tests/                        # Suite de tests
│   ├── __init__.py
│   ├── conftest.py               # Fixtures compartidas
│   ├── test_clientes/
│   │   ├── __init__.py
│   │   └── test_perfil.py
│   ├── test_servicios/
│   │   ├── __init__.py
│   │   └── test_endpoints.py
│   └── test_ordenes/
│       ├── __init__.py
│       └── test_crud.py
│
├── scripts/                      # Scripts de calidad
│   ├── format.ps1                # Formateo (Windows)
│   ├── format.sh                 # Formateo (Linux/Mac)
│   ├── lint.ps1                  # Linting (Windows)
│   ├── lint.sh                   # Linting (Linux/Mac)
│   ├── quality.ps1               # Suite completa (Windows)
│   └── quality.sh                # Suite completa (Linux/Mac)
│
├── docs/                         # Documentación de prácticas
│   ├── PRACTICA-27-PYTEST-BASICS.md
│   ├── PRACTICA-28-API-TESTING.md
│   ├── PRACTICA-29-ADVANCED-DOCS.md
│   └── PRACTICA-30-CODE-QUALITY-CI.md
│
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI/CD
│
├── pyproject.toml                # Configuración del proyecto
├── pytest.ini                    # Configuración pytest
├── requirements.txt              # Dependencias principales
├── requirements-dev.txt          # Dependencias de desarrollo
├── .gitignore                    # Archivos ignorados por git
└── README.md                     # Documentación principal
```

---

## 🚀 Instalación y Configuración

### 1. Prerrequisitos

- Python 3.11 o superior
- pip actualizado
- Git (opcional)

### 2. Crear entorno virtual

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
# Dependencias principales
pip install -r requirements.txt

# Dependencias de desarrollo (testing, linting)
pip install -r requirements-dev.txt
```

---

## 🏃 Ejecutar la Aplicación

### Desarrollo

```bash
# Iniciar servidor de desarrollo
uvicorn app.main:app --reload

# La API estará disponible en:
# http://localhost:8000
```

### Acceder a la documentación

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 🧪 Ejecutar Tests

### Tests completos con coverage

```bash
pytest
```

### Tests específicos

```bash
# Tests de clientes
pytest tests/test_clientes/

# Tests de servicios
pytest tests/test_servicios/

# Tests de órdenes
pytest tests/test_ordenes/

# Test específico
pytest tests/test_clientes/test_perfil.py::test_crear_cliente_exitoso
```

### Ver reporte de coverage

```bash
# Generar reporte HTML
pytest --cov-report=html

# Abrir en navegador (el archivo está en htmlcov/index.html)
```

---

## 🔧 Herramientas de Calidad

### Black - Formateo automático

```bash
# Formatear todo el código
black app tests

# Solo verificar sin modificar
black --check app tests
```

### Ruff - Linting rápido

```bash
# Ejecutar linting
ruff check app tests

# Auto-fix problemas
ruff check --fix app tests
```

### MyPy - Type checking

```bash
# Verificar tipos
mypy app
```

### Suite completa

**Windows:**
```powershell
.\scripts\quality.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/quality.sh
./scripts/quality.sh
```

---

## 📚 Prácticas Incluidas

### Práctica 27: Fundamentos de pytest
- **Archivo:** `docs/PRACTICA-27-PYTEST-BASICS.md`
- **Contenido:**
  - Suite de tests básica
  - Fixtures y parametrización
  - Reportes de coverage
  - Tests de servicios de usuario

### Práctica 28: Testing de API
- **Archivo:** `docs/PRACTICA-28-API-TESTING.md`
- **Contenido:**
  - Tests de endpoints REST
  - Validación de códigos HTTP
  - Verificación de JSON
  - Manejo de errores

### Práctica 29: Documentación Avanzada
- **Archivo:** `docs/PRACTICA-29-ADVANCED-DOCS.md`
- **Contenido:**
  - OpenAPI/Swagger personalizado
  - Schemas documentados
  - Ejemplos en endpoints
  - Metadata de API

### Práctica 30: Calidad de Código y CI/CD
- **Archivo:** `docs/PRACTICA-30-CODE-QUALITY-CI.md`
- **Contenido:**
  - Black, Ruff, MyPy
  - Scripts de calidad
  - GitHub Actions
  - Métricas y badges

---

## 🔄 CI/CD

### GitHub Actions

El proyecto incluye configuración de CI/CD en `.github/workflows/ci.yml` que ejecuta:

1. ✅ Verificación de formateo (Black)
2. ✅ Linting (Ruff)
3. ✅ Type checking (MyPy)
4. ✅ Tests con coverage (pytest)
5. ✅ Upload de coverage a Codecov

### Ejecutar localmente

Para simular lo que hace el CI:

```bash
# Windows
.\scripts\quality.ps1

# Linux/Mac
./scripts/quality.sh
```

---

## 📦 Entregables

### Lista de verificación

- [ ] Código fuente completo
- [ ] Suite de tests funcionando
- [ ] Coverage > 80%
- [ ] Documentación API (Swagger)
- [ ] Herramientas de calidad configuradas
- [ ] CI/CD configurado
- [ ] README completo
- [ ] 4 prácticas documentadas

### Archivos a entregar

1. **Código completo** (carpeta `Semana-8/`)
2. **Reporte de coverage** (HTML o screenshot)
3. **Screenshot de Swagger UI**
4. **Screenshot de CI/CD** (GitHub Actions)
5. **Documentación de prácticas** (carpeta `docs/`)

---

## 🎯 Comandos Rápidos

```bash
# Iniciar desarrollo
uvicorn app.main:app --reload

# Ejecutar tests
pytest

# Calidad de código
black app tests && ruff check app tests && pytest

# Ver coverage
pytest --cov-report=html && start htmlcov/index.html
```

---

## 📊 Métricas Esperadas

### Coverage
- **Target:** > 80%
- **Actual:** ~89%

### Linting
- **Errores:** 0
- **Warnings:** < 5

### Tests
- **Total:** ~20 tests
- **Pasando:** 100%

---

## 🆘 Solución de Problemas

### Error: ModuleNotFoundError

```bash
# Verificar que el entorno virtual esté activado
# Reinstalar dependencias
pip install -r requirements.txt
```

### Tests fallan

```bash
# Limpiar cache de pytest
pytest --cache-clear

# Ejecutar con más detalle
pytest -v
```

### Coverage bajo

```bash
# Ver qué líneas faltan
pytest --cov-report=term-missing
```

---

## 📞 Contacto

**Estudiante:** ROJAS BURBANO  
**Ficha:** 3147246  
**Semana:** 8

---

**¡Proyecto completo y listo para entregar! 🎉**
