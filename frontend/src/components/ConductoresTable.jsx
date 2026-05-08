import { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_empleado', label: 'ID' },
  { key: 'nombre', label: 'Nombre', render: (row) => `${row.nombre || ''} ${row.apellido || ''}` },
  { key: 'licencia_conducir', label: 'Licencia' },
  { key: 'email', label: 'Email' },
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
];

export default function ConductoresTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/conductores/');
  const [empleados, setEmpleados] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ id_empleado: '', licencia_conducir: '' });
  const [submitError, setSubmitError] = useState('');

  // Cargar empleados para el select
  useEffect(() => {
    fetch('http://localhost:8000/empleados/')
      .then(res => res.json())
      .then(data => {
        if (data.data) {
          setEmpleados(data.data.filter(emp => emp.estatus === 'activo'));
        }
      })
      .catch(err => console.error('Error cargando empleados:', err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitError('');

    try {
      const response = await fetch('http://localhost:8000/conductores/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_empleado: parseInt(formData.id_empleado),
          licencia_conducir: formData.licencia_conducir
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Error al crear conductor');
      }

      alert('Conductor creado exitosamente');
      setFormData({ id_empleado: '', licencia_conducir: '' });
      setShowForm(false);
      window.location.reload();
    } catch (err) {
      setSubmitError(err.message);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Transportistas ({total})</h2>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          {showForm ? 'Cancelar' : 'Nuevo Transportista'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <h3 className="text-lg font-semibold mb-4">Crear Nuevo Transportista</h3>
          {submitError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {submitError}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Empleado
              </label>
              <select
                value={formData.id_empleado}
                onChange={(e) => setFormData({...formData, id_empleado: e.target.value})}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Seleccionar empleado...</option>
                {empleados.map(emp => (
                  <option key={emp.id_empleado} value={emp.id_empleado}>
                    {emp.nombre} {emp.apellido} ({emp.email})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Número de Licencia
              </label>
              <input
                type="text"
                value={formData.licencia_conducir}
                onChange={(e) => setFormData({...formData, licencia_conducir: e.target.value})}
                required
                minLength={5}
                maxLength={50}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="ABC123456"
              />
            </div>
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              Crear Transportista
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
        <span className="text-sm text-gray-600">Página {Math.floor(skip/limit)+1} de {Math.ceil(total/limit)}</span>
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
