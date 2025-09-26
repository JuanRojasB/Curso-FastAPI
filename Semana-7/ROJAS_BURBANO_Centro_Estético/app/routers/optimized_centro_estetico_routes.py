# app/routers/optimized_domain_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..services.optimized_domain_service import OptimizedDomainService
from ..database import get_db

router = APIRouter(prefix="/spa/optimized", tags=["Centro Estético Optimizado"])

@router.get("/tratamiento-critico/{tratamiento_id}")
async def get_critical_tratamiento_optimized(
    tratamiento_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Endpoint optimizado para datos críticos de tratamientos"""
    service = OptimizedDomainService(db, "spa_")
    return await service.get_critical_data(tratamiento_id, limit=limit)

@router.get("/disponibilidad")
async def get_disponibilidad_optimized(
    dia: Optional[str] = None,
    hora: Optional[str] = None,
    capacidad_minima: int = 1,
    db: Session = Depends(get_db)
):
    """Endpoint optimizado para consultas de disponibilidad de equipos y salas"""
    service = OptimizedDomainService(db, "spa_")
    filters = {"dia": dia, "hora": hora, "capacidad_minima": capacidad_minima}
    return await service.get_availability_data(**filters)

@router.get("/alertas-inventario")
async def get_alertas_inventario(db: Session = Depends(get_db)):
    """Endpoint optimizado para alertas de inventario de productos/equipos"""
    service = OptimizedDomainService(db, "spa_")
    return await service.get_inventory_alerts()