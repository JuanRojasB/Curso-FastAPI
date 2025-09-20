from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import json
from typing import Dict, Any, Optional

class DomainValidator(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.validators = self._get_domain_validators(domain_prefix)

    def _get_domain_validators(self, domain_prefix: str) -> Dict[str, Any]:
        """Validadores específicos por dominio"""

        validators = {
            "vet_": {
                "required_headers": ["X-Vet-License"],  # Licencia veterinaria
                "business_hours": (8, 20),              # 8 AM a 8 PM
                "emergency_always": True                # Emergencias 24/7
            },
            "edu_": {
                "required_headers": ["X-Institution-ID"], # ID institución
                "business_hours": (6, 22),               # 6 AM a 10 PM
                "weekend_restricted": ["booking"]        # Restricciones fin de semana
            },
            "gym_": {
                "required_headers": ["X-Gym-Membership"], # Membresía del gimnasio
                "business_hours": (5, 23),               # 5 AM a 11 PM
                "capacity_limits": True                   # Límites de capacidad
            },
            "pharma_": {
                "required_headers": ["X-Pharmacy-License"], # Licencia farmacia
                "business_hours": (7, 21),                 # 7 AM a 9 PM
                "prescription_required": ["controlled"]     # Medicamentos controlados
            }
        }

        return validators.get(domain_prefix, {
            "required_headers": [],
            "business_hours": (0, 24),
            "special_validations": []
        })

    def _validate_business_hours(self, path: str) -> bool:
        """Valida horarios de atención según el dominio"""
        from datetime import datetime

        current_hour = datetime.now().hour
        start_hour, end_hour = self.validators.get("business_hours", (0, 24))

        # Excepciones por dominio
        if self.domain_prefix == "vet_" and "/emergency" in path:
            return True  # Emergencias veterinarias 24/7

        if self.domain_prefix == "pharma_" and "/emergency" in path:
            return True  # Farmacia de emergencias

        return start_hour <= current_hour <= end_hour

    def _validate_required_headers(self, request: Request) -> bool:
        """Valida headers requeridos por dominio"""
        required = self.validators.get("required_headers", [])

        for header in required:
            if header not in request.headers:
                return False

        return True

    def _validate_domain_specific_rules(self, request: Request, path: str) -> tuple[bool, Optional[str]]:
        """Validaciones específicas del dominio"""

        if self.domain_prefix == "edu_":
            # Academia: restricciones de fin de semana para reservas
            weekend_restricted = self.validators.get("weekend_restricted", [])
            if any(restriction in path for restriction in weekend_restricted):
                from datetime import datetime
                if datetime.now().weekday() >= 5:  # Sábado o Domingo
                    return False, "Reservas no disponibles en fin de semana"

        elif self.domain_prefix == "gym_":
            # Gimnasio: verificar límites de capacidad
            if "/checkin" in path and self.validators.get("capacity_limits"):
                # Aquí implementarías la lógica de verificación de capacidad
                # Por simplicidad, siempre retornamos True
                pass

        elif self.domain_prefix == "pharma_":
            # Farmacia: medicamentos controlados requieren prescripción
            if any(controlled in path for controlled in self.validators.get("prescription_required", [])):
                if "X-Prescription-ID" not in request.headers:
                    return False, "Medicamento controlado requiere prescripción"

        return True, None

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Solo validar endpoints del dominio
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        # Validar horarios de atención
        if not self._validate_business_hours(path):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Fuera de horario de atención",
                    "domain": self.domain_prefix,
                    "business_hours": self.validators["business_hours"]
                }
            )

        # Validar headers requeridos
        if not self._validate_required_headers(request):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Headers requeridos faltantes",
                    "required_headers": self.validators["required_headers"]
                }
            )

        # Validaciones específicas del dominio
        is_valid, error_message = self._validate_domain_specific_rules(request, path)
        if not is_valid:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": error_message,
                    "domain": self.domain_prefix
                }
            )

        return await call_next(request)