# app/database/profiling.py
import time
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Configurar logging para consultas lentas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sql_performance")

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    if total > 0.1:  # Log consultas que toman más de 100ms
        logger.warning(f"Consulta lenta ({total:.3f}s): {statement[:100]}...")

# Función para analizar consultas específicas de tu dominio
def analyze_domain_queries(domain_prefix: str):
    """
    Analiza las consultas específicas de tu dominio
    Personaliza según tu contexto de negocio
    """
    slow_queries = []

    # Ejemplo de consultas a analizar (personaliza según tu dominio)
    test_queries = [
        "Búsquedas por entidad principal",
        "Consultas de relaciones complejas",
        "Agregaciones específicas del dominio",
        "Filtros frecuentes en tu industria"
    ]

    return slow_queries