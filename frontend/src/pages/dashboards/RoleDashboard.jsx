import DashboardAdmin from './DashboardAdmin';
import DashboardVendedor from './DashboardVendedor';
import DashboardAlmacenista from './DashboardAlmacenista';
import DashboardContador from './DashboardContador';
import DashboardGerente from './DashboardGerente';
import DashboardConductor from './DashboardConductor';

const dashboards = {
  Administrador: DashboardAdmin,
  Vendedor: DashboardVendedor,
  Almacenista: DashboardAlmacenista,
  Contador: DashboardContador,
  Gerente: DashboardGerente,
  Transportista: DashboardConductor,
};

export default function RoleDashboard({ cargo }) {
  const Dashboard = dashboards[cargo];
  if (!Dashboard) {
    return (
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
        <p>Bienvenido al sistema. Tu rol es: <strong>{cargo || 'No definido'}</strong></p>
        <p className="text-gray-500 mt-2">Usa el menú lateral para navegar.</p>
      </div>
    );
  }
  return <Dashboard />;
}
