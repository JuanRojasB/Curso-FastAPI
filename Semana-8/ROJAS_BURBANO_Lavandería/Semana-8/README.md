# Semana 8: Testing y Calidad de Código
## Lavandería Express QuickClean - ROJAS BURBANO

**Ficha:** 3147246  
**Dominio:** Lavandería Express QuickClean  
**Tipo Genérico:** Tipo C - Servicios Usuario + CI/CD Básico  
**Estudiante:** ROJAS BURBANO

---

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema completo de testing, documentación y calidad de código para la API de **Lavandería Express QuickClean**, enfocado en:

- Gestión de servicios de lavandería para usuarios
- Testing completo de endpoints de servicios
- Documentación avanzada con OpenAPI
- Métricas de calidad de código
- Integración Continua (CI/CD) básico

---

## 🎯 Objetivos de la Semana

1. ✅ Implementar suite completa de tests con pytest
2. ✅ Configurar testing de APIs con TestClient
3. ✅ Generar documentación avanzada automática
4. ✅ Establecer métricas de calidad de código
5. ✅ Configurar CI/CD básico con GitHub Actions

---

## 📁 Estructura del Proyecto

```
Semana-8/
├── README.md                           # Este archivo
├── app/                                # Código fuente de la aplicación
│   ├── __init__.py
│   ├── main.py                         # Aplicación FastAPI principal
│   ├── models/                         # Modelos y esquemas
│   │   ├── __init__.py
│   │   └── schemas.py                  # Esquemas Pydantic
│   ├── routers/                        # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── servicios.py               # Endpoints de servicios
│   │   ├── ordenes.py                 # Endpoints de órdenes
│   │   └── clientes.py                # Endpoints de clientes
│   ├── database.py                     # Configuración de base de datos
│   └── docs/                           # Configuración de documentación
│       ├── __init__.py
│       └── descriptions.py             # Descripciones para OpenAPI
├── tests/                              # Suite de tests
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures generales
│   ├── test_servicios/                # Tests de servicios
│   │   ├── __init__.py
│   │   ├── test_endpoints.py
│   │   └── test_validaciones.py
│   ├── test_ordenes/                  # Tests de órdenes
│   │   ├── __init__.py
│   │   ├── test_crud.py
│   │   └── test_estados.py
│   └── test_clientes/                 # Tests de clientes
│       ├── __init__.py
│       └── test_perfil.py
├── scripts/                            # Scripts de utilidad
│   ├── format.sh                       # Script de formateo
│   ├── lint.sh                         # Script de linting
│   └── quality.sh                      # Script de calidad completa
├── .github/                            # Configuración GitHub
│   └── workflows/
│       └── ci.yml                      # Pipeline de CI/CD
├── docs/                               # Documentación adicional
│   ├── PRACTICA_27.md                 # Pytest Basics
│   ├── PRACTICA_28.md                 # API Testing
│   ├── PRACTICA_29.md                 # Advanced Docs
│   └── PRACTICA_30.md                 # Code Quality & CI
├── pytest.ini                          # Configuración de pytest
├── pyproject.toml                      # Configuración de herramientas
├── .flake8                             # Configuración de flake8
├── .pre-commit-config.yaml            # Pre-commit hooks
├── .coveragerc                         # Configuración de coverage
├── requirements.txt                    # Dependencias principales
├── requirements-dev.txt                # Dependencias de desarrollo
└── CONTRIBUTING.md                     # Guía de contribución
```

---

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Dependencias principales
pip install -r requirements.txt

# Dependencias de desarrollo
pip install -r requirements-dev.txt
```

### 2. Configurar Base de Datos de Testing

```bash
# Las bases de datos de prueba se crean automáticamente
# al ejecutar los tests
```

### 3. Instalar Pre-commit Hooks

```bash
pre-commit install
```

---

## 🧪 Ejecución de Tests

### Tests Completos

```bash
# Ejecutar todos los tests con coverage
pytest tests/ -v --cov=app --cov-report=html
```

### Tests por Categoría

```bash
# Tests de servicios únicamente
pytest tests/test_servicios/ -v

