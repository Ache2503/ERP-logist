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
    git clone https://github.com/Ache2503/ERP-logist.git
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

## 🧠 Decisiones de Arquitectura y Patrones

Para este proyecto, se tomó la decisión consciente de alejarse de la estructura monolítica tradicional (donde las consultas a la base de datos están mezcladas con las rutas) y se implementó un diseño orientado al dominio:

* **Separation of Concerns (SoC):** Cada capa tiene una única responsabilidad. Si cambiamos de base de datos mañana, los Controladores y Servicios no se enterarán, ya que solo interactúan con interfaces abstractas.
* **Patrón Repositorio:** Centraliza la lógica de acceso a datos. Evita la duplicación de consultas SQL (a través del ORM) y facilita la creación de pruebas unitarias al permitir inyectar bases de datos en memoria (mocking).
* **Inyección de Dependencias:** Utilizada a través de FastAPI (`Depends`), permite una gestión segura y eficiente del ciclo de vida de las conexiones a la base de datos por cada petición.

## 🚦 Estado del Proyecto (Roadmap)

Este sistema se encuentra en desarrollo activo. A continuación, el progreso de los módulos principales:

- [x] **Arquitectura Base:** Configuración de ORM, migraciones (Alembic) y variables de entorno.
- [x] **Módulo de Inventario:** CRUD completo de Productos, Categorías y Marcas.
- [x] **Esquemas de Seguridad:** Validación estricta de datos de entrada/salida con Pydantic.
- [ ] **Módulo de Autenticación:** Implementación de JWT (JSON Web Tokens) y control de accesos basados en Roles (RBAC).
- [ ] **Módulo de Ventas/Compras:** Transacciones lógicas que afecten el stock en tiempo real.
- [ ] **Cobertura de Pruebas:** Implementación de tests unitarios y de integración.

## 🧪 Pruebas Unitarias e Integración (Próximamente)

La arquitectura de este proyecto está diseñada para ser altamente testeable. En las próximas fases se integrará **Pytest** para evaluar:
1.  **Lógica de Negocio (Servicios):** Verificación de reglas (ej. no permitir stock negativo).
2.  **Endpoints (Controladores):** Pruebas de integración simulando peticiones HTTP con `TestClient` de FastAPI.
---

## ✒️ Autores
* **Axel Michael Gonzalez Orihuela** - *Desarrollo Inicial y Arquitectura*

---
