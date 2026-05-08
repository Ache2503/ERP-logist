import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_almacen', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'id_tipo_almacen', label: 'Tipo' },
  { key: 'ubicacion', label: 'Ubicación' },
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
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function AlmacenesTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/almacenes/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Almacenes ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Almacén
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
