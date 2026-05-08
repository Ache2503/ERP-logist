import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_marca', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function MarcasTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/marcas/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Marcas ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nueva Marca
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
