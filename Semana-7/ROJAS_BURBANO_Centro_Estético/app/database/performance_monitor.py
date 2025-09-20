import time
from sqlalchemy import text
from contextlib import contextmanager

class DatabasePerformanceMonitor:

    @staticmethod
    @contextmanager
    def measure_query_time(query_name: str):
        """Context manager para medir tiempo de consultas"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            print(f"Query '{query_name}' ejecutada en {duration:.3f}s")

            # Log si es lenta (personaliza el threshold según tu dominio)
            if duration > 0.5:  # 500ms
                print(f"⚠️  Consulta lenta detectada: {query_name}")

    @staticmethod
    def get_database_stats(db: Session):
        """Obtiene estadísticas generales de la base de datos"""
        stats_query = """
        SELECT
            schemaname,
            tablename,
            attname,
            n_distinct,
            correlation
        FROM pg_stats
        WHERE schemaname = 'public'
        ORDER BY tablename, attname;
        """

        result = db.execute(text(stats_query))
        return [dict(row) for row in result]

    @staticmethod
    def analyze_slow_queries(db: Session, domain_prefix: str):
        """Analiza consultas lentas específicas del dominio"""
        # Consulta para obtener consultas lentas (requiere pg_stat_statements)
        slow_queries = """
        SELECT query, calls, total_time, mean_time
        FROM pg_stat_statements
        WHERE query LIKE '%tu_tabla_principal%'  -- Personaliza según tu dominio
        ORDER BY mean_time DESC
        LIMIT 10;
        """

        try:
            result = db.execute(text(slow_queries))
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error analizando consultas lentas: {e}")
            return []