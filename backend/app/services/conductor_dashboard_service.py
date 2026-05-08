"""Service — Conductor Dashboard"""
from datetime import date
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from fastapi import HTTPException, status

from app.models.conductores import Conductores
from app.models.empleados import Empleados
from app.models.envios import Envios
from app.models.asignacion_transporte import AsignacionTransporte
from app.models.seguimiento_envio import SeguimientoEnvio
from app.models.vehiculo import Vehiculo
from app.models.pedidos_clientes import PedidosClientes
from app.models.pedido_cliente_detalle import PedidoClienteDetalle
from app.models.clientes import Clientes
from app.models.productos import Productos
from app.models.incidentes import Incidentes
from app.models.resenas import Resenas
from app.schemas.conductores_dashboard import (
    ConductorPerfilResponse, ConductorPerfilUpdate,
    ConductorStats, EnvioDetalleCompleto, EnvioDetalleProducto,
    EnvioClienteInfo, IncidenteCreate, IncidenteResponse,
    ResenaResponse, IncidenteListResponse,
)


class ConductorDashboardService:

    def __init__(self, db: Session):
        self.db = db

    def _get_conductor(self, id_empleado: int) -> Conductores:
        c = self.db.query(Conductores).filter(Conductores.id_empleado == id_empleado).first()
        if not c:
            raise HTTPException(status_code=404, detail="Conductor no encontrado")
        return c

    def obtener_perfil(self, id_empleado: int) -> ConductorPerfilResponse:
        c = self._get_conductor(id_empleado)
        emp = c.empleados
        return ConductorPerfilResponse(
            id_empleado=emp.id_empleado,
            nombre=emp.nombre,
            apellido=emp.apellido,
            email=emp.email,
            telefono=emp.telefono,
            direccion=emp.direccion,
            cargo=emp.cargo,
            estatus=emp.estatus,
            licencia_conducir=c.licencia_conducir,
        )

    def actualizar_perfil(self, id_empleado: int, data: ConductorPerfilUpdate) -> ConductorPerfilResponse:
        c = self._get_conductor(id_empleado)
        emp = c.empleados
        if data.telefono is not None:
            emp.telefono = data.telefono
        if data.direccion is not None:
            emp.direccion = data.direccion
        if data.email is not None:
            emp.email = data.email
        self.db.commit()
        self.db.refresh(emp)
        return self.obtener_perfil(id_empleado)

    def estadisticas(self, id_empleado: int) -> ConductorStats:
        self._get_conductor(id_empleado)

        envios_ids = [
            r[0] for r in
            self.db.query(AsignacionTransporte.id_envio)
            .filter(AsignacionTransporte.id_conductor == id_empleado)
            .all()
        ]

        total = self.db.query(func.count(Envios.id_envio)).filter(Envios.id_envio.in_(envios_ids)).scalar() or 0
        en_ruta = self.db.query(func.count(Envios.id_envio)).filter(Envios.id_envio.in_(envios_ids), Envios.estatus == "en_ruta").scalar() or 0
        entregados = self.db.query(func.count(Envios.id_envio)).filter(Envios.id_envio.in_(envios_ids), Envios.estatus == "entregado").scalar() or 0
        fallidos = self.db.query(func.count(Envios.id_envio)).filter(Envios.id_envio.in_(envios_ids), Envios.estatus.in_(["cancelado", "fallido"])).scalar() or 0
        pendientes = self.db.query(func.count(Envios.id_envio)).filter(Envios.id_envio.in_(envios_ids), Envios.estatus == "pendiente").scalar() or 0
        incidentes = self.db.query(func.count(Incidentes.id_incidente)).filter(Incidentes.id_empleado == id_empleado).scalar() or 0

        calif = self.db.query(func.avg(Resenas.calificacion)).filter(Resenas.id_empleado == id_empleado).scalar()
        total_resenas = self.db.query(func.count(Resenas.id_resena)).filter(Resenas.id_empleado == id_empleado).scalar() or 0

        return ConductorStats(
            total_asignados=total,
            en_ruta=en_ruta,
            entregados=entregados,
            fallidos=fallidos,
            pendientes=pendientes,
            total_incidentes=incidentes,
            calificacion_promedio=round(float(calif or 0), 2),
            total_resenas=total_resenas,
        )

    def detalle_envio(self, id_empleado: int, id_envio: int) -> Optional[EnvioDetalleCompleto]:
        self._get_conductor(id_empleado)

        asignacion = (
            self.db.query(AsignacionTransporte)
            .filter(
                AsignacionTransporte.id_conductor == id_empleado,
                AsignacionTransporte.id_envio == id_envio,
            ).first()
        )
        if not asignacion:
            raise HTTPException(status_code=404, detail="Envío no asignado a este conductor")

        envio = self.db.query(Envios).filter(Envios.id_envio == id_envio).first()
        if not envio:
            raise HTTPException(status_code=404, detail="Envío no encontrado")

        pedido = self.db.query(PedidosClientes).filter(PedidosClientes.id_pedido_cliente == envio.id_pedido_cliente).first() if envio.id_pedido_cliente else None
        cliente = self.db.query(Clientes).filter(Clientes.id_cliente == pedido.id_cliente).first() if pedido else None
        vehiculo = self.db.query(Vehiculo).filter(Vehiculo.id_vehiculo == envio.id_vehiculo).first() if envio.id_vehiculo else None

        productos = []
        if pedido:
            detalles = (
                self.db.query(PedidoClienteDetalle, Productos)
                .join(Productos, Productos.id_producto == PedidoClienteDetalle.id_producto)
                .filter(PedidoClienteDetalle.id_pedido_cliente == pedido.id_pedido_cliente)
                .all()
            )
            for d, p in detalles:
                productos.append(EnvioDetalleProducto(
                    id_producto=p.id_producto,
                    nombre=p.nombre,
                    cantidad=d.cantidad,
                    precio_unitario=d.precio_unitario,
                ))

        seguimiento = [
            {"fecha": s.fecha_seguimiento.isoformat(), "estatus": s.estatus, "ubicacion": s.ubicacion}
            for s in self.db.query(SeguimientoEnvio).filter(SeguimientoEnvio.id_envio == id_envio).order_by(SeguimientoEnvio.fecha_seguimiento).all()
        ]

        return EnvioDetalleCompleto(
            id_envio=envio.id_envio,
            fecha_envio=envio.fecha_envio,
            estatus=envio.estatus,
            id_pedido_cliente=envio.id_pedido_cliente,
            pedido_fecha=pedido.fecha if pedido else None,
            pedido_total=pedido.total if pedido else None,
            pedido_estatus=pedido.estatus if pedido else None,
            vehiculo_placa=vehiculo.placa if vehiculo else None,
            vehiculo_marca=vehiculo.marca if vehiculo else None,
            vehiculo_modelo=vehiculo.modelo if vehiculo else None,
            cliente=EnvioClienteInfo(
                id_cliente=cliente.id_cliente,
                nombre=cliente.nombre,
                apellido=cliente.apellido,
                direccion=cliente.direccion,
                telefono=cliente.telefono,
                email=cliente.email,
            ) if cliente else None,
            productos=productos,
            seguimiento=seguimiento,
        )

    def listar_envios_asignados(self, id_empleado: int, skip: int = 0, limit: int = 100) -> dict:
        self._get_conductor(id_empleado)

        query = (
            self.db.query(AsignacionTransporte, Envios, PedidosClientes, Clientes)
            .join(Envios, Envios.id_envio == AsignacionTransporte.id_envio)
            .join(PedidosClientes, PedidosClientes.id_pedido_cliente == Envios.id_pedido_cliente, isouter=True)
            .join(Clientes, Clientes.id_cliente == PedidosClientes.id_cliente, isouter=True)
            .filter(AsignacionTransporte.id_conductor == id_empleado)
            .order_by(desc(Envios.fecha_envio))
        )

        total = query.count()
        rows = query.offset(skip).limit(limit).all()

        data = []
        for a, e, p, c in rows:
            data.append({
                "id_asignacion": a.id_asignacion,
                "id_envio": e.id_envio,
                "fecha_envio": str(e.fecha_envio),
                "estatus_envio": e.estatus,
                "id_pedido_cliente": p.id_pedido_cliente if p else None,
                "cliente_nombre": f"{c.nombre} {c.apellido or ''}".strip() if c else "N/A",
                "total_pedido": float(p.total) if p else 0,
            })

        return {"total": total, "data": data}

    def crear_incidente(self, id_empleado: int, data: IncidenteCreate) -> IncidenteResponse:
        self._get_conductor(id_empleado)
        envio = self.db.query(Envios).filter(Envios.id_envio == data.id_envio).first()
        if not envio:
            raise HTTPException(status_code=404, detail="Envío no encontrado")

        incidente = Incidentes(
            id_envio=data.id_envio,
            id_empleado=id_empleado,
            tipo=data.tipo,
            descripcion=data.descripcion,
            evidencia=data.evidencia,
            estatus="pendiente",
        )
        self.db.add(incidente)
        self.db.commit()
        self.db.refresh(incidente)
        return IncidenteResponse.model_validate(incidente)

    def listar_incidentes(self, id_empleado: int, skip: int = 0, limit: int = 100) -> IncidenteListResponse:
        self._get_conductor(id_empleado)
        query = self.db.query(Incidentes).filter(Incidentes.id_empleado == id_empleado).order_by(desc(Incidentes.fecha_reporte))
        total = query.count()
        data = query.offset(skip).limit(limit).all()
        return IncidenteListResponse(
            total=total,
            data=[IncidenteResponse.model_validate(i) for i in data],
        )

    def listar_resenas(self, id_empleado: int, skip: int = 0, limit: int = 100) -> list[ResenaResponse]:
        self._get_conductor(id_empleado)
        query = (
            self.db.query(Resenas, Clientes)
            .join(Clientes, Clientes.id_cliente == Resenas.id_cliente, isouter=True)
            .filter(Resenas.id_empleado == id_empleado)
            .order_by(desc(Resenas.fecha_resena))
            .offset(skip).limit(limit).all()
        )
        return [
            ResenaResponse(
                id_resena=r.id_resena,
                calificacion=r.calificacion,
                comentario=r.comentario,
                fecha_resena=r.fecha_resena,
                cliente_nombre=f"{c.nombre} {c.apellido or ''}".strip() if c else "Anónimo",
            )
            for r, c in query
        ]

    def actualizar_estatus_envio(self, id_empleado: int, id_envio: int, estatus: str, ubicacion: Optional[str] = None) -> dict:
        self._get_conductor(id_empleado)
        envio = self.db.query(Envios).filter(Envios.id_envio == id_envio).first()
        if not envio:
            raise HTTPException(status_code=404, detail="Envío no encontrado")

        envio.estatus = estatus
        seguimiento = SeguimientoEnvio(id_envio=id_envio, estatus=estatus, ubicacion=ubicacion)
        self.db.add(seguimiento)
        self.db.commit()

        return {"mensaje": "Estatus actualizado", "id_envio": id_envio, "estatus": estatus}
