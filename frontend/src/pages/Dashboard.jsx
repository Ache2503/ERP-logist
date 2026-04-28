export default function Dashboard() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded shadow">Total Empleados: 12</div>
        <div className="bg-white p-4 rounded shadow">Clientes: 48</div>
        <div className="bg-white p-4 rounded shadow">Productos: 156</div>
        <div className="bg-white p-4 rounded shadow">Ventas Hoy: $3,200</div>
      </div>
    </div>
  );
}