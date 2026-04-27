"""
Service — Pedidos Clientes
Maneja órdenes de venta a clientes
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from app.repositories.pedido_cliente_repository import PedidoClienteRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.almacen_repository import AlmacenRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.pedidos_clientes import (
    PedidoClienteCreate, PedidoClienteUpdate,
    PedidoClienteResponse, PedidoClienteConDetalles, 
    PedidoClienteConRelaciones, PedidoClienteListResponse,
    PedidoClienteDetalleConProducto,
)


class PedidoClienteService:
    def __init__(self, db: Session):
        self.db = db
        # Nota: Crear repositorio si no existe
        self.cliente_repo = ClienteRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.almacen_repo = AlmacenRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> PedidoClienteListResponse:
        # TODO: Implementar
        pass

    def buscar(self, q: str, skip: int = 0, 
              limit: int = 100) -> list[PedidoClienteResponse]:
        # TODO: Implementar
        pass

    def obtener(self, id_pedido_cliente: int) -> PedidoClienteConRelaciones:
        # TODO: Implementar
        pass

    def crear(self, data: PedidoClienteCreate) -> PedidoClienteConDetalles:
        # TODO: Implementar validaciones y creación
        pass

    def actualizar(self, id_pedido_cliente: int, 
                  data: PedidoClienteUpdate) -> PedidoClienteResponse:
        # TODO: Implementar
        pass

    def eliminar(self, id_pedido_cliente: int) -> None:
        # TODO: Implementar
        pass

    def listar_detalles(self, id_pedido_cliente: int) -> list[PedidoClienteDetalleConProducto]:
        # TODO: Implementar
        pass

    def obtener_detalle(self, id_pedido_cliente_detalle: int) -> PedidoClienteDetalleConProducto:
        # TODO: Implementar
        pass

    def eliminar_detalle(self, id_pedido_cliente_detalle: int) -> None:
        # TODO: Implementar
        pass

    def listar_por_cliente(self, id_cliente: int, 
                          skip: int = 0, limit: int = 100) -> list[PedidoClienteResponse]:
        # TODO: Implementar
        pass

    def listar_por_estado(self, estado: str, 
                         skip: int = 0, limit: int = 100) -> list[PedidoClienteResponse]:
        # TODO: Implementar
        pass

    def listar_por_empleado(self, id_empleado: int, 
                           skip: int = 0, limit: int = 100) -> list[PedidoClienteResponse]:
        # TODO: Implementar
        pass