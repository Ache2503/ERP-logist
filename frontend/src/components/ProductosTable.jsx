import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_producto', label: 'ID' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'codigo', label: 'Código' },
  { key: 'precio', label: 'Precio', render: (row) => `$${row.precio ? row.precio.toFixed(2) : '0.00'}` },
  { key: 'id_categoria', label: 'Categoría' },
  { key: 'id_marca', label: 'Marca' },
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

export default function ProductosTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/productos/');

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Listado de Productos ({total})</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
          Nuevo Producto
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
