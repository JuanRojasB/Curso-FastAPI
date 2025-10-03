"""
Router de Servicios - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import ServicioCreate, ServicioUpdate, ServicioResponse

router = APIRouter()


@router.post(
    "/servicios",
    response_model=ServicioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo servicio",
    description="Crea un nuevo servicio de lavandería en el sistema",
)
async def crear_servicio(servicio: ServicioCreate):
    """
    Crear un nuevo servicio de lavandería
    
    - **nombre**: Nombre del servicio
    - **tipo_servicio**: Tipo de servicio (lavado_seco, planchado, etc.)
    - **precio_base**: Precio en COP
    - **tiempo_estimado_horas**: Tiempo de servicio en horas
    """
    # Implementación pendiente
    return {
        "id": 1,
        "nombre": servicio.nombre,
        "descripcion": servicio.descripcion,
        "tipo_servicio": servicio.tipo_servicio,
        "precio_base": servicio.precio_base,
        "tiempo_estimado_horas": servicio.tiempo_estimado_horas,
        "activo": servicio.activo,
        "fecha_creacion": "2024-01-01T00:00:00",
        "fecha_actualizacion": "2024-01-01T00:00:00",
    }


@router.get(
    "/servicios",
    response_model=List[ServicioResponse],
    summary="Listar servicios",
    description="Obtiene la lista de todos los servicios de lavandería",
)
async def listar_servicios(skip: int = 0, limit: int = 100, activo: bool = None):
    """
    Obtener lista de servicios
    
    - **skip**: Número de registros a omitir
    - **limit**: Número máximo de registros a retornar
    - **activo**: Filtrar por servicios activos/inactivos
    """
    return []


@router.get(
    "/servicios/{servicio_id}",
    response_model=ServicioResponse,
    summary="Obtener servicio",
    description="Obtiene un servicio específico por su ID",
)
async def obtener_servicio(servicio_id: int):
    """Obtener servicio por ID"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado"
    )


@router.put(
    "/servicios/{servicio_id}",
    response_model=ServicioResponse,
    summary="Actualizar servicio",
    description="Actualiza la información de un servicio existente",
)
async def actualizar_servicio(servicio_id: int, servicio: ServicioUpdate):
    """Actualizar servicio existente"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado"
    )


@router.delete(
    "/servicios/{servicio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar servicio",
    description="Elimina un servicio del sistema",
)
async def eliminar_servicio(servicio_id: int):
    """Eliminar servicio (soft delete)"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Servicio no encontrado"
    )
