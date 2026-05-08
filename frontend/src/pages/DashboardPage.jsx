export default function DashboardPage() {
  const empleadoStr = localStorage.getItem('empleado');
  const empleado = empleadoStr ? JSON.parse(empleadoStr) : null;
  
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('empleado');
    window.location.href = '/login';
  };

  if (!empleado) {
    return <div className="p-6">No hay datos de usuario. <a href="/login">Ir al login</a></div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">
            ¡Bienvenido, {empleado.nombre || 'Usuario'}!
          </h2>
          <p className="text-gray-600">{empleado.cargo || 'Empleado'}</p>
        </div>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Cerrar Sesión
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Información del Usuario</h3>
        <div className="space-y-2">
          <p><strong>ID:</strong> {empleado.id_empleado}</p>
          <p><strong>Nombre:</strong> {empleado.nombre} {empleado.apellido}</p>
          <p><strong>Email:</strong> {empleado.email}</p>
          <p><strong>Cargo:</strong> {empleado.cargo}</p>
          <p><strong>Estatus:</strong> 
            <span className={`px-2 py-1 rounded text-xs ${
              empleado.estatus === 'activo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              {empleado.estatus}
            </span>
          </p>
        </div>
      </div>

      <div className="mt-6 bg-yellow-50 border border-yellow-200 p-4 rounded">
        <p className="text-yellow-800">
          ⚠️ Dashboard en construcción. Usa el menú lateral para navegar por los módulos.
        </p>
      </div>
    </div>
  );
}
