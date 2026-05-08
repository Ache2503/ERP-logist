import { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

const columnas = [
  { key: 'id_empleado', label: 'ID' },
  { key: 'nombre', label: 'Nombre', render: (row) => `${row.nombre || ''} ${row.apellido || ''}` },
  { key: 'email', label: 'Email' },
  { key: 'cargo', label: 'Cargo' },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'activo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { 
    key: 'acciones', 
    label: 'Acciones',
    render: (row) => (
      <button
        onClick={() => handleSetPassword(row.id_empleado, row.nombre, row.apellido)}
        className="text-blue-600 hover:text-blue-800 text-sm"
      >
        Cambiar Pass
      </button>
    )
  },
];

export default function EmpleadosTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/empleados/');
  const { empleado: currentUser } = useAuth();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    email: '',
    password: '',
    cargo: '',
  });
  const [submitError, setSubmitError] = useState('');
  const [submitSuccess, setSubmitSuccess] = useState('');
  const [passwordModal, setPasswordModal] = useState({ show: false, id: null, nombre: '', password: '' });

  const handleSetPassword = (id, nombre, apellido) => {
    setPasswordModal({ show: true, id, nombre: `${nombre} ${apellido}`, password: '' });
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');

    try {
      const response = await fetch(`http://localhost:8000/empleados/${passwordModal.id}/set-password`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: passwordModal.password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Error al cambiar contraseña');
      }

      setPasswordModal({ show: false, id: null, nombre: '', password: '' });
      alert('Contraseña actualizada exitosamente');
    } catch (err) {
      setSubmitError(err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');
    setSubmitSuccess('');

    try {
      const response = await fetch('http://localhost:8000/empleados/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          fecha_registro: new Date().toISOString().split('T')[0]
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al crear empleado');
      }

      setSubmitSuccess('Empleado creado exitosamente');
      setFormData({ nombre: '', apellido: '', email: '', password: '', cargo: '' });
      setShowForm(false);
      window.location.reload();
    } catch (err) {
      setSubmitError(err.message);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Gestión de Usuarios ({total})</h2>
        {currentUser?.cargo === 'Administrador' && (
          <button 
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            {showForm ? 'Cancelar' : 'Nuevo Usuario'}
          </button>
        )}
      </div>

      {submitError && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {submitError}
        </div>
      )}

      {submitSuccess && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded mb-4">
          {submitSuccess}
        </div>
      )}

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h3 className="text-lg font-semibold mb-4">Crear Nuevo Usuario</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre *
                </label>
                <input
                  type="text"
                  value={formData.nombre}
                  onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                  required
                  minLength={1}
                  maxLength={100}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Apellido *
                </label>
                <input
                  type="text"
                  value={formData.apellido}
                  onChange={(e) => setFormData({...formData, apellido: e.target.value})}
                  required
                  minLength={1}
                  maxLength={100}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email *
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contraseña * (mínimo 6 caracteres)
              </label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
                minLength={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Cargo
              </label>
              <select
                value={formData.cargo}
                onChange={(e) => setFormData({...formData, cargo: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Seleccionar...</option>
                <option value="Administrador">Administrador</option>
                <option value="Vendedor">Vendedor</option>
                <option value="Almacenista">Almacenista</option>
                <option value="Contador">Contador</option>
                <option value="Gerente">Gerente</option>
              </select>
            </div>

            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              Crear Usuario
            </button>
          </form>
        </div>
      )}

      <DataTable
        columns={columnas}
        data={data}
        loading={loading}
        error={error}
        total={total}
        skip={skip}
        limit={limit}
        onPageChange={setSkip}
      />

      {/* Modal para cambiar contraseña */}
      {passwordModal.show && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">
              Cambiar Contraseña: {passwordModal.nombre}
            </h3>
            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nueva Contraseña (mínimo 6 caracteres) *
                </label>
                <input
                  type="password"
                  value={passwordModal.password}
                  onChange={(e) => setPasswordModal({...passwordModal, password: e.target.value})}
                  required
                  minLength={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="••••••"
                />
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
                >
                  Actualizar
                </button>
                <button
                  type="button"
                  onClick={() => setPasswordModal({ show: false, id: null, nombre: '', password: '' })}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function DataTable({ columns, data, loading, error, total, skip, limit, onPageChange }) {
  if (loading) return <p className="text-center py-4">Cargando...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (!data || data.length === 0) return <p>No hay registros.</p>;

  return (
    <div>
      <div className="overflow-x-auto bg-white shadow rounded">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map(col => (
                <th key={col.key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, i) => (
              <tr key={row.id_empleado || i} className="hover:bg-gray-50">
                {columns.map(col => (
                  <td key={col.key} className="px-6 py-4 whitespace-nowrap text-sm">
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between mt-4">
        <button
          onClick={() => onPageChange(Math.max(0, skip - limit))}
          disabled={skip === 0}
          className="px-4 py-2 bg-white border rounded shadow disabled:opacity-50"
        >
          Anterior
        </button>
        <span className="text-sm text-gray-600">
          Página {Math.floor(skip/limit)+1} de {Math.ceil(total/limit)}
        </span>
        <button
          onClick={() => onPageChange(skip + limit)}
          disabled={skip + limit >= total}
          className="px-4 py-2 bg-white border rounded shadow disabled:opacity-50"
        >
          Siguiente
        </button>
      </div>
    </div>
  );
}
