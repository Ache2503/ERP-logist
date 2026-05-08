import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, ForeignKeyConstraint, Index, CheckConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


class Resenas(Base):

    __tablename__ = 'resenas'
    __table_args__ = (
        CheckConstraint('(`calificacion` >= 1 AND `calificacion` <= 5)', name='resenas_chk_1'),
        ForeignKeyConstraint(['id_pedido_cliente'], ['pedidos_clientes.id_pedido_cliente'], name='resenas_ibfk_1'),
        ForeignKeyConstraint(['id_cliente'], ['clientes.id_cliente'], name='resenas_ibfk_2'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='resenas_ibfk_3'),
        Index('idx_resena_pedido', 'id_pedido_cliente'),
        Index('idx_resena_cliente', 'id_cliente'),
        Index('idx_resena_empleado', 'id_empleado'),
    )

    id_resena: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_pedido_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_cliente: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    calificacion: Mapped[int] = mapped_column(Integer, nullable=False)
    comentario: Mapped[Optional[str]] = mapped_column(Text)
    fecha_resena: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    pedidos_clientes: Mapped['PedidosClientes'] = relationship('PedidosClientes', back_populates='resenas')
    clientes: Mapped['Clientes'] = relationship('Clientes', back_populates='resenas')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='resenas')
