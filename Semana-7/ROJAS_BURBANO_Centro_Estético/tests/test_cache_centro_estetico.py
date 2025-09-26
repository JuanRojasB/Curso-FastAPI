# tests/test_cache_domain.py
import pytest
# tests/test_cache_centro_estetico.py
from app.cache.redis_config import cache_manager


class TestCentroEsteticoCache:
    def test_cache_tratamientos_frecuentes(self):
        """Verifica almacenamiento y recuperación de tratamientos frecuentes"""
        test_key = "tratamientos_frecuentes"
        test_data = [
            {"id": 1, "nombre": "Limpieza Facial"},
            {"id": 2, "nombre": "Depilación Láser"}
        ]
        assert cache_manager.set_cache(test_key, test_data, 'frequent_data')
        cached_data = cache_manager.get_cache(test_key)
        assert cached_data == test_data
        cache_manager.invalidate_cache(test_key)

    def test_cache_configuracion_centro(self):
        """Verifica almacenamiento y recuperación de configuración del centro estético"""
        config_key = "configuracion"
        config_data = {
            "horario": "09:00-19:00",
            "direccion": "Av. Belleza 123",
            "telefono": "555-1234"
        }
        assert cache_manager.set_cache(config_key, config_data, 'stable_data')
        cached_config = cache_manager.get_cache(config_key)
        assert cached_config == config_data
        cache_manager.invalidate_cache(config_key)

    def test_cache_catalogo_servicios_equipos(self):
        """Verifica almacenamiento y recuperación del catálogo de servicios y equipos"""
        catalog_key = "catalogo"
        catalog_data = {
            "servicios": ["Masaje Relajante", "Peeling Químico"],
            "equipos": ["Láser Diodo", "Radiofrecuencia"]
        }
        assert cache_manager.set_cache(catalog_key, catalog_data, 'reference_data')
        cached_catalog = cache_manager.get_cache(catalog_key)
        assert cached_catalog == catalog_data
        cache_manager.invalidate_cache(catalog_key)
