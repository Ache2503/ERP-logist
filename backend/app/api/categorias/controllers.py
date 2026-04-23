"""
api/categorias/controllers.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from app.core.database import get_db
from app.services.categoria_service import CategoriaService
from app.schemas.categorias import (
    CategoriaCreate, CategoriaUpdate,
    CategoriaResponse, CategoriaListResponse,
)
router = APIRouter(prefix="/categorias", tags=["Categorías"])
