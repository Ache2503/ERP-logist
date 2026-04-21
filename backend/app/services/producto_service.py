from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse

class ProductoService:
    def __init__(self, db: Session):
        self.repo = ProductoRepository(db)

    def crear_producto(self, producto_data: ProductoCreate) -> ProductoResponse:
        # Validar que el código no exista
        existente = self.repo.get_by_codigo(producto_data.codigo)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un producto con ese código"
            )
        # Aquí podrías validar que la categoría, marca y unidad de medida existan
        producto = self.repo.create(producto_data)
        return ProductoResponse.model_validate(producto)

    def obtener_producto(self, producto_id: int) -> ProductoResponse:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return ProductoResponse.model_validate(producto)

    def listar_productos(self, skip: int = 0, limit: int = 100) -> List[ProductoResponse]:
        productos = self.repo.get_all(skip=skip, limit=limit)
        return [ProductoResponse.model_validate(p) for p in productos]

    def actualizar_producto(self, producto_id: int, update_data: ProductoUpdate) -> ProductoResponse:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        
        # Si se está cambiando el código, verificar que no exista ya
        if update_data.codigo and update_data.codigo != producto.codigo:
            existente = self.repo.get_by_codigo(update_data.codigo)
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nuevo código ya está en uso"
                )
        
        producto_actualizado = self.repo.update(producto, update_data)
        return ProductoResponse.model_validate(producto_actualizado)

    def eliminar_producto(self, producto_id: int) -> None:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        # Opcional: verificar que no tenga movimientos de inventario asociados
        self.repo.delete(producto)