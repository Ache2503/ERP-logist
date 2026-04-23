"""
Service — Tipos de Almacén
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.tipo_almacen_repository import TipoAlmacenRepository
from app.schemas.tipos_almacen import (
    TipoAlmacenCreate, TipoAlmacenUpdate,
    TipoAlmacenResponse, TipoAlmacenListResponse,
)


class TipoAlmacenService:

    def __init__(self, db: Session):
        self.repo = TipoAlmacenRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> TipoAlmacenListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return TipoAlmacenListResponse(
            total=total, skip=skip, limit=limit,
            data=[TipoAlmacenResponse.model_validate(t) for t in data],
        )

    def obtener(self, id_tipo_almacen: int) -> TipoAlmacenResponse:
        t = self.repo.get_by_id(id_tipo_almacen)
        if not t:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de almacén {id_tipo_almacen} no encontrado",
            )
        return TipoAlmacenResponse.model_validate(t)

    def crear(self, data: TipoAlmacenCreate) -> TipoAlmacenResponse:
        if self.repo.get_by_nombre(data.nombre_tipo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un tipo de almacén con nombre '{data.nombre_tipo}'",
            )
        return TipoAlmacenResponse.model_validate(self.repo.create(data))

    def actualizar(self, id_tipo_almacen: int,
                   data: TipoAlmacenUpdate) -> TipoAlmacenResponse:
        t = self.repo.get_by_id(id_tipo_almacen)
        if not t:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de almacén {id_tipo_almacen} no encontrado",
            )
        if data.nombre_tipo and data.nombre_tipo != t.nombre_tipo:
            if self.repo.get_by_nombre(data.nombre_tipo):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un tipo de almacén con nombre '{data.nombre_tipo}'",
                )
        return TipoAlmacenResponse.model_validate(self.repo.update(t, data))

    def eliminar(self, id_tipo_almacen: int) -> None:
        t = self.repo.get_by_id(id_tipo_almacen)
        if not t:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo de almacén {id_tipo_almacen} no encontrado",
            )
        self.repo.delete(t)