# tests/test_cache_domain.py
import pytest
# tests/test_cache_centro_estetico.py
from app.cache.redis_config import cache_manager

class TestDomainCache:
    
    
    def test_cache_basic_functionality(self):
        """Verifica funcionalidad básica del cache"""
        test_key = "test_entity_123"
        test_data = {"id": 123, "nombre": "Test Entity"}

        # Almacena en cache
        assert cache_manager.set_cache(test_key, test_data)

        # Recupera del cache
        cached_data = cache_manager.get_cache(test_key)
        assert cached_data == test_data

        # Limpia
        cache_manager.invalidate_cache(test_key)
        
        

    def test_domain_specific_caching(self):
        
        """Verifica caching específico de tu dominio"""
        # Personaliza este test según tu dominio
        # Ejemplo genérico:
        entity_data = {"specific_field": "domain_value"}
        cache_key = "spa_tratamientos_frecuentes"

        # Establece los datos en la caché con una clave que refleja el dominio
        cache_manager.set_cache(cache_key, entity_data, 'frequent_data')
        
        # Recupera los datos de la caché
        retrieved = cache_manager.get_cache(cache_key)

        # Verifica que los datos recuperados sean los mismos
        assert retrieved == entity_data

        # Limpia la caché
        cache_manager.invalidate_cache(cache_key)
