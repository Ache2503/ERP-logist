"""Service — Reportes y Estadísticas"""
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.models.pedidos_clientes import PedidosClientes
from app.models.compras import Compras
from app.models.productos import Productos
from app.models.empleados import Empleados
from app.models.productos_almacen import ProductosAlmacen
from app.schemas.reportes import (
    ResumenVentas, VentaPeriodo, ResumenInventario,
    ResumenEmpleados, ResumenFinanciero, ProductoMasVendido,
    ReporteDashboard,
)


class ReporteService:

    def __init__(self, db: Session):
        self.db = db

    def resumen_ventas(self) -> ResumenVentas:
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        inicio_mes = hoy.replace(day=1)

        def _stats(desde):
            q = self.db.query(func.count(PedidosClientes.id_pedido_cliente),
                              func.coalesce(func.sum(PedidosClientes.total), 0))
            if desde:
                q = q.filter(PedidosClientes.fecha >= desde)
            return q.first()

        c_hoy, m_hoy = _stats(hoy)
        c_sem, m_sem = _stats(inicio_semana)
        c_mes, m_mes = _stats(inicio_mes)

        ventas_por_mes = (
            self.db.query(
                func.date_format(PedidosClientes.fecha, "%Y-%m").label("periodo"),
                func.count(PedidosClientes.id_pedido_cliente).label("total"),
                func.coalesce(func.sum(PedidosClientes.total), 0).label("monto"),
            )
            .filter(PedidosClientes.fecha >= date(hoy.year - 1, hoy.month, 1))
            .group_by(func.date_format(PedidosClientes.fecha, "%Y-%m"))
            .order_by(func.date_format(PedidosClientes.fecha, "%Y-%m"))
            .all()
        )

        return ResumenVentas(
            ventas_hoy=c_hoy or 0,
            ventas_semana=c_sem or 0,
            ventas_mes=c_mes or 0,
            monto_hoy=Decimal(str(m_hoy or 0)),
            monto_semana=Decimal(str(m_sem or 0)),
            monto_mes=Decimal(str(m_mes or 0)),
            ventas_por_periodo=[
                VentaPeriodo(periodo=r.periodo, total_ventas=r.total,
                             monto_total=Decimal(str(r.monto)),
                             promedio_por_venta=Decimal(str(r.monto / r.total)) if r.total else Decimal("0"))
                for r in ventas_por_mes
            ],
        )

    def productos_mas_vendidos(self, limite: int = 10) -> list[ProductoMasVendido]:
        from app.models.pedido_cliente_detalle import PedidoClienteDetalle

        resultados = (
            self.db.query(
                Productos.id_producto,
                Productos.nombre,
                func.coalesce(func.sum(PedidoClienteDetalle.cantidad), 0).label("total_vendido"),
                func.coalesce(func.sum(PedidoClienteDetalle.subtotal), 0).label("monto_total"),
            )
            .join(PedidoClienteDetalle, PedidoClienteDetalle.id_producto == Productos.id_producto)
            .join(PedidosClientes, PedidosClientes.id_pedido_cliente == PedidoClienteDetalle.id_pedido_cliente)
            .filter(PedidosClientes.estatus.in_(["completado", "entregado"]))
            .group_by(Productos.id_producto, Productos.nombre)
            .order_by(func.sum(PedidoClienteDetalle.cantidad).desc())
            .limit(limite)
            .all()
        )

        return [
            ProductoMasVendido(
                id_producto=r.id_producto, nombre=r.nombre,
                total_vendido=int(r.total_vendido or 0),
                monto_total=Decimal(str(r.monto_total or 0)),
            )
            for r in resultados
        ]

    def resumen_inventario(self) -> ResumenInventario:
        total_prod = self.db.query(func.count(Productos.id_producto)).scalar() or 0
        total_stock = int(self.db.query(func.coalesce(func.sum(ProductosAlmacen.stock), 0)).scalar() or 0)
        bajo_stock = (
            self.db.query(func.count(ProductosAlmacen.id_producto_almacen))
            .filter(ProductosAlmacen.stock < 10)
            .scalar() or 0
        )
        valor = (
            self.db.query(func.coalesce(func.sum(Productos.precio * ProductosAlmacen.stock), 0))
            .join(ProductosAlmacen, ProductosAlmacen.id_producto == Productos.id_producto, isouter=True)
            .scalar() or 0
        )

        return ResumenInventario(
            total_productos=int(total_prod),
            total_en_stock=int(total_stock),
            productos_bajo_stock=int(bajo_stock),
            valor_total_inventario=Decimal(str(valor)),
        )

    def resumen_empleados(self) -> ResumenEmpleados:
        total = self.db.query(func.count(Empleados.id_empleado)).scalar() or 0
        activos = self.db.query(func.count(Empleados.id_empleado)).filter(Empleados.estatus == "activo").scalar() or 0
        inactivos = total - activos

        por_cargo = (
            self.db.query(Empleados.cargo, func.count(Empleados.id_empleado).label("total"))
            .group_by(Empleados.cargo)
            .all()
        )

        return ResumenEmpleados(
            total=int(total),
            activos=int(activos),
            inactivos=int(inactivos),
            por_cargo=[{"cargo": r.cargo, "total": r.total} for r in por_cargo],
        )

    def resumen_financiero(self) -> ResumenFinanciero:
        hoy = date.today()
        inicio_mes = hoy.replace(day=1)

        ventas_total = self.db.query(func.coalesce(func.sum(PedidosClientes.total), 0)).scalar() or 0
        compras_total = self.db.query(func.coalesce(func.sum(Compras.subtotal), 0)).scalar() or 0

        ventas_mes = self.db.query(func.coalesce(func.sum(PedidosClientes.total), 0))\
            .filter(PedidosClientes.fecha >= inicio_mes).scalar() or 0
        compras_mes = self.db.query(func.coalesce(func.sum(Compras.subtotal), 0))\
            .filter(Compras.fecha_compra >= inicio_mes).scalar() or 0

        return ResumenFinanciero(
            ventas_totales=Decimal(str(ventas_total)),
            compras_totales=Decimal(str(compras_total)),
            ganancia_estimada=Decimal(str(ventas_total - compras_total)),
            ventas_mes_actual=Decimal(str(ventas_mes)),
            compras_mes_actual=Decimal(str(compras_mes)),
        )

    def dashboard_completo(self, rol: str) -> ReporteDashboard:
        resp = ReporteDashboard()

        if rol in ("Administrador", "Gerente"):
            resp.empleados = self.resumen_empleados()
            resp.ventas = self.resumen_ventas()
            resp.inventario = self.resumen_inventario()
            resp.financiero = self.resumen_financiero()
            resp.productos_mas_vendidos = self.productos_mas_vendidos(5)
        elif rol == "Vendedor":
            resp.ventas = self.resumen_ventas()
            resp.productos_mas_vendidos = self.productos_mas_vendidos(5)
        elif rol == "Almacenista":
            resp.inventario = self.resumen_inventario()
        elif rol == "Contador":
            resp.financiero = self.resumen_financiero()
            resp.ventas = self.resumen_ventas()
        elif rol == "Transportista":
            pass

        return resp
