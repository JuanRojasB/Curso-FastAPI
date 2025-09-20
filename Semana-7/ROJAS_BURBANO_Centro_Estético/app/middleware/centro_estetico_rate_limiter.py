from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time
import json
from typing import Dict, Optional

class DomainRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str, redis_client: redis.Redis):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.redis = redis_client

        # Configuración específica por dominio
        self.rate_limits = self._get_domain_rate_limits(domain_prefix)

    def _get_domain_rate_limits(self, domain_prefix: str) -> Dict[str, Dict]:
        """Configuración de límites específicos por dominio"""

        rate_configs = {
            "vet_": {
                # Tipo A - límites altos para operaciones críticas
                "critical": {"requests": 200, "window": 60},      # 200 req/min críticas
                "routine": {"requests": 100, "window": 60},       # 100 req/min rutinarias
                "general": {"requests": 150, "window": 60},       # 150 req/min general
                "admin": {"requests": 50, "window": 60}           # 50 req/min admin
            },
            "edu_": {
                # Tipo B - límites medios para reservas
                "booking": {"requests": 80, "window": 60},        # 80 req/min reservas
                "schedule": {"requests": 200, "window": 60},      # 200 req/min horarios
                "general": {"requests": 120, "window": 60},       # 120 req/min general
                "admin": {"requests": 40, "window": 60}           # 40 req/min admin
            },
            "gym_": {
                # Tipo C - límites altos para accesos frecuentes
                "access": {"requests": 300, "window": 60},        # 300 req/min accesos
                "equipment": {"requests": 150, "window": 60},     # 150 req/min equipos
                "routine": {"requests": 100, "window": 60},       # 100 req/min rutinas
                "general": {"requests": 180, "window": 60},       # 180 req/min general
                "admin": {"requests": 60, "window": 60}           # 60 req/min admin
            },
            "pharma_": {
                # Tipo D - límites altos para inventario
                "inventory": {"requests": 400, "window": 60},     # 400 req/min inventario
                "sales": {"requests": 200, "window": 60},         # 200 req/min ventas
                "search": {"requests": 300, "window": 60},        # 300 req/min búsquedas
                "general": {"requests": 250, "window": 60},       # 250 req/min general
                "admin": {"requests": 80, "window": 60}           # 80 req/min admin
            }
        }

        # Configuración por defecto para otros dominios
        default_config = {
            "high_priority": {"requests": 200, "window": 60},
            "medium_priority": {"requests": 100, "window": 60},
            "low_priority": {"requests": 50, "window": 60},
            "general": {"requests": 120, "window": 60},
            "admin": {"requests": 30, "window": 60}
        }

        return rate_configs.get(domain_prefix, default_config)

    def _get_rate_limit_category(self, path: str, method: str) -> str:
        """Determina la categoría de rate limit según el endpoint"""

        # Patrones específicos por dominio
        if self.domain_prefix == "vet_":
            if "/emergency" in path or "/urgente" in path:
                return "emergency"
            elif "/consultation" in path or "/consulta" in path:
                return "consultation"
            elif "/admin" in path:
                return "admin"

        elif self.domain_prefix == "edu_":
            if "/booking" in path or "/reserva" in path:
                return "booking"
            elif "/schedule" in path or "/horario" in path:
                return "schedule"
            elif "/admin" in path:
                return "admin"

        elif self.domain_prefix == "gym_":
            if "/checkin" in path or "/entrada" in path:
                return "checkin"
            elif "/equipment" in path or "/equipo" in path:
                return "equipment"
            elif "/routine" in path or "/rutina" in path:
                return "routine"
            elif "/admin" in path:
                return "admin"

        elif self.domain_prefix == "pharma_":
            if "/inventory" in path or "/inventario" in path:
                return "inventory"
            elif "/sales" in path or "/venta" in path:
                return "sales"
            elif "/search" in path or "/buscar" in path:
                return "search"
            elif "/admin" in path:
                return "admin"

        return "general"

    async def dispatch(self, request: Request, call_next):
        # Obtener información del request
        client_ip = request.client.host
        path = request.url.path
        method = request.method

        # Solo aplicar rate limiting a endpoints de tu dominio
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        # Determinar categoría de rate limit
        category = self._get_rate_limit_category(path, method)
        rate_config = self.rate_limits.get(category, self.rate_limits["general"])

        # Verificar rate limit
        if not self._check_rate_limit(client_ip, category, rate_config):
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "category": category,
                    "limit": rate_config["requests"],
                    "window": rate_config["window"],
                    "domain": self.domain_prefix
                }
            )

        # Continuar con el request
        response = await call_next(request)
        return response

    def _check_rate_limit(self, client_ip: str, category: str, config: Dict) -> bool:
        """Verifica si el cliente excede el rate limit"""
        current_time = int(time.time())
        window_start = current_time - config["window"]

        # Clave específica para el dominio y categoría
        key = f"{self.domain_prefix}:rate_limit:{category}:{client_ip}"

        # Obtener requests en la ventana actual
        requests = self.redis.zrangebyscore(key, window_start, current_time)

        if len(requests) >= config["requests"]:
            return False

        # Añadir request actual
        self.redis.zadd(key, {str(current_time): current_time})
        self.redis.expire(key, config["window"])

        # Limpiar requests antiguos
        self.redis.zremrangebyscore(key, 0, window_start)

        return True