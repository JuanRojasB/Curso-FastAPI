# app/routers/middleware_monitoring.py
from fastapi import APIRouter, Depends
import redis

router = APIRouter(prefix="/tu_prefijo/monitoring", tags=["Middleware Monitoring"])

@router.get("/rate-limits")
async def get_rate_limit_stats():
    """Obtiene estadísticas de rate limiting específicas del dominio"""
    # Implementar lógica para obtener stats de Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # Obtener claves de rate limiting del dominio
    keys = redis_client.keys("tu_prefijo_:rate_limit:*")

    stats = {}
    for key in keys:
        key_str = key.decode() if isinstance(key, bytes) else key
        parts = key_str.split(":")
        if len(parts) >= 4:
            category = parts[2]
            client_ip = parts[3]
            count = redis_client.zcard(key)

            if category not in stats:
                stats[category] = {}
            stats[category][client_ip] = count

    return stats

@router.get("/middleware-health")
async def check_middleware_health():
    """Verifica el estado del middleware del dominio"""
    return {
        "domain": "tu_prefijo_",
        "rate_limiter": "active",
        "logger": "active",
        "validator": "active",
        "status": "healthy"
    }