import { NavLink } from 'react-router-dom';

const menuItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/empleados', label: 'Empleados', icon: '👥' },
  { path: '/clientes', label: 'Clientes', icon: '🏢' },
  { path: '/productos', label: 'Productos', icon: '📦' },
  { path: '/ventas', label: 'Ventas', icon: '💰' },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4">
      <h2 className="text-2xl font-bold mb-6">ERP System</h2>
      <nav>
        <ul className="space-y-2">
          {menuItems.map(item => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                end={item.path === '/'}   // "end" para que el dashboard solo se active en "/"
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-2 rounded transition-colors ${
                    isActive ? 'bg-blue-600 text-white' : 'hover:bg-gray-700'
                  }`
                }
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}