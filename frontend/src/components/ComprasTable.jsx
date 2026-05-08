import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_compra', label: 'ID' },
  { key: 'numero_compra', label: 'Número' },
  { key: 'id_proveedor', label: 'Proveedor' },
  { key: 'id_empleado', label: 'Empleado' },
  { key: 'id_almacen', label: 'Almacén' },
  { key: 'total', label: 'Total', render: (row) => `$${row.total ? row.total.toFixed(2) : '0.00'}` },
  { 
    key: 'estatus', 
    label: 'Estatus',
    render: (row) => (
      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
        row.estatus === 'completada' ? 'bg-green-100 text-green-800' : 
        row.estatus === 'pendiente' ? 'bg-yellow-100 text-yellow-800' :
        'bg-gray-100 text-gray-800'
      }`}>
        {row.estatus}
      </span>
    )
  },
  { key: 'fecha_compra', label: 'Fecha' },
];

export default function ComprasTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/compras/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Compras ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nueva Compra
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
