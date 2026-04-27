"""
Schemas Pydantic — Pedidos Clientes
Relaciones: clientes + productos + empleados
Tablas: pedidos_clientes + pedido_cliente_detalle
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.schemas.clientes import ClienteResponse
from app.schemas.productos import ProductoResponse
from app.schemas.empleados import EmpleadoResponse


class PedidoClienteDetalleBase(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., gt=0, decimal_places=2)
    descuento_porcentaje: Decimal = Field(default=0, ge=0, le=100, decimal_places=2)


class PedidoClienteDetalleCreate(PedidoClienteDetalleBase):
    pass


class PedidoClienteDetalleResponse(PedidoClienteDetalleBase):
    model_config = ConfigDict(from_attributes=True)
    id_pedido_cliente_detalle: int
    subtotal: Decimal  # cantidad * precio_unitario
    descuento_monto: Decimal
    total: Decimal


class PedidoClienteDetalleConProducto(PedidoClienteDetalleResponse):
    producto: Optional[ProductoResponse] = None


# ── PEDIDO CLIENTE (ORDEN DE VENTA) ─────────────────────────

class PedidoClienteBase(BaseModel):
    numero_pedido: str = Field(..., min_length=1, max_length=50, description="Número único")
    id_cliente: int
    id_empleado: int = Field(..., description="Vendedor/responsable")
    fecha_pedido: datetime = Field(default_factory=datetime.now)
    fecha_entrega_esperada: Optional[datetime] = None
    estado: str = Field(default="pendiente", description="pendiente, confirmado, despachado, entregado, cancelado")
    notas: Optional[str] = None


class PedidoClienteCreate(PedidoClienteBase):
    detalles: list[PedidoClienteDetalleCreate] = Field(..., min_items=1)


class PedidoClienteUpdate(BaseModel):
    numero_pedido: Optional[str] = Field(None, min_length=1, max_length=50)
    id_cliente: Optional[int] = None
    id_empleado: Optional[int] = None
    fecha_entrega_esperada: Optional[datetime] = None
    estado: Optional[str] = None
    notas: Optional[str] = None


class PedidoClienteResponse(PedidoClienteBase):
    model_config = ConfigDict(from_attributes=True)
    id_pedido_cliente: int
    total: Decimal
    fecha_creacion: datetime


class PedidoClienteConDetalles(PedidoClienteResponse):
    """Pedido con todos sus detalles."""
    detalles: list[PedidoClienteDetalleConProducto] = []


class PedidoClienteConRelaciones(PedidoClienteResponse):
    """Pedido con relaciones completas."""
    cliente: Optional[ClienteResponse] = None
    empleado: Optional[EmpleadoResponse] = None
    detalles: list[PedidoClienteDetalleConProducto] = []


class PedidoClienteListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: list[PedidoClienteResponse]