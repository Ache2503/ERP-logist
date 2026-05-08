# Sistema ERP - API REST

Sistema de planificación de recursos empresariales completo con backend FastAPI y frontend en React.

## Tabla de Contenidos

1. [Descripción](#descripción)
2. [Tech Stack](#tech-stack)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Autenticación](#autenticación)
5. [Endpoints Disponibles](#endpoints-disponibles)
6. [Instalación](#instalación)
7. [Configuración](#configuración)
8. [Frontend - Guía de Desarrollo](#frontend---guía-de-desarrollo)
9. [Ejemplos de Uso](#ejemplos-de-uso)
10. [Estados del Sistema](#estados-del-sistema)
11. [Modelos de Base de Datos](#modelos-de-base-de-datos)

---

## Descripción

ERP (Enterprise Resource Planning) es un sistema completo para la gestión empresarial que incluye:

- **Gestión de clientes y proveedores**
- **Catálogo de productos** con categorías, marcas y unidades de medida
- **Control de inventario** en múltiples almacenes
- **Módulo de compras** a proveedores
- **Módulo de ventas** y pedidos de clientes
- **Logística** y seguimiento de envíos
- **Gestión de empleados** con roles y permisos
- **Sistema de transporte** flotas de vehículos
- **Autenticación JWT** para empleados
- **Dashboard personalizado** por usuario

---

## Tech Stack

### Backend
| Tecnología | Versión |
|------------|--------|
| FastAPI | 0.115.6 |
| SQLAlchemy | 2.0.36 |
| Uvicorn | 0.34.0 |
| PyMySQL | 1.1.1 |
| Pydantic | 2.10.4 |
| Python-Jose | 3.3.0 |
| Passlib | 1.7.4 |
| Alembic | 1.14.1 |

### Frontend
| Tecnología | Versión |
|------------|---------|
| React | 19.2.5 |
| Vite | 8.0.10 |
| Tailwind CSS | 3.4.19 |
| React Router DOM | 7.14.2 |

### Base de Datos
- **MySQL** - Base de datos relacional

---

## Estructura del Proyecto

```
proyecto-erp/
├── backend/                 # API REST
│   ├── app/
│   │   ├── api/          # Controladores (routes)
│   │   ├── core/         # Configuración, seguridad
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── repositories/  # Acceso a datos
│   │   ├── schemas/     # Schemas Pydantic
│   │   ├── services/    # Lógica de negocio
│   │   └── utils/       # Utilidades
│   ├── migrations/       # Alembic
│   ├── requirements.txt
│   ├── run.py          # Entry point
│   └── README.md
├── frontend/               # Aplicación web React
│   ├── src/
│   │   ├── components/  # Componentes reutilizables
│   │   ├── hooks/       # Custom hooks (useApi, useAuth)
│   │   ├── pages/       # Páginas del sistema
│   │   └── App.jsx      # Configuración de rutas
│   ├── FRONTEND_GUIDE.md  # Guía para desarrolladores
│   └── README.md
├── docs/                # Documentación técnica
└── README.md           # Este archivo
```

---

## Autenticación

### Backend (JWT)

El sistema utiliza JWT (JSON Web Tokens) para autenticar empleados.

**Endpoint de Login:**
```bash
POST http://localhost:8000/auth/login
Content-Type: application/json

{
  "email": "empleado@empresa.com",
  "password": "contraseña123"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "empleado": {
    "id_empleado": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@empresa.com",
    "cargo": "Administrador"
  }
}
```

### Frontend

- **LoginPage.jsx**: Página de inicio de sesión
- **useAuth.jsx**: Hook personalizado para gestionar autenticación
- **ProtectedRoute.jsx**: Componente para proteger rutas
- **Dashboard personalizado**: Muestra información del empleado y estadísticas

**Flujo:**
1. Empleado inicia sesión con email y contraseña
2. Se guarda el JWT en `localStorage`
3. Se redirige al dashboard personalizado
4. El empleado puede cerrar sesión desde el header

---

## Frontend - Guía de Desarrollo

Para una guía completa de cómo agregar nuevos módulos y patrones de código, consultar:
👉 **[frontend/FRONTEND_GUIDE.md](./frontend/FRONTEND_GUIDE.md)**

### Inicio Rápido

```bash
cd frontend
npm install
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

### Características Implementadas

- ✅ Sistema de login con JWT
- ✅ Rutas protegidas
- ✅ Dashboard personalizado por empleado
- ✅ Sidebar con navegación a todos los módulos
- ✅ Tablas de datos con paginación para todos los módulos
- ✅ Logout desde el header
- ✅ Manejo de estado con Context API

---

## Endpoints Disponibles

### Módulos Funcionales

| Módulo | Prefijo | Métodos HTTP | Descripción |
|--------|--------|------------|-----------|
| **Auth** | `/auth` | POST | Autenticación (por implementar) |
| **Roles & Permisos** | `/roles`, `/permisos` | GET, POST, PUT, DELETE | Gestión de Roles y Permisos |
| **Empleados** | `/empleados` | GET, POST, PUT, DELETE, PATCH | Personal de la empresa |
| **Clientes** | `/clientes` | GET, POST, PUT, DELETE, PATCH | Clientes |
| **Proveedores** | `/proveedores` | GET, POST, PUT, DELETE | Proveedores |
| **Categorías** | `/categorias` | GET, POST, PUT, DELETE | Categorías de productos |
| **Marcas** | `/marcas` | GET, POST, PUT, DELETE | Marcas de productos |
| **Unidades Medida** | `/unidades-medida` | GET, POST, PUT, DELETE | Unidades (kg, pcs, etc) |
| **Almacenes** | `/almacenes` | GET, POST, PUT, DELETE | Bodegas |
| **Tipos Almacén** | `/tipos-almacen` | GET, POST, PUT, DELETE | Tipos de bodega |
| **Vehículos** | `/vehiculos` | GET, POST, PUT, DELETE | Flota vehicular |
| **Tipos Vehículos** | `/tipos-vehiculos` | GET, POST | Tipos de unidad |
| **Productos** | `/productos` | GET, POST, PUT, DELETE | Catálogo de productos |
| **Inventario** | `/inventario` | GET, POST, PUT, DELETE, AJUSTAR | Control de stock |
| **Compras** | `/compras` | GET, POST, PUT, DELETE | Órdenes de compra |
| **Ventas** | `/ventas` | GET, POST, PUT, DELETE | Ventas directas |
| **Logística** | `/logistica` | GET, POST, PUT, DELETE | Envíos y rutas |
| **Pedidos Clientes** | `/pedidos-clientes` | GET, POST, PUT, DELETE | Órdenes de venta |

---

## Datos de Prueba Existentes

| Módulo | Cantidad | Notas |
|--------|----------|-------|
| Empleados | 2 | |
| Clientes | 3 | |
| Marcas | 2 | Samsung |
| Unidades Medida | 2 | kg |
| Categorías | 1 | |
| Almacenes | 1 | Principal |
| Tipo Almacén | 1 | Bodega |
| Ventas | 3 | |
| Pedidos Clientes | 3 | 1 pendiente |

---

## Instalación

### Requisitos Previos
- Python 3.12+
- MySQL 8.0+

### Pasos

```bash
# 1. Clonar el proyecto
git clone <repo-url>
cd proyecto-erp

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate   # Windows

# 4. Instalar dependencias
cd backend
pip install -r requirements.txt

# 5. Configurar base de datos
# Crear base de datos MySQL
mysql -u root -p
CREATE DATABASE erp_db;

# 6. Configurar variables de entorno
cp backend/env.example backend/.env
# Editar .env con credenciales

# 7. Ejecutar migraciones
alembic upgrade head

# 8. Iniciar servidor
python backend/run.py
```

---

## Configuración

### Variables de Entorno (`.env`)

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=erp_db
DB_USER=root
DB_PASSWORD=tu_password

# Aplicación
APP_NAME=ERP API
APP_VERSION=1.0.0
DEBUG=true
ENVIRONMENT=development
```

---

## Documentación API

Una vez iniciado el servidor:

| Recurso | URL |
|--------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## Ejemplos de Uso

### Autenticación
```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "pass"}'
```

### Crear Cliente
```bash
curl -X POST "http://localhost:8000/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@test.com",
    "dirección": "Calle 123",
    "telefono": "5551234567",
    "rfc": "JUAN123"
  }'
```

### Crear Marca
```bash
curl -X POST "http://localhost:8000/marcas/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Samsung"}'
```

### Crear Categoría
```bash
curl -X POST "http://localhost:8000/categorias" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Electrónica"}'
```

### Crear Unidad de Medida
```bash
curl -X POST "http://localhost:8000/unidades-medida" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Kilogramo", "abreviatura": "kg"}'
```

### Crear Producto
**Nota:** Requiere que existan categoría, marca y unidad primero.

```bash
curl -X POST "http://localhost:8000/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell XPS 15",
    "codigo": "LAP-DELL-001",
    "id_categoria": 1,
    "id_marca": 1,
    "id_unidad_medida": 1,
    "precio": 25000.00,
    "estatus": "activo"
  }'
```

### Crear Pedido de Cliente
```bash
curl -X POST "http://localhost:8000/pedidos-clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "id_cliente": 1,
    "id_empleado": 1,
    "id_almacen": 1,
    "estatus": "pendiente"
  }'
```

### Crear Inventario (stock de producto en almacén)
```bash
curl -X POST "http://localhost:8000/inventario" \
  -H "Content-Type: application/json" \
  -d '{
    "id_producto": 1,
    "id_almacen": 1,
    "stock": 50,
    "stock_minimo": 10,
    "stock_maximo": 100
  }'
```

### Ajustar Stock (agregar o quitar)
```bash
# Agregar 10 unidades
curl -X POST "http://localhost:8000/inventario/1/ajustar" \
  -H "Content-Type: application/json" \
  -d '{"cantidad": 10}'

# Restar 5 unidades
curl -X POST "http://localhost:8000/inventario/1/ajustar" \
  -H "Content-Type: application/json" \
  -d '{"cantidad": -5}'
```

### Ver productos bajo stock mínimo
```bash
curl -X GET "http://localhost:8000/inventario/bajo-stock"
```

### Crear Envío
```bash
curl -X POST "http://localhost:8000/logistica" \
  -H "Content-Type: application/json" \
  -d '{
    "id_pedido_cliente": 1,
    "id_vehiculo": 1,
    "id_empleado": 1,
    "estatus": "pendiente"
  }'
```

---

## Estados del Sistema

### Productos/Clientes/Empleados
| Estado | Descripción |
|--------|-----------|
| activo | Disponible/Activo |
| inactivo | No disponible/Inactivo |

### Pedidos Clientes
| Estado | Descripción |
|--------|-----------|
| pendiente | Esperando confirmación |
| confirmado | Confirmado |
| despachado | Enviado |
| entregado | Completado |
| cancelado | Cancelado |

### Compras
| Estado | Descripción |
|--------|-----------|
| pendiente | Esperando |
| confirmada | Aprobada |
| entregada | Recibida |
| cancelada | Cancelada |

### Envíos
| Estado | Descripción |
|--------|-----------|
| pendiente | Por enviar |
| en_transito | En camino |
| entregado | Recibido |

---

## Modelos de Base de Datos

### Tablas Principales
- `clientes` - Catálogo de clientes
- `proveedores` - Catálogo de proveedores
- `empleados` - Personal de la empresa
- `roles` - Roles del sistema
- `permisos` - Permisos disponibles
- `categorias` - Categorías de productos
- `categoria_padre` - Categorías principales
- `marcas` - Marcas de productos
- `unidades_medida` - Unidades de medición
- `almacenes` - Bodegas
- `tipos_almacen` - Tipos de bodega
- `vehiculo` - Flota vehicular
- `tipos_vehiculo` - Tipos de unidad
- `productos` - Catálogo de productos

### Tablas de Transacciones
- `compras` - Órdenes de compra
- `compra_detalle` - Detalles de compra
- `pedidos_clientes` - Pedidos de clientes
- `pedido_cliente_detalle` - Detalles de pedido
- `envios` - Envíos
- `envio_detalle` - Detalles de envío
- `guia_remision` - Guías de remisión
- `movimiento` - Movimientos de inventario

---

## Licencia

MIT License

---

## Autores

Sistema ERP - Equipo de Desarrollo