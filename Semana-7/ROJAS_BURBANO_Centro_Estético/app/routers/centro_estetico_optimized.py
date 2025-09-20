# app/routers/centro_estetico.py
from fastapi import APIRouter, HTTPException
from ..cache.cache_decorators import cache_result
from ..cache.redis_config import cache_manager
from ..services import tu_servicio_dominio  # Asegúrate de que el servicio esté importado correctamente

# Definimos el router para el Centro Estético
router = APIRouter(prefix="/spa", tags=["Centro Estético: Servicios y Equipos"])

# Endpoint para obtener los tratamientos más frecuentes
@router.get("/tratamientos/frecuentes")
@cache_result(ttl_type='frequent_data', key_prefix='spa_tratamientos_frecuentes')
async def get_tratamientos_frecuentes():
    """
    Obtiene los tratamientos más consultados o más populares del centro estético.
    """
    try:
        # Lógica para obtener los tratamientos más populares
        tratamientos_frecuentes = await tu_servicio_dominio.get_tratamientos_populares()
        return tratamientos_frecuentes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tratamientos frecuentes: {str(e)}")

# Endpoint para obtener la configuración del centro estético
@router.get("/configuracion")
@cache_result(ttl_type='stable_data', key_prefix='spa_config')
async def get_configuracion_dominio():
    """
    Obtiene la configuración específica del centro estético (horarios, precios, etc.).
    Datos que cambian raramente.
    """
    try:
        # Lógica para obtener la configuración del centro estético
        configuracion = await tu_servicio_dominio.get_configuracion_estetica()
        return configuracion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener configuración: {str(e)}")

# Endpoint para obtener el catálogo de tratamientos y equipos
@router.get("/catalogo")
@cache_result(ttl_type='reference_data', key_prefix='spa_catalogo_tratamientos')
async def get_catalogo_tratamientos():
    """
    Obtiene el catálogo de tratamientos y equipos utilizados en el centro estético.
    Ejemplo: Tipos de tratamientos faciales, productos cosméticos, equipos de estética, etc.
    """
    try:
        # Lógica para obtener el catálogo de tratamientos y equipos
        catalogo_tratamientos = await tu_servicio_dominio.get_catalogo_tratamientos_y_equipos()
        return catalogo_tratamientos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener catálogo de tratamientos: {str(e)}")
