"""
Router de Clientes - Lavandería Express QuickClean
ROJAS BURBANO - Ficha 3147246
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter()


@router.post(
    "/clientes",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo cliente",
    description="Registra un nuevo cliente en el sistema de lavandería",
)
async def registrar_cliente(cliente: ClienteCreate):
    """
    Registrar un nuevo cliente
    
    - **nombre_completo**: Nombre completo del cliente
    - **email**: Email de contacto
    - **telefono**: Número de teléfono
    - **direccion**: Dirección de domicilio
    - **password**: Contraseña para acceso al sistema
    """
    return {
        "id": 1,
        "nombre_completo": cliente.nombre_completo,
        "email": cliente.email,
        "telefono": cliente.telefono,
        "direccion": cliente.direccion,
        "preferencias": cliente.preferencias,
        "activo": True,
        "fecha_registro": "2024-01-01T00:00:00",
    }


@router.get(
    "/clientes",
    response_model=List[ClienteResponse],
    summary="Listar clientes",
    description="Obtiene la lista de clientes registrados",
)
async def listar_clientes(skip: int = 0, limit: int = 100, activo: bool = None):
    """
    Obtener lista de clientes
    
    - **skip**: Número de registros a omitir
    - **limit**: Número máximo de registros
    - **activo**: Filtrar por clientes activos/inactivos
    """
    return []


@router.get(
    "/clientes/{cliente_id}",
    response_model=ClienteResponse,
    summary="Obtener cliente",
    description="Obtiene un cliente específico por su ID",
)
async def obtener_cliente(cliente_id: int):
    """Obtener cliente por ID"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
    )


@router.put(
    "/clientes/{cliente_id}",
    response_model=ClienteResponse,
    summary="Actualizar cliente",
    description="Actualiza la información de un cliente existente",
)
async def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    """Actualizar cliente existente"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
    )


@router.delete(
    "/clientes/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desactivar cliente",
    description="Desactiva un cliente del sistema (soft delete)",
)
async def desactivar_cliente(cliente_id: int):
    """Desactivar cliente (soft delete)"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
    )
