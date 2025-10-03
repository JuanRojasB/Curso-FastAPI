# 🧺 Ejemplos de Uso - API Lavandería Express QuickClean

## 📋 Tabla de Contenidos

1. [Gestión de Clientes](#gestión-de-clientes)
2. [Gestión de Servicios](#gestión-de-servicios)
3. [Gestión de Órdenes](#gestión-de-órdenes)
4. [Ejemplos con cURL](#ejemplos-con-curl)
5. [Ejemplos con Python](#ejemplos-con-python)

---

## 🙍 Gestión de Clientes

### 1. Crear un nuevo cliente

**Endpoint:** `POST /api/clientes`

```json
{
  "nombre": "Juan Pérez García",
  "email": "juan.perez@email.com",
  "telefono": "3001234567",
  "direccion": "Calle 123 #45-67, Bogotá"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez García",
  "email": "juan.perez@email.com",
  "telefono": "3001234567",
  "direccion": "Calle 123 #45-67, Bogotá",
  "fecha_registro": "2025-10-02T14:30:00",
  "activo": true
}
```

### 2. Listar todos los clientes

**Endpoint:** `GET /api/clientes`

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez García",
    "email": "juan.perez@email.com",
    "telefono": "3001234567",
    "direccion": "Calle 123 #45-67, Bogotá",
    "fecha_registro": "2025-10-02T14:30:00",
    "activo": true
  },
  {
    "id": 2,
    "nombre": "María Rodríguez",
    "email": "maria.rodriguez@email.com",
    "telefono": "3109876543",
    "direccion": "Carrera 50 #25-30, Medellín",
    "fecha_registro": "2025-10-02T15:00:00",
    "activo": true
  }
]
```

### 3. Obtener un cliente específico

**Endpoint:** `GET /api/clientes/1`

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez García",
  "email": "juan.perez@email.com",
  "telefono": "3001234567",
  "direccion": "Calle 123 #45-67, Bogotá",
  "fecha_registro": "2025-10-02T14:30:00",
  "activo": true
}
```

### 4. Actualizar un cliente

**Endpoint:** `PUT /api/clientes/1`

```json
{
  "nombre": "Juan Pérez García",
  "email": "juan.perez@email.com",
  "telefono": "3001234567",
  "direccion": "Carrera 15 #80-25, Bogotá"
}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez García",
  "email": "juan.perez@email.com",
  "telefono": "3001234567",
  "direccion": "Carrera 15 #80-25, Bogotá",
  "fecha_registro": "2025-10-02T14:30:00",
  "activo": true
}
```

### 5. Eliminar un cliente

**Endpoint:** `DELETE /api/clientes/1`

**Respuesta (204 No Content)**

---

## 🧼 Gestión de Servicios

### 1. Crear servicio de lavado

**Endpoint:** `POST /api/servicios`

```json
{
  "nombre": "Lavado Express 24h",
  "descripcion": "Lavado completo con entrega en 24 horas",
  "precio": 15000.0,
  "tipo": "lavado",
  "tiempo_estimado": 24,
  "activo": true
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "Lavado Express 24h",
  "descripcion": "Lavado completo con entrega en 24 horas",
  "precio": 15000.0,
  "tipo": "lavado",
  "tiempo_estimado": 24,
  "activo": true,
  "fecha_creacion": "2025-10-02T16:00:00"
}
```

### 2. Crear servicio de planchado

**Endpoint:** `POST /api/servicios`

```json
{
  "nombre": "Planchado Premium",
  "descripcion": "Planchado profesional con vapor para ropa delicada",
  "precio": 12000.0,
  "tipo": "planchado",
  "tiempo_estimado": 12,
  "activo": true
}
```

### 3. Crear servicio de tintorería

**Endpoint:** `POST /api/servicios`

```json
{
  "nombre": "Tintorería Especializada",
  "descripcion": "Limpieza en seco para prendas delicadas y trajes",
  "precio": 35000.0,
  "tipo": "tintoreria",
  "tiempo_estimado": 48,
  "activo": true
}
```

### 4. Listar todos los servicios

**Endpoint:** `GET /api/servicios`

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Lavado Express 24h",
    "descripcion": "Lavado completo con entrega en 24 horas",
    "precio": 15000.0,
    "tipo": "lavado",
    "tiempo_estimado": 24,
    "activo": true,
    "fecha_creacion": "2025-10-02T16:00:00"
  },
  {
    "id": 2,
    "nombre": "Planchado Premium",
    "descripcion": "Planchado profesional con vapor",
    "precio": 12000.0,
    "tipo": "planchado",
    "tiempo_estimado": 12,
    "activo": true,
    "fecha_creacion": "2025-10-02T16:05:00"
  }
]
```

### 5. Actualizar precio de servicio

**Endpoint:** `PUT /api/servicios/1/precio`

```json
{
  "precio": 18000.0
}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Lavado Express 24h",
  "descripcion": "Lavado completo con entrega en 24 horas",
  "precio": 18000.0,
  "tipo": "lavado",
  "tiempo_estimado": 24,
  "activo": true,
  "fecha_creacion": "2025-10-02T16:00:00"
}
```

---

## 📦 Gestión de Órdenes

### 1. Crear orden simple

**Endpoint:** `POST /api/ordenes`

```json
{
  "cliente_id": 1,
  "servicios": [
    {
      "servicio_id": 1,
      "cantidad": 3,
      "descripcion": "3 camisas blancas"
    }
  ],
  "notas": "Cliente preferencial"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "cliente_id": 1,
  "servicios": [
    {
      "servicio_id": 1,
      "cantidad": 3,
      "descripcion": "3 camisas blancas",
      "precio_unitario": 18000.0,
      "subtotal": 54000.0
    }
  ],
  "total": 54000.0,
  "estado": "recibida",
  "fecha_creacion": "2025-10-02T17:00:00",
  "fecha_entrega_estimada": "2025-10-03T17:00:00",
  "notas": "Cliente preferencial"
}
```

### 2. Crear orden con múltiples servicios

**Endpoint:** `POST /api/ordenes`

```json
{
  "cliente_id": 1,
  "servicios": [
    {
      "servicio_id": 1,
      "cantidad": 5,
      "descripcion": "5 camisas de vestir"
    },
    {
      "servicio_id": 2,
      "cantidad": 3,
      "descripcion": "3 pantalones"
    },
    {
      "servicio_id": 3,
      "cantidad": 1,
      "descripcion": "1 traje completo"
    }
  ],
  "fecha_entrega": "2025-10-05T10:00:00",
  "notas": "Entrega urgente - cliente empresarial"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "cliente_id": 1,
  "servicios": [
    {
      "servicio_id": 1,
      "cantidad": 5,
      "descripcion": "5 camisas de vestir",
      "precio_unitario": 18000.0,
      "subtotal": 90000.0
    },
    {
      "servicio_id": 2,
      "cantidad": 3,
      "descripcion": "3 pantalones",
      "precio_unitario": 12000.0,
      "subtotal": 36000.0
    },
    {
      "servicio_id": 3,
      "cantidad": 1,
      "descripcion": "1 traje completo",
      "precio_unitario": 35000.0,
      "subtotal": 35000.0
    }
  ],
  "total": 161000.0,
  "estado": "recibida",
  "fecha_creacion": "2025-10-02T17:15:00",
  "fecha_entrega": "2025-10-05T10:00:00",
  "notas": "Entrega urgente - cliente empresarial"
}
```

### 3. Actualizar estado de orden

**Endpoint:** `PUT /api/ordenes/1/estado`

```json
{
  "estado": "en_proceso"
}
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "estado": "en_proceso",
  "fecha_actualizacion": "2025-10-02T18:00:00"
}
```

**Estados posibles:**
- `recibida` - Orden recién creada
- `en_proceso` - En lavandería
- `lista` - Lista para entrega
- `entregada` - Entregada al cliente
- `cancelada` - Orden cancelada

### 4. Listar órdenes de un cliente

**Endpoint:** `GET /api/ordenes/cliente/1`

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "cliente_id": 1,
    "total": 54000.0,
    "estado": "en_proceso",
    "fecha_creacion": "2025-10-02T17:00:00",
    "fecha_entrega_estimada": "2025-10-03T17:00:00"
  },
  {
    "id": 2,
    "cliente_id": 1,
    "total": 161000.0,
    "estado": "recibida",
    "fecha_creacion": "2025-10-02T17:15:00",
    "fecha_entrega": "2025-10-05T10:00:00"
  }
]
```

