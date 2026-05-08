import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, ForeignKeyConstraint, Index, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base


class Incidentes(Base):

    __tablename__ = 'incidentes'
    __table_args__ = (
        ForeignKeyConstraint(['id_envio'], ['envios.id_envio'], name='incidentes_ibfk_1'),
        ForeignKeyConstraint(['id_empleado'], ['empleados.id_empleado'], name='incidentes_ibfk_2'),
        Index('idx_incidente_envio', 'id_envio'),
        Index('idx_incidente_empleado', 'id_empleado'),
    )

    id_incidente: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_envio: Mapped[int] = mapped_column(Integer, nullable=False)
    id_empleado: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_reporte: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    estatus: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'pendiente'"))
    evidencia: Mapped[Optional[str]] = mapped_column(String(255))

    envios: Mapped['Envios'] = relationship('Envios', back_populates='incidentes')
    empleados: Mapped['Empleados'] = relationship('Empleados', back_populates='incidentes')
