# main.py - Integración con tu API existente
from fastapi import FastAPI, Request, Response, status
from prometheus_fastapi_instrumentator import Instrumentator
from app.monitoring.metrics import APIMetrics, monitor_performance
from app.monitoring.profiler import APIProfiler
from app.monitoring.alerts import AlertManager, AlertRule, email_alert
import asyncio
import time

# Configuración según tu dominio asignado
DOMAIN_CONFIG = {
    "app_name": "centro_estetico_api",
    "domain": "spa_",
    "entity": "tratamiento"
}

app = FastAPI(title="API Centro Estético")

# Endpoints mínimos para los tests de middleware

# Simulación de rate limiting para test
rate_limit_counter = 0

@app.post("/spa/reservas")
async def crear_reserva(reserva: dict):
    global rate_limit_counter
    rate_limit_counter += 1
    # Simula rate limiting: responde 429 si se hacen más de 100 requests
    if rate_limit_counter > 100:
        return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    return {"msg": "Reserva creada"}


@app.post("/spa/accion-log")
async def accion_log(data: dict):
    import os
    os.makedirs("logs", exist_ok=True)
    with open("logs/spa_domain.log", "a") as f:
        f.write(f"Acción: {data.get('accion')} Empleado: {data.get('empleado_id')}\n")
    return {"msg": "Acción registrada"}

@app.get("/spa/cliente-protegido")
async def cliente_protegido(request: Request):
    # Simula validación de headers
    cliente_token = request.headers.get("X-Cliente-Token")
    empleado_token = request.headers.get("X-Empleado-Token")
    if not cliente_token or not empleado_token:
        return Response(status_code=400)
    return {"msg": "Acceso permitido"}

@app.get("/spa/horario-restringido")
async def horario_restringido():
    # Simula horario restringido: responde 403
    return Response(status_code=status.HTTP_403_FORBIDDEN)

# Inicializar sistemas de monitoring
metrics = APIMetrics(
    app_name=DOMAIN_CONFIG["app_name"],
    domain=DOMAIN_CONFIG["domain"]
)

profiler = APIProfiler(domain=DOMAIN_CONFIG["domain"])

alert_manager = AlertManager(domain=DOMAIN_CONFIG["domain"])

# Configurar Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Configurar alertas específicas del dominio
alert_manager.add_rule(AlertRule(
    name=f"{DOMAIN_CONFIG['domain']}_high_response_time",
    metric_name="response_time",
    threshold=2.0,  # 2 segundos
    comparison="gt",
    duration=60,    # 1 minuto
    action=email_alert
))

alert_manager.add_rule(AlertRule(
    name=f"{DOMAIN_CONFIG['domain']}_high_cpu",
    metric_name="cpu_usage",
    threshold=80.0,  # 80%
    comparison="gt",
    duration=120,    # 2 minutos
    action=email_alert
))

# Middleware para métricas automáticas
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    metrics.record_request(
        method=request.method,
        endpoint=str(request.url.path),
        status=response.status_code,
        duration=duration
    )

    return response


# Tarea en background para métricas del sistema
async def update_system_metrics():
    while True:
        metrics.update_system_metrics()
        await asyncio.sleep(30)  # Cada 30 segundos

# Lanzar la tarea en el evento de startup de FastAPI
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_system_metrics())

# Endpoint para métricas personalizadas
@app.get("/metrics-dashboard")
async def get_metrics_dashboard():
    """Endpoint para obtener métricas del dashboard"""
    return {
        "domain": DOMAIN_CONFIG["domain"],
        "entity": DOMAIN_CONFIG["entity"],
        "profiles": profiler.get_profile_report(),
        "system_status": "healthy"
    }

# Ejemplo de uso en endpoints existentes
@app.post("/tratamiento/")
@profiler.profile_function("create_tratamiento")
@monitor_performance(metrics)
async def create_tratamiento(tratamiento_data: dict):
    """Crear nuevo tratamiento con monitoring"""
    # Aquí iría la lógica real de creación de tratamiento
    metrics.record_business_event('tratamientos_creados')
    return {"message": "Tratamiento creado exitosamente"}