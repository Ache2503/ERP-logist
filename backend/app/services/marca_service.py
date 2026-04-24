"""
Service for managing brands in the application.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from typing import List, Optional
from app.models.marcas import Marcas
from app.schemas.marcas import MarcaCreate, MarcaUpdate
from app.repositories.marca_repository import MarcaRepository


class MarcaService:
    """
    Service class for handling brand-related operations.
    """

    def __init__(self, db: Session):
        self.repo = MarcaRepository(db)

    def create_marca(self, marca_create: MarcaCreate) -> Marcas:
        """
        Create a new brand in the database.
        """
        db_marca = Marcas(**marca_create.dict())
        self.repo.create(db_marca)
        return db_marca

    def get_marca(self, marca_id: int) -> Optional[Marcas]:
        """
        Retrieve a brand by its ID.
        """
        return self.repo.get(marca_id)

    def get_marcas(self) -> List[Marcas]:
        """
        Retrieve all brands from the database.
        """
        return self.repo.list()

    def update_marca(self, marca_id: int, marca_update: MarcaUpdate) -> Optional[Marcas]:
        """
        Update an existing brand's information.
        """
        db_marca = self.get_marca(marca_id)
        if not db_marca:
            return None
        for key, value in marca_update.dict(exclude_unset=True).items():
            setattr(db_marca, key, value)
        self.repo.update(db_marca)
        return db_marca

    def delete_marca(self, marca_id: int) -> bool:
        """
        Delete a brand from the database.
        """
        db_marca = self.get_marca(marca_id)
        if not db_marca:
            return False
        self.repo.delete(db_marca)
        return True