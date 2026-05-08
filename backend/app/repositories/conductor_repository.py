"""
Repository — Conductores
Solo acceso a datos, sin lógica de negocio.
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.conductores import Conductores
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
