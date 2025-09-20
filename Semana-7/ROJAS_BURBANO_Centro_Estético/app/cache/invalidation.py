# app/cache/invalidation.py
from .redis_config import cache_manager

class DomainCacheInvalidation:

    @staticmethod
    async def on_entity_update(entity_id: str, entity_type: str):
        """Invalida cache cuando se actualiza una entidad de tu dominio"""
        # Invalida caches relacionados con esta entidad específica
        patterns = [
            f"*{entity_type}*{entity_id}*",  # Invalida caché para esta entidad
            f"*frequent_queries*",  # Si afecta consultas frecuentes
        ]

        for pattern in patterns:
            cache_manager.invalidate_cache(pattern)
            print(f"Cache invalidada para el patrón: {pattern}")

    @staticmethod
    async def on_configuration_change():
        """Invalida cache de configuración de tu dominio"""
        cache_manager.invalidate_cache("*config*")
        print("Cache de configuración invalidada")

    @staticmethod
    async def on_catalog_update():
        """Invalida cache de catálogo de tu dominio"""
        cache_manager.invalidate_cache("*catalog*")
        print("Cache de catálogo invalidada")


# Ejemplo de uso en un endpoint de actualización (actualización de una entidad en el centro estético)
from fastapi import APIRouter, HTTPException
from ..services import tu_servicio_dominio  # Importa el servicio correspondiente
from .invalidation import DomainCacheInvalidation

router = APIRouter(prefix="/spa", tags=["Centro Estético: Servicios y Equipos"])

# Endpoint para actualizar los tratamientos
@router.put("/tratamientos/{entity_id}")
async def update_tratamiento(entity_id: str, data: dict):
    """
    Actualiza un tratamiento en el centro estético.
    Después de actualizar, invalida las cachés relevantes.
    """
    try:
        # Actualiza el tratamiento
        resultado = await tu_servicio_dominio.update_tratamiento(entity_id, data)
        
        # Invalida las cachés relacionadas con este tratamiento
        await DomainCacheInvalidation.on_entity_update(entity_id, "tratamiento")
        
        return {"msg": "Tratamiento actualizado con éxito", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar tratamiento: {str(e)}")

# Endpoint para actualizar la configuración (ejemplo de cambio de horarios o precios)
@router.put("/configuracion")
async def update_configuracion(data: dict):
    """
    Actualiza la configuración del centro estético (horarios, precios, etc.).
    Invalida la caché de configuración después de la actualización.
    """
    try:
        # Actualiza la configuración
        resultado = await tu_servicio_dominio.update_configuracion(data)
        
        # Invalida las cachés relacionadas con la configuración
        await DomainCacheInvalidation.on_configuration_change()
        
        return {"msg": "Configuración actualizada con éxito", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar configuración: {str(e)}")

# Endpoint para actualizar el catálogo de tratamientos y equipos
@router.put("/catalogo")
async def update_catalogo(data: dict):
    """
    Actualiza el catálogo de tratamientos y equipos.
    Invalida la caché del catálogo después de la actualización.
    """
    try:
        # Actualiza el catálogo
        resultado = await tu_servicio_dominio.update_catalogo(data)
        
        # Invalida las cachés relacionadas con el catálogo
        await DomainCacheInvalidation.on_catalog_update()
        
        return {"msg": "Catálogo actualizado con éxito", "data": resultado}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar catálogo: {str(e)}")
