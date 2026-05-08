import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_producto_almacen', label: 'ID' },
  { key: 'id_producto', label: 'Producto' },
  { key: 'id_almacen', label: 'Almacén' },
  { key: 'stock', label: 'Stock Actual' },
  { key: 'stock_minimo', label: 'Stock Mínimo' },
  { key: 'stock_maximo', label: 'Stock Máximo' },
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
  { key: 'fecha_actualizacion', label: 'Última Actualización' },
];

export default function InventarioTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/inventario/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Control de Inventario ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Registro
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
