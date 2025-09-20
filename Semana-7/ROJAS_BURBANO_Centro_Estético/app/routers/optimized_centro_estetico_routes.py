# app/routers/optimized_domain_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services.optimized_domain_service import OptimizedDomainService
from ..database import get_db

router = APIRouter(prefix="/tu_prefijo/optimized", tags=["Optimized Domain"])

@router.get("/critical-data/{entity_id}")
async def get_critical_data_optimized(
    entity_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Endpoint optimizado para datos críticos de tu dominio"""
    service = OptimizedDomainService(db, "tu_prefijo")  # Reemplaza con tu prefijo
    return await service.get_critical_data(entity_id, limit=limit)

@router.get("/availability")
async def get_availability_optimized(
    dia: Optional[str] = None,
    hora: Optional[str] = None,
    capacidad_minima: int = 1,
    db: Session = Depends(get_db)
):
    """Endpoint optimizado para consultas de disponibilidad"""
    service = OptimizedDomainService(db, "tu_prefijo")
    filters = {"dia": dia, "hora": hora, "capacidad_minima": capacidad_minima}
    return await service.get_availability_data(**filters)

@router.get("/alerts")
async def get_domain_alerts(db: Session = Depends(get_db)):
    """Endpoint optimizado para alertas específicas del dominio"""
    service = OptimizedDomainService(db, "tu_prefijo")
    return await service.get_inventory_alerts()