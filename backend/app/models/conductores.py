from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Index, Column, Integer, String, Float, Date, DateTime, Text, Boolean, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base

class Conductores(Base):
    __tablename__ = 'Conductores'
    __table__args__ = (
        ForeignKeyConstraint(['id.empleado'],['empleados.id_empleado'], name='empleado_ibfk_1')
    )

    id_conductor : Mapped[int] = mapped_column(Integer, primary_key=True)
    id_empleado : Mapped[int] = mapped_column(Integer, nullable=False)
    licencia_conducir : Mapped[str] = mapped_column(String(50), nullable=False)

    empleados : Mapped['Empleados'] = relationship('Empleados', back_populates='conductores')
