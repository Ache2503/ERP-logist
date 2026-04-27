"""
Controllers — Pedidos Clientes
Órdenes de venta a clientes
"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.pedido_cliente_service import PedidoClienteService
from app.schemas.pedidos_clientes import (
    PedidoClienteCreate, PedidoClienteUpdate,
    PedidoClienteResponse, PedidoClienteConDetalles, PedidoClienteConRelaciones,
    PedidoClienteListResponse, PedidoClienteDetalleConProducto,
)

router = APIRouter(prefix="/pedidos-clientes", tags=["Pedidos Clientes"])


# ════════════════════════════════════════════════════════════════
# PEDIDOS CLIENTES (ÓRDENES DE VENTA)
# ════════════════════════════════════════════════════════════════

@router.get("", response_model=PedidoClienteListResponse, summary="Listar pedidos")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar(skip, limit)


@router.get("/buscar", response_model=list[PedidoClienteResponse],
            summary="Buscar pedidos por número")
def buscar(
    q: str     = Query(..., min_length=1, description="Número de pedido"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).buscar(q, skip, limit)


@router.post("", response_model=PedidoClienteConDetalles,
             status_code=status.HTTP_201_CREATED,
             summary="Crear pedido con detalles")
def crear(data: PedidoClienteCreate, db: Session = Depends(get_db)):
    return PedidoClienteService(db).crear(data)


@router.get("/{id_pedido_cliente}", response_model=PedidoClienteConRelaciones,
            summary="Obtener pedido con detalles y relaciones")
def obtener(id_pedido_cliente: int, db: Session = Depends(get_db)):
    return PedidoClienteService(db).obtener(id_pedido_cliente)


@router.put("/{id_pedido_cliente}", response_model=PedidoClienteResponse,
            summary="Actualizar pedido")
def actualizar(id_pedido_cliente: int, data: PedidoClienteUpdate,
               db: Session = Depends(get_db)):
    return PedidoClienteService(db).actualizar(id_pedido_cliente, data)


@router.delete("/{id_pedido_cliente}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar pedido (solo si está pendiente o cancelado)")
def eliminar(id_pedido_cliente: int, db: Session = Depends(get_db)):
    PedidoClienteService(db).eliminar(id_pedido_cliente)


@router.get("/cliente/{id_cliente}", response_model=list[PedidoClienteResponse],
            summary="Listar pedidos de un cliente")
def listar_por_cliente(
    id_cliente: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar_por_cliente(id_cliente, skip, limit)


@router.get("/estado/{estado}", response_model=list[PedidoClienteResponse],
            summary="Listar pedidos por estado")
def listar_por_estado(
    estado: str = Query(..., description="pendiente/confirmado/despachado/entregado/cancelado"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar_por_estado(estado, skip, limit)


@router.get("/empleado/{id_empleado}", response_model=list[PedidoClienteResponse],
            summary="Listar pedidos de un empleado (vendedor)")
def listar_por_empleado(
    id_empleado: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar_por_empleado(id_empleado, skip, limit)


# ════════════════════════════════════════════════════════════════
# DETALLES DE PEDIDO
# ════════════════════════════════════════════════════════════════

@router.get("/{id_pedido_cliente}/detalles", response_model=list[PedidoClienteDetalleConProducto],
            summary="Listar detalles de un pedido")
def listar_detalles(id_pedido_cliente: int, db: Session = Depends(get_db)):
    return PedidoClienteService(db).listar_detalles(id_pedido_cliente)


@router.get("/detalles/{id_pedido_cliente_detalle}", response_model=PedidoClienteDetalleConProducto,
            summary="Obtener detalle con producto")
def obtener_detalle(id_pedido_cliente_detalle: int, db: Session = Depends(get_db)):
    return PedidoClienteService(db).obtener_detalle(id_pedido_cliente_detalle)


@router.delete("/detalles/{id_pedido_cliente_detalle}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar detalle (solo si pedido está pendiente)")
def eliminar_detalle(id_pedido_cliente_detalle: int, db: Session = Depends(get_db)):
    PedidoClienteService(db).eliminar_detalle(id_pedido_cliente_detalle)