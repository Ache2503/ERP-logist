"""
Repository — Conductores
Solo acceso a datos, sin lógica de negocio.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.conductores import Conductores
from app.models.asignacion_transporte import AsignacionTransporte
from app.models.envios import Envios
from app.models.pedidos_clientes import PedidosClientes
from app.schemas.conductores import ConductorCreate, ConductorUpdate


class ConductorRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Conductores]:
        return self.db.query(Conductores).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(Conductores).count()

    def get_by_id(self, id_empleado: int) -> Optional[Conductores]:
        return self.db.query(Conductores).filter(
            Conductores.id_empleado == id_empleado
        ).first()

    def get_by_licencia(self, licencia: str) -> Optional[Conductores]:
        return self.db.query(Conductores).filter(
            Conductores.licencia_conducir == licencia
        ).first()

    def create(self, data: ConductorCreate) -> Conductores:
        conductor = Conductores(**data.model_dump())
        self.db.add(conductor)
        self.db.commit()
        self.db.refresh(conductor)
        return conductor

    def update(self, conductor: Conductores, data: ConductorUpdate) -> Conductores:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(conductor, field, value)
        self.db.commit()
        self.db.refresh(conductor)
        return conductor

    def delete(self, conductor: Conductores) -> None:
        self.db.delete(conductor)
        self.db.commit()

    def get_envios_asignados(self, id_empleado: int) -> list[dict]:
        """Obtener envíos asignados a un conductor con datos del pedido"""
        results = (
            self.db.query(
                AsignacionTransporte.id_asignacion,
                AsignacionTransporte.id_envio,
                AsignacionTransporte.fecha_asignacion,
                Envios.id_pedido_cliente,
                Envios.estatus.label('estatus_envio'),
                PedidosClientes.id_cliente,
                PedidosClientes.total,
                PedidosClientes.estatus.label('estatus_pedido'),
                PedidosClientes.requiere_envio,
            )
            .join(Envios, AsignacionTransporte.id_envio == Envios.id_envio)
            .join(PedidosClientes, Envios.id_pedido_cliente == PedidosClientes.id_pedido_cliente)
            .filter(AsignacionTransporte.id_conductor == id_empleado)
            .all()
        )

        from app.models.clientes import Clientes
        formatted = []
        for r in results:
            cliente = self.db.query(Clientes).filter(Clientes.id_cliente == r.id_cliente).first()
            formatted.append({
                'id_asignacion': r.id_asignacion,
                'id_envio': r.id_envio,
                'id_pedido_cliente': r.id_pedido_cliente,
                'id_cliente': r.id_cliente,
                'cliente_nombre': f"{cliente.nombre} {cliente.apellido}" if cliente else None,
                'total_pedido': float(r.total) if r.total else None,
                'estatus_envio': r.estatus_envio,
                'estatus_pedido': r.estatus_pedido,
                'fecha_asignacion': str(r.fecha_asignacion) if r.fecha_asignacion else None,
                'requiere_envio': r.requiere_envio,
            })
        return formatted
