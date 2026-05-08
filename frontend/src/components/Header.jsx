import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const { empleado, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white shadow px-6 py-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-gray-800">
        Panel de Administración
      </h1>
      <div className="flex items-center gap-3">
        <span className="text-gray-600">
          {empleado ? `${empleado.nombre} ${empleado.apellido}` : 'Admin'}
        </span>
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
          {empleado?.nombre?.charAt(0) || 'A'}
        </div>
        <button
          onClick={handleLogout}
          className="text-sm text-red-600 hover:text-red-800"
        >
          Cerrar Sesión
        </button>
      </div>
    </header>
  );
}