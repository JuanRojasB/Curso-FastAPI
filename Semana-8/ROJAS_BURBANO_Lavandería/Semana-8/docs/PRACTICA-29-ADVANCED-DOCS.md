# Práctica 29: Documentación Avanzada de API - Lavandería Express QuickClean

## 🎯 Objetivos de la Práctica

- Generar documentación interactiva con OpenAPI/Swagger
- Personalizar Swagger UI para el dominio
- Documentar modelos Pydantic
- Incluir ejemplos y descripciones detalladas

## 📋 Documentación de API

### OpenAPI/Swagger UI

**URL:** `http://localhost:8000/docs`

La API de Lavandería Express QuickClean proporciona documentación interactiva automática generada con FastAPI y OpenAPI 3.0.

### Metadata de la API

```python
# main.py
app = FastAPI(
    title="Lavandería Express QuickClean API",
    description="""
    ## 🧺 Sistema de Gestión de Lavandería
    
    API REST para gestión completa de servicios de lavandería.
    
    ### Funcionalidades principales:
    
    * **Clientes** - Gestión de clientes y perfiles
    * **Servicios** - Catálogo de servicios (lavado, planchado, tintorería)
    * **Órdenes** - Gestión de pedidos y seguimiento
    
    ### Tipos de Servicios:
    
    - 🧼 Lavado Express (24h)
    - 👔 Planchado Premium
    - 🎨 Tintorería Especializada
    - 🧥 Limpieza en Seco
    """,
    version="1.0.0",
    contact={
        "name": "ROJAS BURBANO",
        "email": "soporte@quickclean.com",
    },
    license_info={
        "name": "MIT License",
    }
)
```

## 📊 Schemas Documentados

### Cliente Schema

```python
class ClienteBase(BaseModel):
    """Schema base para datos de cliente"""
    nombre: str = Field(..., description="Nombre completo del cliente", example="Juan Pérez")
    email: EmailStr = Field(..., description="Email único del cliente", example="juan@example.com")
    telefono: str = Field(..., description="Número de teléfono", example="3001234567")
    direccion: str = Field(..., description="Dirección de domicilio", example="Calle 123 #45-67")
    
    class Config:
        schema_extra = {
            "example": {
                "nombre": "María García",
                "email": "maria@example.com",
                "telefono": "3009876543",
                "direccion": "Carrera 50 #25-30"
            }
        }
```

### Servicio Schema

```python
class ServicioBase(BaseModel):
    """Schema base para servicios de lavandería"""
    nombre: str = Field(..., description="Nombre del servicio", example="Lavado Express")
    descripcion: str = Field(..., description="Descripción detallada", example="Lavado completo en 24 horas")
    precio: float = Field(..., gt=0, description="Precio en pesos colombianos", example=15000.0)
    tipo: str = Field(..., description="Tipo de servicio", example="lavado")
    tiempo_estimado: int = Field(..., description="Tiempo en horas", example=24)
    activo: bool = Field(default=True, description="Servicio activo/inactivo")
    
    class Config:
        schema_extra = {
            "example": {
                "nombre": "Planchado Premium",
                "descripcion": "Planchado profesional con vapor",
                "precio": 12000.0,
                "tipo": "planchado",
                "tiempo_estimado": 12,
                "activo": True
            }
        }
```

### Orden Schema

```python
class OrdenCreate(BaseModel):
    """Schema para crear nueva orden de lavandería"""
    cliente_id: int = Field(..., description="ID del cliente")
    servicios: List[ItemOrden] = Field(..., description="Lista de servicios solicitados")
    fecha_entrega: Optional[datetime] = Field(None, description="Fecha deseada de entrega")
    notas: Optional[str] = Field(None, description="Notas especiales")
    
    class Config:
        schema_extra = {
            "example": {
                "cliente_id": 1,
                "servicios": [
                    {
                        "servicio_id": 1,
                        "cantidad": 3,
                        "descripcion": "3 camisas blancas"
                    },
                    {
                        "servicio_id": 2,
                        "cantidad": 1,
                        "descripcion": "1 traje completo"
                    }
                ],
                "fecha_entrega": "2025-10-05T15:00:00",
                "notas": "Cliente preferencial - entrega urgente"
            }
        }
```

