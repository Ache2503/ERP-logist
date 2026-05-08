"""Rutas del módulo Conductores (Transportistas)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.conductores import ConductorCreate, ConductorUpdate, ConductorResponse, ConductorListResponse
from app.services.conductor_service import ConductorService

router = APIRouter(
    prefix="/conductores",
    tags=["Transportistas"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("/", response_model=ConductorListResponse)
def listar(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar conductores"""
    service = ConductorService(db)
    return service.listar(skip, limit)


@router.get("/{id_empleado}", response_model=ConductorResponse)
def obtener(id_empleado: int, db: Session = Depends(get_db)):
    """Obtener conductor por ID"""
    service = ConductorService(db)
    return service.obtener(id_empleado)


@router.post("/", response_model=ConductorResponse, status_code=status.HTTP_201_CREATED)
def crear(data: ConductorCreate, db: Session = Depends(get_db)):
    """Crear nuevo conductor"""
    service = ConductorService(db)
    return service.crear(data)


@router.put("/{id_empleado}", response_model=ConductorResponse)
def actualizar(id_empleado: int, data: ConductorUpdate, db: Session = Depends(get_db)):
    """Actualizar conductor"""
    service = ConductorService(db)
    return service.actualizar(id_empleado, data)


@router.delete("/{id_empleado}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_empleado: int, db: Session = Depends(get_db)):
    """Eliminar conductor"""
    service = ConductorService(db)
    service.eliminar(id_empleado)
    return None
