"""
Service — Productos
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse

class ProductoService:

    def __init__(self, db: Session):
        self.repo = ProductoRepository(db)

    def listar_productos(self, skip: int = 0, limit: int = 100) -> List[ProductoResponse]:
        productos = self.repo.get_all(skip, limit)
        # Convertimos los objetos de SQLAlchemy a diccionarios validados por Pydantic
        return [ProductoResponse.model_validate(p) for p in productos]

    def obtener_producto(self, producto_id: int) -> ProductoResponse:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        return ProductoResponse.model_validate(producto)

    def crear_producto(self, data: ProductoCreate) -> ProductoResponse:
        # Regla de negocio: El código del producto debe ser único
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con el código '{data.codigo}'",
            )
        
        nuevo_producto = self.repo.create(data)
        return ProductoResponse.model_validate(nuevo_producto)

    def actualizar_producto(self, producto_id: int, data: ProductoUpdate) -> ProductoResponse:
        producto_actual = self.repo.get_by_id(producto_id)
        if not producto_actual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        
        # Validar unicidad si el usuario está intentando actualizar el código
        if data.codigo and data.codigo != producto_actual.codigo:
            if self.repo.get_by_codigo(data.codigo):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un producto con el código '{data.codigo}'",
                )
        
        producto_actualizado = self.repo.update(producto_actual, data)
        return ProductoResponse.model_validate(producto_actualizado)

    def eliminar_producto(self, producto_id: int) -> None:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado",
            )
        self.repo.delete(producto)