# app/routers/centro_estetico.py
from fastapi import APIRouter, HTTPException
from ..cache.cache_decorators import cache_result
from ..cache.redis_config import cache_manager
from ..cache.metrics import CacheMetrics
from ..services import tu_servicio_dominio

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
        
        # Registra el cache hit o miss
        CacheMetrics.track_cache_hit("spa_tratamientos_frecuentes")  # Si la caché existe
        return tratamientos_frecuentes
    except Exception as e:
        # Registra el cache miss si hay un error o no se encuentra en caché
        CacheMetrics.track_cache_miss("spa_tratamientos_frecuentes")
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
        
        # Registra el cache hit o miss
        CacheMetrics.track_cache_hit("spa_config")  # Si la caché existe
        return configuracion
    except Exception as e:
        # Registra el cache miss si hay un error o no se encuentra en caché
        CacheMetrics.track_cache_miss("spa_config")
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
        
        # Registra el cache hit o miss
        CacheMetrics.track_cache_hit("spa_catalogo_tratamientos")  # Si la caché existe
        return catalogo_tratamientos
    except Exception as e:
        # Registra el cache miss si hay un error o no se encuentra en caché
        CacheMetrics.track_cache_miss("spa_catalogo_tratamientos")
        raise HTTPException(status_code=500, detail=f"Error al obtener catálogo de tratamientos: {str(e)}")