---

## 💻 Ejemplos con cURL

### Crear cliente

```bash
curl -X POST "http://localhost:8000/api/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Ana López",
    "email": "ana.lopez@email.com",
    "telefono": "3207654321",
    "direccion": "Avenida 68 #45-30"
  }'
```

### Crear servicio

```bash
curl -X POST "http://localhost:8000/api/servicios" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Lavado Express",
    "descripcion": "Lavado rápido 24h",
    "precio": 15000.0,
    "tipo": "lavado",
    "tiempo_estimado": 24,
    "activo": true
  }'
```

### Crear orden

```bash
curl -X POST "http://localhost:8000/api/ordenes" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "servicios": [
      {
        "servicio_id": 1,
        "cantidad": 2,
        "descripcion": "2 camisas"
      }
    ],
    "notas": "Entrega mañana"
  }'
```

### Listar todos los clientes

```bash
curl -X GET "http://localhost:8000/api/clientes"
```

---

## 🐍 Ejemplos con Python (requests)

### Setup

```python
import requests

BASE_URL = "http://localhost:8000/api"
```

### Crear cliente

```python
def crear_cliente():
    url = f"{BASE_URL}/clientes"
    data = {
        "nombre": "Carlos Martínez",
        "email": "carlos.martinez@email.com",
        "telefono": "3151234567",
        "direccion": "Calle 72 #10-20"
    }
    response = requests.post(url, json=data)
    print(response.json())
    return response.json()

cliente = crear_cliente()
```

