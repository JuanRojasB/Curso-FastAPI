# Práctica 28: Testing de API - Lavandería Express QuickClean

## 🎯 Objetivos de la Práctica

- Implementar tests exhaustivos de endpoints REST
- Validar códigos de respuesta HTTP
- Verificar estructura de datos JSON
- Testear validaciones y errores

## 📋 Endpoints a Testear

### 1. Clientes API (`/api/clientes`)

| Método | Endpoint                  | Test                          |
|--------|---------------------------|-------------------------------|
| POST   | /api/clientes             | Crear cliente                 |
| GET    | /api/clientes             | Listar clientes               |
| GET    | /api/clientes/{id}        | Obtener cliente específico    |
| PUT    | /api/clientes/{id}        | Actualizar cliente            |
| DELETE | /api/clientes/{id}        | Eliminar cliente              |

### 2. Servicios API (`/api/servicios`)

| Método | Endpoint                  | Test                          |
|--------|---------------------------|-------------------------------|
| POST   | /api/servicios            | Crear servicio                |
| GET    | /api/servicios            | Listar servicios              |
| GET    | /api/servicios/{id}       | Obtener servicio              |
| PUT    | /api/servicios/{id}       | Actualizar servicio           |
| PUT    | /api/servicios/{id}/precio| Actualizar precio             |

### 3. Órdenes API (`/api/ordenes`)

| Método | Endpoint                  | Test                          |
|--------|---------------------------|-------------------------------|
| POST   | /api/ordenes              | Crear orden                   |
| GET    | /api/ordenes              | Listar órdenes                |
| GET    | /api/ordenes/{id}         | Obtener orden                 |
| PUT    | /api/ordenes/{id}/estado  | Actualizar estado             |
| GET    | /api/ordenes/cliente/{id} | Órdenes por cliente           |

## 🧪 Casos de Prueba Implementados

### Tests de Clientes

```python
def test_crear_cliente_exitoso(client):
    """POST /api/clientes - Crear cliente válido"""
    response = client.post("/api/clientes", json={
        "nombre": "Juan Pérez",
        "email": "juan@example.com",
        "telefono": "3001234567",
        "direccion": "Calle 123 #45-67"
    })
    assert response.status_code == 201
    assert response.json()["nombre"] == "Juan Pérez"

def test_crear_cliente_email_duplicado(client, sample_cliente):
    """POST /api/clientes - Error email duplicado"""
    response = client.post("/api/clientes", json={
        "nombre": "Otro Usuario",
        "email": sample_cliente["email"],  # Email ya existe
        "telefono": "3009876543",
        "direccion": "Otra dirección"
    })
    assert response.status_code == 400
```

### Tests de Servicios

```python
def test_crear_servicio_lavado(client):
    """POST /api/servicios - Crear servicio de lavado"""
    response = client.post("/api/servicios", json={
        "nombre": "Lavado Express",
        "descripcion": "Lavado rápido en 24 horas",
        "precio": 15000.0,
        "tipo": "lavado",
        "activo": True
    })
    assert response.status_code == 201
    assert response.json()["tipo"] == "lavado"

def test_actualizar_precio_servicio(client, sample_servicio):
    """PUT /api/servicios/{id}/precio - Actualizar precio"""
    response = client.put(
        f"/api/servicios/{sample_servicio['id']}/precio",
        json={"precio": 18000.0}
    )
    assert response.status_code == 200
    assert response.json()["precio"] == 18000.0
```

### Tests de Órdenes

```python
def test_crear_orden_completa(client, sample_cliente, sample_servicio):
    """POST /api/ordenes - Crear orden con servicios"""
    response = client.post("/api/ordenes", json={
        "cliente_id": sample_cliente["id"],
        "servicios": [
            {
                "servicio_id": sample_servicio["id"],
                "cantidad": 2,
                "descripcion": "2 camisas"
            }
        ],
        "notas": "Entrega urgente"
    })
    assert response.status_code == 201
    assert "total" in response.json()
    assert response.json()["estado"] == "recibida"

def test_actualizar_estado_orden(client, sample_orden):
    """PUT /api/ordenes/{id}/estado - Cambiar estado"""
    response = client.put(
        f"/api/ordenes/{sample_orden['id']}/estado",
        json={"estado": "en_proceso"}
    )
    assert response.status_code == 200
    assert response.json()["estado"] == "en_proceso"
```

## 🔍 Validaciones Implementadas

### 1. Validación de Datos de Entrada
- Campos requeridos presentes
- Tipos de datos correctos
- Formato de email válido
- Números de teléfono válidos
- Valores numéricos positivos

### 2. Validación de Respuestas
- Códigos HTTP correctos (200, 201, 400, 404)
- Estructura JSON esperada
- Campos de respuesta completos
- Timestamps válidos

### 3. Validación de Errores
- 400 Bad Request: Datos inválidos
- 404 Not Found: Recurso no existe
- 409 Conflict: Duplicados
- 422 Unprocessable Entity: Validación fallida

## 📊 Ejecutar Tests de API

```bash
# Todos los tests de API
pytest tests/ -v

# Solo endpoints de clientes
pytest tests/test_clientes/test_perfil.py -v

# Con coverage detallado
pytest --cov=app.routers --cov-report=term-missing

# Generar reporte JSON
pytest --json-report --json-report-file=report.json
```

## ✅ Criterios de Éxito

- [ ] Todos los endpoints probados
- [ ] Códigos HTTP correctos validados
- [ ] Respuestas JSON verificadas
- [ ] Casos de error manejados
- [ ] Validaciones de datos implementadas
- [ ] Coverage de routers > 85%

## 📈 Resultados Esperados

```
tests/test_clientes/test_perfil.py::test_crear_cliente_exitoso PASSED
tests/test_clientes/test_perfil.py::test_obtener_cliente_existente PASSED
tests/test_clientes/test_perfil.py::test_cliente_no_encontrado PASSED
tests/test_servicios/test_endpoints.py::test_crear_servicio_lavado PASSED
tests/test_servicios/test_endpoints.py::test_actualizar_precio PASSED
tests/test_ordenes/test_crud.py::test_crear_orden_completa PASSED
tests/test_ordenes/test_crud.py::test_actualizar_estado PASSED

========================= 20 passed in 2.45s =========================
```

## 🎓 Entregables

1. Tests completos de todos los endpoints
2. Validaciones de datos implementadas
3. Manejo de errores testeado
4. Reporte de coverage de routers
5. Documentación de casos de prueba

---

**Práctica 28 - ROJAS BURBANO - Lavandería Express QuickClean**
