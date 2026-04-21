"""
Controllers — Marcas
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.marca_service import MarcaService
from app.schemas.marcas import (
    MarcaCreate, MarcaUpdate,
    MarcaResponse, MarcaListResponse,
)

router = APIRouter(prefix="/marcas", tags=["Marcas"])


@router.get("", response_model=MarcaListResponse, summary="Listar marcas")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return MarcaService(db).listar(skip, limit)


@router.post("", response_model=MarcaResponse,
             status_code=status.HTTP_201_CREATED, summary="Crear marca")
def crear(data: MarcaCreate, db: Session = Depends(get_db)):
    return MarcaService(db).crear(data)


@router.get("/{id_marca}", response_model=MarcaResponse, summary="Obtener marca")
def obtener(id_marca: int, db: Session = Depends(get_db)):
    return MarcaService(db).obtener(id_marca)


@router.put("/{id_marca}", response_model=MarcaResponse, summary="Actualizar marca")
def actualizar(id_marca: int, data: MarcaUpdate, db: Session = Depends(get_db)):
    return MarcaService(db).actualizar(id_marca, data)


@router.delete("/{id_marca}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar marca")
def eliminar(id_marca: int, db: Session = Depends(get_db)):
    MarcaService(db).eliminar(id_marca)