### Crear servicio

```python
def crear_servicio():
    url = f"{BASE_URL}/servicios"
    data = {
        "nombre": "Planchado Express",
        "descripcion": "Planchado rápido en 6 horas",
        "precio": 10000.0,
        "tipo": "planchado",
        "tiempo_estimado": 6,
        "activo": True
    }
    response = requests.post(url, json=data)
    return response.json()

servicio = crear_servicio()
```

### Crear orden completa

```python
def crear_orden(cliente_id, servicios):
    url = f"{BASE_URL}/ordenes"
    data = {
        "cliente_id": cliente_id,
        "servicios": servicios,
        "notas": "Orden creada desde Python"
    }
    response = requests.post(url, json=data)
    return response.json()

orden = crear_orden(
    cliente_id=1,
    servicios=[
        {
            "servicio_id": 1,
            "cantidad": 3,
            "descripcion": "3 camisas"
        },
        {
            "servicio_id": 2,
            "cantidad": 2,
            "descripcion": "2 pantalones"
        }
    ]
)
print(f"Orden creada: {orden['id']}, Total: ${orden['total']}")
```

### Actualizar estado de orden

```python
def actualizar_estado_orden(orden_id, nuevo_estado):
    url = f"{BASE_URL}/ordenes/{orden_id}/estado"
    data = {"estado": nuevo_estado}
    response = requests.put(url, json=data)
    return response.json()

actualizar_estado_orden(1, "en_proceso")
actualizar_estado_orden(1, "lista")
actualizar_estado_orden(1, "entregada")
```

### Listar órdenes de un cliente

```python
def obtener_ordenes_cliente(cliente_id):
    url = f"{BASE_URL}/ordenes/cliente/{cliente_id}"
    response = requests.get(url)
    ordenes = response.json()
    
    print(f"Cliente {cliente_id} tiene {len(ordenes)} órdenes:")
    for orden in ordenes:
        print(f"  - Orden #{orden['id']}: ${orden['total']} - {orden['estado']}")
    
    return ordenes

obtener_ordenes_cliente(1)
```

---

## 🔍 Casos de Uso Completos

### Caso 1: Cliente nuevo realiza su primera orden

```python
# 1. Crear cliente
cliente = {
    "nombre": "Pedro Sánchez",
    "email": "pedro.sanchez@email.com",
    "telefono": "3001112233",
    "direccion": "Calle 100 #50-25"
}
resp_cliente = requests.post(f"{BASE_URL}/clientes", json=cliente)
cliente_id = resp_cliente.json()["id"]

# 2. Consultar servicios disponibles
servicios = requests.get(f"{BASE_URL}/servicios").json()
print(f"Servicios disponibles: {len(servicios)}")

# 3. Crear orden con servicios seleccionados
orden = {
    "cliente_id": cliente_id,
    "servicios": [
        {"servicio_id": 1, "cantidad": 5, "descripcion": "5 camisas"},
        {"servicio_id": 2, "cantidad": 2, "descripcion": "2 pantalones"}
    ],
    "notas": "Primera orden del cliente"
}
resp_orden = requests.post(f"{BASE_URL}/ordenes", json=orden)
print(f"Orden creada: Total ${resp_orden.json()['total']}")
```

### Caso 2: Seguimiento de orden

```python
orden_id = 1

# 1. Orden recibida
requests.put(f"{BASE_URL}/ordenes/{orden_id}/estado", 
             json={"estado": "recibida"})

# 2. Orden en proceso (1 hora después)
requests.put(f"{BASE_URL}/ordenes/{orden_id}/estado", 
             json={"estado": "en_proceso"})

# 3. Orden lista (al día siguiente)
requests.put(f"{BASE_URL}/ordenes/{orden_id}/estado", 
             json={"estado": "lista"})

# 4. Orden entregada
requests.put(f"{BASE_URL}/ordenes/{orden_id}/estado", 
             json={"estado": "entregada"})
```

---

## 📊 Respuestas de Error

### Cliente no encontrado (404)

```json
{
  "detail": "Cliente con id 999 no encontrado"
}
```

### Email duplicado (400)

```json
{
  "detail": "Ya existe un cliente con este email"
}
```

### Datos inválidos (422)

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

**Ejemplos de uso para Lavandería Express QuickClean API**  
**ROJAS BURBANO - Ficha 3147246**
