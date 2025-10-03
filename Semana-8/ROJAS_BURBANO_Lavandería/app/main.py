"""
Lavandería Express QuickClean - Aplicación FastAPI Principal
Ficha 3147246 - Semana 8 - ROJAS BURBANO

Sistema de gestión de servicios de lavandería con enfoque en:
- Servicios de usuario (Tipo C)
- Testing completo
- Documentación avanzada
- CI/CD básico
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Importar routers cuando estén disponibles
# from app.routers import servicios, ordenes, clientes

app = FastAPI(
    title="Lavandería Express QuickClean API",
    description="""
    ## API REST para gestión de servicios de lavandería
    
    Sistema completo de gestión que incluye:
    
    ### Características Principales
    
    * **Servicios de Lavandería**: Gestión completa de tipos de servicio
    * **Órdenes de Trabajo**: Control de órdenes y estados
    * **Clientes**: Administración de perfiles y preferencias
    * **Autenticación**: Sistema seguro de autenticación JWT
    * **Notificaciones**: Alertas y actualizaciones en tiempo real
    
    ### Tipo de Proyecto
    
    **Tipo C - Servicios de Usuario**: Enfocado en la gestión de servicios
    personalizados para clientes con seguimiento completo del ciclo de vida
    de las órdenes de lavandería.
    
    ### Estudiante
    
    **ROJAS BURBANO** - Ficha 3147246
    """,
    version="2.0.0",
    contact={
        "name": "ROJAS BURBANO",
        "email": "rojas.burbano@lavanderia.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "servicios",
            "description": "Operaciones de gestión de servicios de lavandería",
        },
        {
            "name": "ordenes",
            "description": "Gestión de órdenes de trabajo y seguimiento",
        },
        {
            "name": "clientes",
            "description": "Administración de clientes y perfiles",
        },
        {
            "name": "auth",
            "description": "Autenticación y autorización de usuarios",
        },
    ],
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "message": "Lavandería Express QuickClean API",
        "version": "2.0.0",
        "estudiante": "ROJAS BURBANO",
        "ficha": "3147246",
        "tipo": "Tipo C - Servicios Usuario",
        "semana": 8,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["root"])
async def health_check():
    """Health check endpoint para monitoreo"""
    return {"status": "healthy", "service": "lavanderia-quickclean"}


@app.get("/api/v1/info", tags=["root"])
async def api_info():
    """Información detallada de la API"""
    return {
        "api_name": "Lavandería Express QuickClean",
        "version": "2.0.0",
        "tipo_proyecto": "Tipo C - Servicios Usuario",
        "caracteristicas": [
            "Gestión de servicios de lavandería",
            "Control de órdenes de trabajo",
            "Administración de clientes",
            "Sistema de autenticación",
            "Testing completo con pytest",
            "Documentación avanzada OpenAPI",
            "CI/CD básico con GitHub Actions",
        ],
        "endpoints_principales": {
            "servicios": "/api/v1/servicios",
            "ordenes": "/api/v1/ordenes",
            "clientes": "/api/v1/clientes",
            "auth": "/api/v1/auth",
        },
    }


# Incluir routers cuando estén disponibles
# app.include_router(servicios.router, prefix="/api/v1", tags=["servicios"])
# app.include_router(ordenes.router, prefix="/api/v1", tags=["ordenes"])
# app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
