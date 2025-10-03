"""
Esquemas Pydantic - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246

Esquemas para servicios de lavandería (Tipo C)
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==================== ENUMS ====================

class TipoServicio(str, Enum):
    """Tipos de servicio disponibles en la lavandería"""
    LAVADO_SECO = "lavado_seco"
    LAVADO_AGUA = "lavado_agua"
    PLANCHADO = "planchado"
    TINTORERIA = "tintoreria"
    EXPRESS = "express"


class EstadoOrden(str, Enum):
    """Estados posibles de una orden de lavandería"""
    RECIBIDA = "recibida"
    EN_PROCESO = "en_proceso"
    LISTA = "lista"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"


class PrioridadOrden(str, Enum):
    """Niveles de prioridad para órdenes"""
    NORMAL = "normal"
    URGENTE = "urgente"
    EXPRESS = "express"


# ==================== SERVICIOS ====================

class ServicioBase(BaseModel):
    """Esquema base para servicios de lavandería"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Lavado en Seco Premium",
                "descripcion": "Servicio de lavado en seco para prendas delicadas",
                "tipo_servicio": "lavado_seco",
                "precio_base": 15000.0,
                "tiempo_estimado_horas": 24,
                "activo": True,
            }
        }
    )

    nombre: str = Field(
        ...,
        description="Nombre del servicio de lavandería",
        min_length=3,
        max_length=100,
        examples=["Lavado en Seco", "Planchado Express", "Tintorería Premium"],
    )

    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada del servicio",
        max_length=500,
        examples=["Servicio especializado en prendas delicadas"],
    )

    tipo_servicio: TipoServicio = Field(
        ...,
        description="Tipo de servicio de lavandería",
        examples=["lavado_seco", "planchado"],
    )

    precio_base: float = Field(
        ...,
        description="Precio base del servicio en COP",
        ge=0,
        le=1000000,
        examples=[15000.0, 8000.0, 25000.0],
    )

    tiempo_estimado_horas: int = Field(
        ...,
        description="Tiempo estimado de servicio en horas",
        ge=1,
        le=168,
        examples=[24, 48, 4],
    )

    activo: bool = Field(
        default=True, description="Indica si el servicio está disponible"
    )


class ServicioCreate(ServicioBase):
    """Esquema para crear un servicio"""
    pass


class ServicioUpdate(BaseModel):
    """Esquema para actualizar un servicio"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    tipo_servicio: Optional[TipoServicio] = None
    precio_base: Optional[float] = Field(None, ge=0, le=1000000)
    tiempo_estimado_horas: Optional[int] = Field(None, ge=1, le=168)
    activo: Optional[bool] = None


class ServicioResponse(ServicioBase):
    """Esquema de respuesta para servicios"""
    id: int = Field(..., description="ID único del servicio")
    fecha_creacion: datetime = Field(..., description="Fecha de creación")
    fecha_actualizacion: datetime = Field(..., description="Fecha de última actualización")

    model_config = ConfigDict(from_attributes=True)


# ==================== CLIENTES ====================

class ClienteBase(BaseModel):
    """Esquema base para clientes"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre_completo": "Juan Pérez García",
                "email": "juan.perez@email.com",
                "telefono": "3001234567",
                "direccion": "Calle 123 #45-67",
                "preferencias": {
                    "notificaciones_email": True,
                    "notificaciones_sms": False,
                },
            }
        }
    )

    nombre_completo: str = Field(
        ...,
        description="Nombre completo del cliente",
        min_length=3,
        max_length=150,
        examples=["Juan Pérez García", "María González López"],
    )

    email: str = Field(
        ...,
        description="Email del cliente",
        examples=["cliente@email.com"],
    )

    telefono: str = Field(
        ...,
        description="Teléfono de contacto",
        pattern=r"^3\d{9}$",
        examples=["3001234567", "3159876543"],
    )

    direccion: Optional[str] = Field(
        None,
        description="Dirección del cliente",
        max_length=300,
        examples=["Calle 123 #45-67, Bogotá"],
    )

    preferencias: Optional[dict] = Field(
        default_factory=dict,
        description="Preferencias del cliente",
    )


