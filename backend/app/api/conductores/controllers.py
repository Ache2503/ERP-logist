"""Rutas del módulo Conductores (Transportistas)"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.conductores import ConductorCreate, ConductorUpdate, ConductorResponse, ConductorListResponse, ConductorEnvioListResponse
from app.services.conductor_service import ConductorService
from app.services.conductor_dashboard_service import ConductorDashboardService
from app.schemas.conductores_dashboard import (
    ConductorPerfilResponse, ConductorPerfilUpdate,
    ConductorStats, EnvioDetalleCompleto,
    IncidenteCreate, IncidenteResponse, IncidenteListResponse,
    ResenaResponse,
)

router = APIRouter(
    prefix="/conductores",
    tags=["Transportistas"],
    responses={404: {"description": "No encontrado"}},
)

# ── CRUD estándar ──────────────────────────────────────────

@router.get("", response_model=ConductorListResponse)
def listar(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    service = ConductorService(db)
    return service.listar(skip, limit)


@router.get("/{id_empleado}", response_model=ConductorResponse)
def obtener(id_empleado: int, db: Session = Depends(get_db)):
    service = ConductorService(db)
    return service.obtener(id_empleado)


@router.post("", response_model=ConductorResponse, status_code=status.HTTP_201_CREATED)
def crear(data: ConductorCreate, db: Session = Depends(get_db)):
    service = ConductorService(db)
    return service.crear(data)


@router.put("/{id_empleado}", response_model=ConductorResponse)
def actualizar(id_empleado: int, data: ConductorUpdate, db: Session = Depends(get_db)):
    service = ConductorService(db)
    return service.actualizar(id_empleado, data)


@router.delete("/{id_empleado}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_empleado: int, db: Session = Depends(get_db)):
    service = ConductorService(db)
    service.eliminar(id_empleado)

# ── Dashboard del Conductor ────────────────────────────────

@router.get("/{id_empleado}/envios", response_model=ConductorEnvioListResponse)
def listar_envios_conductor(id_empleado: int, db: Session = Depends(get_db)):
    service = ConductorService(db)
    return service.listar_envios_asignados(id_empleado)


@router.get("/{id_empleado}/dashboard/envios", summary="Envíos asignados con paginación")
def envios_asignados(
    id_empleado: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    svc = ConductorDashboardService(db)
    return svc.listar_envios_asignados(id_empleado, skip, limit)


@router.get("/{id_empleado}/dashboard/perfil", response_model=ConductorPerfilResponse,
            summary="Perfil del conductor")
def obtener_perfil(id_empleado: int, db: Session = Depends(get_db)):
    svc = ConductorDashboardService(db)
    return svc.obtener_perfil(id_empleado)


@router.put("/{id_empleado}/dashboard/perfil", response_model=ConductorPerfilResponse,
            summary="Actualizar perfil (sin cambiar rol)")
def actualizar_perfil(id_empleado: int, data: ConductorPerfilUpdate, db: Session = Depends(get_db)):
    svc = ConductorDashboardService(db)
    return svc.actualizar_perfil(id_empleado, data)


@router.get("/{id_empleado}/dashboard/estadisticas", response_model=ConductorStats,
            summary="Estadísticas del conductor")
def estadisticas(id_empleado: int, db: Session = Depends(get_db)):
    svc = ConductorDashboardService(db)
    return svc.estadisticas(id_empleado)


@router.get("/{id_empleado}/dashboard/envios/{id_envio}", response_model=EnvioDetalleCompleto,
            summary="Detalle completo de un envío asignado")
def detalle_envio(id_empleado: int, id_envio: int, db: Session = Depends(get_db)):
    svc = ConductorDashboardService(db)
    return svc.detalle_envio(id_empleado, id_envio)


@router.post("/{id_empleado}/dashboard/envios/{id_envio}/estatus",
             summary="Actualizar estatus del envío")
def actualizar_estatus(
    id_empleado: int, id_envio: int,
    estatus: str = Query(..., description="en_ruta, entregado, fallido, cancelado"),
    ubicacion: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    svc = ConductorDashboardService(db)
    return svc.actualizar_estatus_envio(id_empleado, id_envio, estatus, ubicacion)


# ── Incidentes ─────────────────────────────────────────────

@router.post("/{id_empleado}/dashboard/incidentes", response_model=IncidenteResponse,
             status_code=status.HTTP_201_CREATED, summary="Reportar incidente")
def crear_incidente(id_empleado: int, data: IncidenteCreate, db: Session = Depends(get_db)):
    svc = ConductorDashboardService(db)
    return svc.crear_incidente(id_empleado, data)


@router.get("/{id_empleado}/dashboard/incidentes", response_model=IncidenteListResponse,
            summary="Listar incidentes del conductor")
def listar_incidentes(
    id_empleado: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    svc = ConductorDashboardService(db)
    return svc.listar_incidentes(id_empleado, skip, limit)


# ── Reseñas ────────────────────────────────────────────────

@router.get("/{id_empleado}/dashboard/resenas", response_model=list[ResenaResponse],
            summary="Reseñas recibidas del conductor")
def listar_resenas(
    id_empleado: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    svc = ConductorDashboardService(db)
    return svc.listar_resenas(id_empleado, skip, limit)
