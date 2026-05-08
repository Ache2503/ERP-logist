# Frontend - ERP System

React + Vite + Tailwind CSS

## 📚 Documentación

Para una guía completa de desarrollo y cómo agregar nuevos módulos, consultar:
👉 **[FRONTEND_GUIDE.md](./FRONTEND_GUIDE.md)**

---

## 🛠 Tech Stack

- **React** 19.2.5
- **Vite** 8.0.10
- **Tailwind CSS** 3.4.19
- **React Router DOM** 7.14.2

---

## 🚀 Comandos

```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Construir para producción
npm run build

# Linting
npm run lint

# Vista previa de producción
npm run preview
```

---

## 📁 Estructura

```
frontend/
├── src/
│   ├── components/       # Componentes reutilizables
│   │   ├── DataTable.jsx    # Tabla genérica con paginación
│   │   ├── Layout.jsx       # Estructura principal
│   │   ├── Sidebar.jsx      # Menú lateral
│   │   └── Header.jsx       # Barra superior
│   ├── hooks/
│   │   └── useApi.js        # Hook para consumir API
│   ├── pages/           # Páginas del sistema
│   ├── App.jsx          # Configuración de rutas
│   └── main.jsx         # Entry point
├── package.json
├── vite.config.js
├── tailwind.config.js
└── FRONTEND_GUIDE.md    # Guía de desarrollo
```

---

## 🔗 Backend API

Asegúrate de que el backend esté corriendo en:
- URL: `http://localhost:8000`
- Documentación: `http://localhost:8000/docs`

Consulta el archivo `/README.md` en la raíz para ver todos los endpoints disponibles.