class ClienteCreate(ClienteBase):
    """Esquema para crear un cliente"""
    password: str = Field(
        ...,
        description="Contraseña del cliente",
        min_length=6,
        max_length=100,
    )


class ClienteUpdate(BaseModel):
    """Esquema para actualizar un cliente"""
    nombre_completo: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[str] = None
    telefono: Optional[str] = Field(None, pattern=r"^3\d{9}$")
    direccion: Optional[str] = Field(None, max_length=300)
    preferencias: Optional[dict] = None


class ClienteResponse(ClienteBase):
    """Esquema de respuesta para clientes"""
    id: int = Field(..., description="ID único del cliente")
    activo: bool = Field(..., description="Estado del cliente")
    fecha_registro: datetime = Field(..., description="Fecha de registro")

    model_config = ConfigDict(from_attributes=True)


# ==================== ÓRDENES ====================

class OrdenBase(BaseModel):
    """Esquema base para órdenes de lavandería"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cliente_id": 1,
                "servicio_id": 1,
                "cantidad_prendas": 5,
                "descripcion_prendas": "2 camisas, 2 pantalones, 1 chaqueta",
                "prioridad": "normal",
                "observaciones": "Cuidado especial con la chaqueta de cuero",
            }
        }
    )

    cliente_id: int = Field(
        ..., description="ID del cliente", gt=0, examples=[1, 5, 10]
    )

    servicio_id: int = Field(
        ..., description="ID del servicio solicitado", gt=0, examples=[1, 3, 7]
    )

    cantidad_prendas: int = Field(
        ...,
        description="Cantidad de prendas en la orden",
        ge=1,
        le=100,
        examples=[5, 10, 3],
    )

    descripcion_prendas: str = Field(
        ...,
        description="Descripción de las prendas",
        min_length=5,
        max_length=500,
        examples=["3 camisas blancas, 2 pantalones de vestir"],
    )

    prioridad: PrioridadOrden = Field(
        default=PrioridadOrden.NORMAL,
        description="Prioridad de la orden",
        examples=["normal", "urgente"],
    )

    observaciones: Optional[str] = Field(
        None,
        description="Observaciones adicionales",
        max_length=1000,
        examples=["Cuidado con manchas difíciles en camisa #2"],
    )


class OrdenCreate(OrdenBase):
    """Esquema para crear una orden"""
    pass


class OrdenUpdate(BaseModel):
    """Esquema para actualizar una orden"""
    cantidad_prendas: Optional[int] = Field(None, ge=1, le=100)
    descripcion_prendas: Optional[str] = Field(None, min_length=5, max_length=500)
    prioridad: Optional[PrioridadOrden] = None
    observaciones: Optional[str] = Field(None, max_length=1000)
    estado: Optional[EstadoOrden] = None


class OrdenResponse(OrdenBase):
    """Esquema de respuesta para órdenes"""
    id: int = Field(..., description="ID único de la orden")
    numero_orden: str = Field(..., description="Número de orden único")
    estado: EstadoOrden = Field(..., description="Estado actual de la orden")
    precio_total: float = Field(..., description="Precio total de la orden")
    fecha_recepcion: datetime = Field(..., description="Fecha de recepción")
    fecha_estimada_entrega: datetime = Field(..., description="Fecha estimada de entrega")
    fecha_entrega_real: Optional[datetime] = Field(None, description="Fecha real de entrega")

    model_config = ConfigDict(from_attributes=True)


# ==================== AUTENTICACIÓN ====================

class Token(BaseModel):
    """Esquema para token de autenticación"""
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")


class TokenData(BaseModel):
    """Datos contenidos en el token"""
    email: Optional[str] = None


class UserLogin(BaseModel):
    """Esquema para login de usuario"""
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")
