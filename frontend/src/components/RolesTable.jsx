import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_rol', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function RolesTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/roles/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Gestión de Roles ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Rol
        </button>
      </div>
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
