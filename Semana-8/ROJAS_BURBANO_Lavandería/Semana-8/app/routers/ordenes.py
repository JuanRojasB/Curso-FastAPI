"""
Router de Órdenes - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import OrdenCreate, OrdenUpdate, OrdenResponse, EstadoOrden

router = APIRouter()


@router.post(
    "/ordenes",
    response_model=OrdenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva orden",
    description="Crea una nueva orden de lavandería para un cliente",
)
async def crear_orden(orden: OrdenCreate):
    """
    Crear una nueva orden de lavandería
    
    - **cliente_id**: ID del cliente
    - **servicio_id**: ID del servicio solicitado
    - **cantidad_prendas**: Número de prendas
    - **descripcion_prendas**: Detalle de las prendas
    - **prioridad**: Normal, urgente o express
    """
    return {
        "id": 1,
        "numero_orden": "ORD-2024-001",
        "cliente_id": orden.cliente_id,
        "servicio_id": orden.servicio_id,
        "cantidad_prendas": orden.cantidad_prendas,
        "descripcion_prendas": orden.descripcion_prendas,
        "prioridad": orden.prioridad,
        "observaciones": orden.observaciones,
        "estado": "recibida",
        "precio_total": 50000.0,
        "fecha_recepcion": "2024-01-01T10:00:00",
        "fecha_estimada_entrega": "2024-01-03T10:00:00",
        "fecha_entrega_real": None,
    }


@router.get(
    "/ordenes",
    response_model=List[OrdenResponse],
    summary="Listar órdenes",
    description="Obtiene la lista de órdenes de lavandería",
)
async def listar_ordenes(
    skip: int = 0, limit: int = 100, estado: EstadoOrden = None, cliente_id: int = None
):
    """
    Obtener lista de órdenes
    
    - **skip**: Número de registros a omitir
    - **limit**: Número máximo de registros
    - **estado**: Filtrar por estado
    - **cliente_id**: Filtrar por cliente
    """
    return []


@router.get(
    "/ordenes/{orden_id}",
    response_model=OrdenResponse,
    summary="Obtener orden",
    description="Obtiene una orden específica por su ID",
)
async def obtener_orden(orden_id: int):
    """Obtener orden por ID"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
    )


@router.put(
    "/ordenes/{orden_id}",
    response_model=OrdenResponse,
    summary="Actualizar orden",
    description="Actualiza la información de una orden existente",
)
async def actualizar_orden(orden_id: int, orden: OrdenUpdate):
    """Actualizar orden existente"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
    )


@router.patch(
    "/ordenes/{orden_id}/estado",
    response_model=OrdenResponse,
    summary="Cambiar estado de orden",
    description="Actualiza el estado de una orden",
)
async def cambiar_estado_orden(orden_id: int, nuevo_estado: EstadoOrden):
    """Cambiar estado de una orden"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
    )