## 🎨 Tags y Organización

```python
tags_metadata = [
    {
        "name": "clientes",
        "description": "Operaciones con clientes de la lavandería. Gestión de perfiles, contactos y direcciones.",
    },
    {
        "name": "servicios",
        "description": "Catálogo de servicios disponibles. Incluye lavado, planchado, tintorería y limpieza en seco.",
    },
    {
        "name": "ordenes",
        "description": "Gestión de órdenes de servicio. Creación, seguimiento y actualización de estados.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)
```

## 📝 Documentación de Endpoints

### Ejemplo: Crear Cliente

```python
@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo cliente",
    description="""
    Registra un nuevo cliente en el sistema de lavandería.
    
    **Validaciones:**
    - Email debe ser único en el sistema
    - Teléfono debe tener formato válido colombiano
    - Nombre debe tener al menos 3 caracteres
    
    **Respuesta exitosa:** Retorna el cliente creado con su ID asignado
    """,
    responses={
        201: {
            "description": "Cliente creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "nombre": "Juan Pérez",
                        "email": "juan@example.com",
                        "telefono": "3001234567",
                        "direccion": "Calle 123 #45-67",
                        "fecha_registro": "2025-10-02T10:30:00"
                    }
                }
            }
        },
        400: {
            "description": "Email duplicado o datos inválidos"
        },
        422: {
            "description": "Error de validación de datos"
        }
    }
)
async def crear_cliente(cliente: ClienteCreate):
    """Endpoint para crear cliente con documentación completa"""
    # Implementación
    pass
```

### Ejemplo: Crear Orden

```python
@router.post(
    "/",
    response_model=OrdenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva orden de servicio",
    description="""
    Crea una nueva orden de servicio de lavandería.
    
    **Proceso:**
    1. Valida existencia del cliente
    2. Valida servicios solicitados
    3. Calcula total automáticamente
    4. Asigna estado inicial "recibida"
    5. Calcula fecha estimada de entrega
    
    **Estados posibles:**
    - `recibida`: Orden recién creada
    - `en_proceso`: En lavandería
    - `lista`: Lista para entrega
    - `entregada`: Entregada al cliente
    - `cancelada`: Orden cancelada
    """,
    responses={
        201: {
            "description": "Orden creada exitosamente",
        },
        404: {
            "description": "Cliente o servicio no encontrado"
        }
    }
)
async def crear_orden(orden: OrdenCreate):
    """Endpoint para crear orden con cálculo automático de total"""
    # Implementación
    pass
```

## 🔧 Personalización Swagger UI

```python
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": 1,
            "defaultModelExpandDepth": 3,
            "displayRequestDuration": True,
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True
        }
    )
```

## 📊 Acceder a la Documentación

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Acceder a documentación
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
# OpenAPI JSON: http://localhost:8000/openapi.json
```

## ✅ Criterios de Éxito

- [ ] Metadata de API configurada
- [ ] Todos los schemas documentados
- [ ] Ejemplos incluidos en schemas
- [ ] Tags organizados correctamente
- [ ] Endpoints con descripciones detalladas
- [ ] Respuestas documentadas (200, 400, 404, etc.)
- [ ] Swagger UI personalizado
- [ ] ReDoc accesible

## 🎓 Entregables

1. Documentación interactiva funcional
2. Schemas con ejemplos completos
3. Endpoints con descripciones detalladas
4. Screenshots de Swagger UI
5. Archivo OpenAPI JSON exportado

---

**Práctica 29 - ROJAS BURBANO - Lavandería Express QuickClean**
