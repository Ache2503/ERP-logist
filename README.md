# 🚀 ERP System - Backend API

Este es el núcleo de servicios (Backend) para un sistema de **Planificación de Recursos Empresariales (ERP)** modular, robusto y escalable. La aplicación está diseñada siguiendo patrones de arquitectura limpia para facilitar el mantenimiento y la extensión de funcionalidades.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.12+
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Asíncrono y de alto rendimiento)
* **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
* **Validación de Datos:** [Pydantic v2](https://docs.pydantic.dev/)
* **Migraciones de DB:** [Alembic](https://alembic.sqlalchemy.org/)
* **Base de Datos:** MariaDB / MySQL
* **Contenedores:** [Docker](https://www.docker.com/) & Docker Compose

## 🏗️ Arquitectura del Proyecto

El proyecto implementa una arquitectura por capas basada en la **Separación de Responsabilidades (SoC)** para asegurar un código limpio y testeable:

1.  **Models (ORM):** Definición de las tablas y relaciones de la base de datos.
2.  **Schemas (DTOs):** Modelos de Pydantic para validación de entrada/salida y tipado estricto.
3.  **Repositories:** Capa de acceso a datos que encapsula todas las consultas SQL (Patrón Repositorio).
4.  **Services:** Capa de lógica de negocio donde se aplican reglas y validaciones complejas.
5.  **Controllers (API):** Endpoints de FastAPI que gestionan las peticiones HTTP y las respuestas.

## 📦 Módulos Principales

El backend está organizado de forma modular, incluyendo:
* **Inventario:** Gestión completa de productos, categorías, marcas y unidades de medida.
* **Almacenes:** Control de stock físico y tipos de almacén.
* **Personal:** Gestión de empleados, roles y permisos de acceso.
* **Comercial:** Administración de clientes, proveedores y sus respectivos contactos.
* **Operaciones:** Flujos de compras, ventas, pedidos y devoluciones.
* **Logística:** Control de vehículos, rutas y seguimiento de envíos.

## 🚀 Instalación y Configuración

### Requisitos Previos
* Python 3.12 o superior
* Docker y Docker Compose (opcional)

### Pasos para el despliegue local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/proyecto-erp.git
    cd proyecto-erp/backend
    ```

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` basado en `.env.example` y configura tus credenciales de base de datos.

3.  **Crear entorno virtual e instalar dependencias:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Ejecutar migraciones:**
    ```bash
    alembic upgrade head
    ```

5.  **Iniciar el servidor:**
    ```bash
    python run.py
    ```

## 🐳 Despliegue con Docker

Para levantar todo el stack (API + Base de Datos) de forma rápida:
```bash
docker-compose up --build
```

## 📖 Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva y probar los endpoints en:
* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

---

## ✒️ Autores
* **Axel Michael Gonzalez Orihuela** - *Desarrollo Inicial y Arquitectura*

---