# Tests de órdenes únicamente
pytest tests/test_ordenes/ -v

# Tests de clientes únicamente
pytest tests/test_clientes/ -v
```

### Tests con Marcadores

```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Tests específicos Tipo C
pytest -m tipo_c
```

---

## 📊 Calidad de Código

### Formateo Automático

```bash
# Formatear código con Black
black app/ tests/

# Organizar imports con isort
isort app/ tests/
```

### Linting

```bash
# Verificar estilo de código
flake8 app/ tests/

# Verificación de tipos
mypy app/

# Análisis de seguridad
bandit -r app/
```

### Script de Calidad Completa

```bash
# En Linux/Mac
./scripts/quality.sh

# En Windows PowerShell
.\scripts\quality.ps1
```

---

## 📚 Documentación API

### Acceder a Documentación Interactiva

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Abrir navegador en:
# http://localhost:8000/docs        (Swagger UI)
# http://localhost:8000/redoc       (ReDoc)
```

---

## 🔄 CI/CD

### GitHub Actions

El proyecto incluye un pipeline de CI/CD que se ejecuta automáticamente en:

- Push a rama `main` o `develop`
- Pull Requests a `main`

**Validaciones automáticas:**
- ✅ Formateo de código (Black)
- ✅ Organización de imports (isort)
- ✅ Linting (flake8)
- ✅ Verificación de tipos (mypy)
- ✅ Análisis de seguridad (bandit)
- ✅ Ejecución de tests
- ✅ Reporte de coverage

---

## 📝 Prácticas Implementadas

### Práctica 27: Pytest y Testing Básico ✅
- Configuración de pytest para Lavandería
- Fixtures reutilizables para servicios
- Tests básicos de servicios de lavandería
- Estructura escalable de testing

### Práctica 28: Testing de APIs Completo ✅
- TestClient para endpoints de lavandería
- Tests de autenticación de clientes
- Tests CRUD completos de servicios y órdenes
- Validación de responses y status codes

### Práctica 29: Documentación Avanzada ✅
- Esquemas Pydantic documentados para servicios
- OpenAPI personalizado para lavandería
- Documentación interactiva completa
- Ejemplos específicos del dominio

### Práctica 30: Code Quality & CI ✅
- Herramientas de calidad configuradas
- GitHub Actions CI/CD básico
- Pre-commit hooks instalados
- Métricas de calidad implementadas

---

## 🎯 Objetivos de Coverage

- **Target Mínimo:** 80%
- **Target Objetivo:** 90%
- **Áreas Críticas:** 95%

---

## 📈 Métricas de Calidad

### Estándares Implementados

- **Formateo:** Black (88 caracteres por línea)
- **Imports:** isort (perfil black)
- **Linting:** flake8 (configuración personalizada)
- **Tipos:** mypy (verificación estática)
- **Seguridad:** bandit (análisis de vulnerabilidades)

---

## 🤝 Contribución

Para contribuir al proyecto, consulta [CONTRIBUTING.md](CONTRIBUTING.md)

### Proceso de Desarrollo

1. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
2. Desarrollar siguiendo estándares
3. Ejecutar suite de calidad: `./scripts/quality.sh`
4. Commit con conventional commits
5. Push y crear Pull Request

---

## 📞 Contacto

**Estudiante:** ROJAS BURBANO  
**Ficha:** 3147246  
**Dominio:** Lavandería Express QuickClean  

---

## 📄 Licencia

Este proyecto es parte del material educativo de la Ficha 3147246.

---

**SEMANA 8 - TESTING Y CALIDAD DE CÓDIGO**  
_Lavandería Express QuickClean - Sistema de Gestión de Servicios_
