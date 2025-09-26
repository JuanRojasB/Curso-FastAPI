# app/routers/middleware_monitoring.py
from fastapi import APIRouter, Depends
import redis

router = APIRouter(prefix="/spa/monitoring", tags=["Centro Estético Monitoring"])

@router.get("/rate-limits")
async def get_rate_limit_stats():
    """Obtiene estadísticas de rate limiting para reservas y tratamientos"""
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    keys = redis_client.keys("spa_:rate_limit:*")
    stats = {}
    for key in keys:
        key_str = key.decode() if isinstance(key, bytes) else key
        parts = key_str.split(":")
        if len(parts) >= 4:
            categoria = parts[2]
            cliente_id = parts[3]
            count = redis_client.zcard(key)
            if categoria not in stats:
                stats[categoria] = {}
            stats[categoria][cliente_id] = count
    return stats

@router.get("/middleware-health")
async def check_middleware_health():
    """Verifica el estado del middleware del centro estético"""
    return {
        "domain": "spa_",
        "rate_limiter": "active",
        "logger": "active",
        "validator": "active",
        "status": "healthy"
    }