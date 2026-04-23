"""
Service for managing brands in the application.
"""

from typing import List, Optional
from app.models.marcas import Marca
from app.schemas.marcas import MarcaCreate, MarcaUpdate


class MarcaService:
    """
    Service class for handling brand-related operations.
    """

    def __init__(self):
        self.db = SessionLocal()

    def create_marca(self, marca_create: MarcaCreate) -> Marca:
        """
        Create a new brand in the database.
        """
        db_marca = Marca(**marca_create.dict())
        self.db.add(db_marca)
        self.db.commit()
        self.db.refresh(db_marca)
        return db_marca

    def get_marca(self, marca_id: int) -> Optional[Marca]:
        """
        Retrieve a brand by its ID.
        """
        return self.db.query(Marca).filter(Marca.id == marca_id).first()

    def get_marcas(self) -> List[Marca]:
        """
        Retrieve all brands from the database.
        """
        return self.db.query(Marca).all()

    def update_marca(self, marca_id: int, marca_update: MarcaUpdate) -> Optional[Marca]:
        """
        Update an existing brand's information.
        """
        db_marca = self.get_marca(marca_id)
        if not db_marca:
            return None
        for key, value in marca_update.dict(exclude_unset=True).items():
            setattr(db_marca, key, value)
        self.db.commit()
        self.db.refresh(db_marca)
        return db_marca

    def delete_marca(self, marca_id: int) -> bool:
        """
        Delete a brand from the database.
        """
        db_marca = self.get_marca(marca_id)
        if not db_marca:
            return False
        self.db.delete(db_marca)
        self.db.commit()
        return True