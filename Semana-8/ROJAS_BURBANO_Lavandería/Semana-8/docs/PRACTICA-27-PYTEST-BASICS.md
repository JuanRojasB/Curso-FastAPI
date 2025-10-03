# Práctica 27: Fundamentos de pytest - Lavandería Express QuickClean

## 🎯 Objetivos de la Práctica

- Implementar suite de tests básica usando pytest
- Aplicar fixtures y parametrización
- Generar reportes de coverage
- Validar endpoints de servicios de usuario

## 📋 Contexto del Dominio

**Dominio:** Lavandería Express QuickClean  
**Tipo:** C - Servicios Usuario + CI/CD Básico  
**Estudiante:** ROJAS BURBANO

### Funcionalidades a Testear:

1. **Gestión de Clientes** (Usuarios del servicio)
2. **Gestión de Servicios** (Lavado, planchado, tintorería)
3. **Gestión de Órdenes** (Pedidos de lavandería)

## 🧪 Tests Implementados

### 1. Tests de Clientes (`test_clientes/test_perfil.py`)

```python
# Tests para gestión de perfiles de clientes
- test_crear_cliente_exitoso
- test_obtener_cliente_existente
- test_actualizar_cliente
- test_eliminar_cliente
- test_listar_todos_clientes
```

**Cobertura esperada:** > 80%

### 2. Tests de Servicios (`test_servicios/test_endpoints.py`)

```python
# Tests para catálogo de servicios de lavandería
- test_crear_servicio_lavado
- test_obtener_servicio
- test_listar_servicios_activos
- test_actualizar_precio_servicio
- test_desactivar_servicio
```

**Cobertura esperada:** > 80%

### 3. Tests de Órdenes (`test_ordenes/test_crud.py`)

```python
# Tests para gestión de órdenes de lavandería
- test_crear_orden_con_servicios
- test_obtener_orden_por_id
- test_actualizar_estado_orden
- test_calcular_total_orden
- test_listar_ordenes_cliente
```

**Cobertura esperada:** > 80%

## 🔧 Configuración de pytest

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
```

### Fixtures Principales (conftest.py)

1. **client**: Cliente de prueba FastAPI
2. **db**: Base de datos en memoria para tests
3. **sample_cliente**: Cliente de ejemplo
4. **sample_servicio**: Servicio de ejemplo
5. **sample_orden**: Orden de ejemplo

## 📊 Ejecutar Tests

```bash
# Todos los tests con coverage
pytest

# Tests específicos de clientes
pytest tests/test_clientes/

# Tests específicos con verbose
pytest -v tests/test_servicios/

# Generar reporte HTML
pytest --cov-report=html
```

## ✅ Criterios de Éxito

- [ ] Todos los tests pasan correctamente
- [ ] Coverage total > 80%
- [ ] Tests organizados por módulo
- [ ] Uso correcto de fixtures
- [ ] Parametrización implementada
- [ ] Reportes generados correctamente

## 📈 Resultados Esperados

```
tests/test_clientes/test_perfil.py ........     [33%]
tests/test_servicios/test_endpoints.py .....    [66%]
tests/test_ordenes/test_crud.py .......        [100%]

----------- coverage: platform win32, python 3.11 -----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
app/__init__.py                   0      0   100%
app/database.py                  15      2    87%
app/main.py                      25      3    88%
app/models/schemas.py            45      5    89%
app/routers/clientes.py          35      4    89%
app/routers/servicios.py         32      3    91%
app/routers/ordenes.py           40      5    88%
-------------------------------------------------
TOTAL                           192     22    89%
```

## 🎓 Entregables

1. Suite completa de tests implementada
2. Reporte de coverage HTML generado
3. Fixtures reutilizables configuradas
4. Documentación de casos de prueba
5. Screenshots de ejecución exitosa

---

**Práctica 27 - ROJAS BURBANO - Lavandería Express QuickClean**
