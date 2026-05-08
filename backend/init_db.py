"""
Script para inicializar la base de datos con datos de prueba
"""
from app.core.database import SessionLocal, engine, Base
from app.models.empleados import Empleados
from app.core.security import get_password_hash
import datetime


def init_db():
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas correctamente")

    db = SessionLocal()

    try:
        # Verificar si ya hay datos
        existing = db.query(Empleados).count()
        if existing > 0:
            print(f"✓ Base de datos ya tiene {existing} empleados")
            return

        # Crear empleados de prueba
        empleados = [
            Empleados(
                nombre="Admin",
                apellido="Sistema",
                email="admin@erp.com",
                password_hash=get_password_hash("admin123"),
                cargo="Administrador",
                estatus="activo",
                fecha_registro=datetime.date.today(),
            ),
            Empleados(
                nombre="Juan",
                apellido="Perez",
                email="juan@test.com",
                password_hash=get_password_hash("test123"),
                cargo="Vendedor",
                estatus="activo",
                fecha_registro=datetime.date.today(),
            ),
        ]

        for emp in empleados:
            db.add(emp)

        db.commit()
        print(f"✓ {len(empleados)} empleados creados exitosamente")

    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()
    print("¡Inicialización completada!")
