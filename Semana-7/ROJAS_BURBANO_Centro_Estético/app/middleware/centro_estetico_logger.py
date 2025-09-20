# app/middleware/domain_logger.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
import time
from typing import Dict, Any

class DomainLogger(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str):
        super().__init__(app)
        self.domain_prefix = domain_prefix

        # Configurar logger específico para el dominio
        self.logger = logging.getLogger(f"{domain_prefix}domain_logger")
        self.logger.setLevel(logging.INFO)

        # Handler específico para archivos del dominio
        handler = logging.FileHandler(f"logs/{domain_prefix}domain.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Configurar qué endpoints loggear por dominio
        self.logged_endpoints = self._get_logged_endpoints(domain_prefix)

    def _get_logged_endpoints(self, domain_prefix: str) -> Dict[str, str]:
        """Define qué endpoints requieren logging específico por dominio"""

        logging_configs = {
            "vet_": {
                "/historial": "CRITICAL",  # Acceso a historiales médicos
                "/emergency": "CRITICAL",  # Emergencias veterinarias
                "/update": "WARNING",      # Modificaciones importantes
                "/delete": "CRITICAL",     # Eliminaciones críticas
            },
            "edu_": {
                "/booking": "INFO",        # Reservas de aulas
                "/schedule": "INFO",       # Cambios en horarios
                "/enrollment": "WARNING",  # Inscripciones/cancelaciones
                "/admin": "WARNING",       # Acciones administrativas
            },
            "gym_": {
                "/checkin": "INFO",        # Check-ins de miembros
                "/equipment": "INFO",      # Uso de equipos
                "/membership": "WARNING",  # Cambios en membresías
                "/access": "INFO",         # Acceso a instalaciones
            },
            "pharma_": {
                "/inventory": "INFO",      # Consultas de inventario
                "/sales": "WARNING",       # Ventas realizadas
                "/price": "INFO",          # Consultas de precios
                "/admin": "CRITICAL",      # Cambios administrativos
            }
        }

        return logging_configs.get(domain_prefix, {
            "/create": "INFO",
            "/update": "WARNING",
            "/delete": "CRITICAL",
            "/admin": "WARNING"
        })

    def _should_log_endpoint(self, path: str) -> tuple[bool, str]:
        """Determina si el endpoint debe ser loggeado y su nivel"""
        for endpoint_pattern, level in self.logged_endpoints.items():
            if endpoint_pattern in path:
                return True, level
        return False, "INFO"

    def _extract_domain_specific_data(self, request: Request, path: str) -> Dict[str, Any]:
        """Extrae datos específicos del dominio para logging"""
        data = {
            "domain": self.domain_prefix,
            "path": path,
            "method": request.method,
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent", "unknown")
        }

        # Datos específicos por dominio
        if self.domain_prefix == "vet_":
            # Para veterinaria, loggear IDs de mascotas y veterinarios
            if "mascota_id" in str(request.url):
                data["entity_type"] = "mascota"
            elif "veterinario_id" in str(request.url):
                data["entity_type"] = "veterinario"

        elif self.domain_prefix == "edu_":
            # Para academia, loggear IDs de estudiantes y aulas
            if "estudiante_id" in str(request.url):
                data["entity_type"] = "estudiante"
            elif "aula_id" in str(request.url):
                data["entity_type"] = "aula"

        elif self.domain_prefix == "gym_":
            # Para gimnasio, loggear IDs de usuarios y equipos
            if "usuario_id" in str(request.url):
                data["entity_type"] = "usuario"
            elif "equipo_id" in str(request.url):
                data["entity_type"] = "equipo"

        elif self.domain_prefix == "pharma_":
            # Para farmacia, loggear IDs de productos y ventas
            if "producto_id" in str(request.url):
                data["entity_type"] = "producto"
            elif "venta_id" in str(request.url):
                data["entity_type"] = "venta"

        return data

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path

        # Solo procesar endpoints del dominio
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        # Verificar si debe ser loggeado
        should_log, log_level = self._should_log_endpoint(path)

        if should_log:
            # Datos del request
            request_data = self._extract_domain_specific_data(request, path)

            # Loggear inicio del request
            self.logger.log(
                getattr(logging, log_level),
                f"REQUEST_START: {json.dumps(request_data)}"
            )

        # Procesar request
        response = await call_next(request)

        if should_log:
            # Calcular tiempo de respuesta
            process_time = time.time() - start_time

            # Datos de la respuesta
            response_data = {
                **request_data,
                "status_code": response.status_code,
                "process_time": round(process_time, 3)
            }

            # Determinar nivel según status code
            if response.status_code >= 500:
                response_level = "CRITICAL"
            elif response.status_code >= 400:
                response_level = "WARNING"
            else:
                response_level = log_level

            # Loggear respuesta
            self.logger.log(
                getattr(logging, response_level),
                f"REQUEST_END: {json.dumps(response_data)}"
            )

        return response