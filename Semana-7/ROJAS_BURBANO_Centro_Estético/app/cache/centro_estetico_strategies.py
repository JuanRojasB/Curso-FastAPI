# app/cache/domain_specific_caching.py
from .redis_config import cache_manager

class DomainSpecificCaching:

    @staticmethod
    async def cache_for_domain_type_a():
        """Estrategias para dominios tipo A (alta frecuencia de consultas)"""
        # Cache de tratamientos populares por usuario/cliente
        cache_manager.set_cache('spa_tratamientos:frecuentes', ['Tratamiento Facial Rejuvenecedor', 'Masaje Relax', 'Limpieza Facial'])
        # Cache de configuraciones estándar (horarios de atención, precios)
        cache_manager.set_cache('spa_configuracion:horarios', 'Lunes a Viernes, 9am - 6pm')
        cache_manager.set_cache('spa_configuracion:precio_base', 100)
        # Cache de información de referencia (tipos de piel, etc.)
        cache_manager.set_cache('spa_referencia:tipos_de_piel', ['Normal', 'Grasa', 'Mixta', 'Seca'])

    @staticmethod
    async def implement_domain_cache(domain_prefix: str):
        """
        Implementa caching específico según el dominio (Centro Estético)
        Personalizado para el contexto del negocio del centro estético.
        """
        if domain_prefix == "spa_tratamientos":
            await DomainSpecificCaching.cache_for_domain_type_a()  # Alta frecuencia de consultas (tratamientos populares, precios)
        else:
            raise ValueError(f"Tipo de dominio no reconocido: {domain_prefix}")
