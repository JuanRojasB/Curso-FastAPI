import pytest
import time
from sqlalchemy.orm import Session
from app.services.optimized_centro_estetico_service import OptimizedDomainService


class TestCentroEsteticoDBOptimization:
    @pytest.mark.asyncio
    async def test_consulta_critica_reservas(self, db_session: Session):
        """Verifica que la consulta crítica de reservas sea rápida"""
        from app.services.optimized_centro_estetico_service import OptimizedDomainService
        service = OptimizedDomainService(db_session, "spa_")
        start_time = time.time()
        result = await service.get_critical_data(entity_id=1)
        duration = time.time() - start_time
        assert duration < 0.2, f"Consulta crítica de reservas muy lenta: {duration:.3f}s"
        assert result is not None

    @pytest.mark.asyncio
    async def test_consulta_disponibilidad_tratamientos(self, db_session: Session):
        """Verifica performance de consulta de disponibilidad de tratamientos"""
        from app.services.optimized_centro_estetico_service import OptimizedDomainService
        service = OptimizedDomainService(db_session, "spa_")
        start_time = time.time()
        result = await service.get_availability_data()
        duration = time.time() - start_time
        assert duration < 0.3, f"Consulta de disponibilidad de tratamientos lenta: {duration:.3f}s"

    def test_indexes_exist(self, db_session: Session):
        """Verifica que existan índices en tablas relevantes del centro estético"""
        from sqlalchemy import text
        check_indexes = """
        SELECT indexname, tablename
        FROM pg_indexes
        WHERE indexname LIKE '%spa_%' 
        OR tablename IN ('tratamientos', 'reservas', 'clientes');
        """
        result = db_session.execute(text(check_indexes))
        indexes = [dict(row) for row in result]
        assert len(indexes) >= 2, "Faltan índices en tablas críticas del centro estético"