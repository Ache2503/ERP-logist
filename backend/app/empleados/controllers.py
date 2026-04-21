from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.empleados import Empleados

router = APIRouter(prefix="/empleados", tags=["empleados"])

@router.get("/")
def listar_empleados(db: Session = Depends(get_db)):
    empleados = db.query(Empleados).all()
    return empleados