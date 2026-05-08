"""
Service — Conductores
Lógica de negocio: validaciones de unicidad, reglas de estatus.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.conductor_repository import ConductorRepository
from app.schemas.conductores import (
    ConductorCreate, ConductorUpdate,
    ConductorResponse, ConductorListResponse,
    ConductorEnvioResponse, ConductorEnvioListResponse,
)
from app.models.empleados import Empleados


class ConductorService:

    def __init__(self, db: Session):
        self.repo = ConductorRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> ConductorListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        
        # Obtener datos completos con información del empleado
        data_response = []
        for conductor in data:
            emp = self._get_empleado(self.repo.db, conductor.id_empleado)
            data_response.append(
                ConductorResponse(
                    id_empleado=conductor.id_empleado,
                    licencia_conducir=conductor.licencia_conducir,
                    nombre=emp.nombre if emp else None,
                    apellido=emp.apellido if emp else None,
                    email=emp.email if emp else None,
                    estatus=emp.estatus if emp else None
                )
            )
        
        return ConductorListResponse(
            total=total, skip=skip, limit=limit,
            data=data_response
        )

    def obtener(self, id_empleado: int) -> ConductorResponse:
        conductor = self.repo.get_by_id(id_empleado)
        if not conductor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conductor {id_empleado} no encontrado"
            )
        emp = self._get_empleado(self.repo.db, conductor.id_empleado)
        return ConductorResponse(
            id_empleado=conductor.id_empleado,
            licencia_conducir=conductor.licencia_conducir,
            nombre=emp.nombre if emp else None,
            apellido=emp.apellido if emp else None,
            email=emp.email if emp else None,
            estatus=emp.estatus if emp else None
        )

    def crear(self, data: ConductorCreate) -> ConductorResponse:
        # Verificar que el empleado existe
        emp = self._get_empleado(self.repo.db, data.id_empleado)
        if not emp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {data.id_empleado} no encontrado"
            )
        
        # Verificar que el empleado no sea ya conductor
        if self.repo.get_by_id(data.id_empleado):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El empleado {data.id_empleado} ya es conductor"
            )
        
        # Verificar unicidad de licencia
        if self.repo.get_by_licencia(data.licencia_conducir):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un conductor con esa licencia"
            )
        
        # Actualizar cargo del empleado a Transportista
        emp.cargo = 'Transportista'
        self.repo.db.commit()
        
        conductor = self.repo.create(data)
        return ConductorResponse(
            id_empleado=conductor.id_empleado,
            licencia_conducir=conductor.licencia_conducir,
            nombre=emp.nombre,
            apellido=emp.apellido,
            email=emp.email,
            estatus=emp.estatus
        )

    def actualizar(self, id_empleado: int, data: ConductorUpdate) -> ConductorResponse:
        conductor = self.repo.get_by_id(id_empleado)
        if not conductor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conductor {id_empleado} no encontrado"
            )
        
        # Verificar unicidad de licencia si se actualiza
        if data.licencia_conducir:
            existing = self.repo.get_by_licencia(data.licencia_conducir)
            if existing and existing.id_empleado != id_empleado:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un conductor con esa licencia"
                )
        
        conductor = self.repo.update(conductor, data)
        emp = self._get_empleado(self.repo.db, conductor.id_empleado)
        return ConductorResponse(
            id_empleado=conductor.id_empleado,
            licencia_conducir=conductor.licencia_conducir,
            nombre=emp.nombre if emp else None,
            apellido=emp.apellido if emp else None,
            email=emp.email if emp else None,
            estatus=emp.estatus if emp else None
        )

    def eliminar(self, id_empleado: int) -> None:
        conductor = self.repo.get_by_id(id_empleado)
        if not conductor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conductor {id_empleado} no encontrado"
            )
        self.repo.delete(conductor)

    def listar_envios_asignados(self, id_empleado: int) -> ConductorEnvioListResponse:
        """Listar envíos asignados a un conductor"""
        data = self.repo.get_envios_asignados(id_empleado)
        return ConductorEnvioListResponse(
            total=len(data),
            data=[ConductorEnvioResponse(**d) for d in data]
        )

    def _get_empleado(self, db, id_empleado: int):
        return db.query(Empleados).filter(
            Empleados.id_empleado == id_empleado
        ).first()
