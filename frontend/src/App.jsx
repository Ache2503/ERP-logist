import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import Layout from './components/Layout';
import RoleDashboard from './pages/dashboards/RoleDashboard';
import EmpleadosPage from './pages/EmpleadosPage';
import ClientesPage from './pages/ClientesPage';
import ProductosPage from './pages/ProductosPage';
import MarcasPage from './pages/MarcasPage';
import CategoriasPage from './pages/CategoriasPage';
import UnidadesMedidaPage from './pages/UnidadesMedidaPage';
import AlmacenesPage from './pages/AlmacenesPage';
import ProveedoresPage from './pages/ProveedoresPage';
import VentasPage from './pages/VentasPage';
import ComprasPage from './pages/ComprasPage';
import PedidosClientesPage from './pages/PedidosClientesPage';
import InventarioPage from './pages/InventarioPage';
import LogisticaPage from './pages/LogisticaPage';
import VehiculosPage from './pages/VehiculosPage';
import TiposVehiculosPage from './pages/TiposVehiculosPage';
import RolesPage from './pages/RolesPage';
import PermisosPage from './pages/PermisosPage';
import ConductoresPage from './pages/ConductoresPage';
import ReportesPage from './pages/ReportesPage';

function AppRoutes() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Cargando...</div>;
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />}
      />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<RoleDashboardWrapper />} />
        <Route path="empleados" element={<EmpleadosPage />} />
        <Route path="clientes" element={<ClientesPage />} />
        <Route path="productos" element={<ProductosPage />} />
        <Route path="marcas" element={<MarcasPage />} />
        <Route path="categorias" element={<CategoriasPage />} />
        <Route path="unidades-medida" element={<UnidadesMedidaPage />} />
        <Route path="almacenes" element={<AlmacenesPage />} />
        <Route path="proveedores" element={<ProveedoresPage />} />
        <Route path="ventas" element={<VentasPage />} />
        <Route path="compras" element={<ComprasPage />} />
        <Route path="pedidos-clientes" element={<PedidosClientesPage />} />
        <Route path="inventario" element={<InventarioPage />} />
        <Route path="logistica" element={<LogisticaPage />} />
        <Route path="vehiculos" element={<VehiculosPage />} />
        <Route path="tipos-vehiculos" element={<TiposVehiculosPage />} />
        <Route path="roles" element={<RolesPage />} />
        <Route path="permisos" element={<PermisosPage />} />
        <Route path="conductores" element={<ConductoresPage />} />
        <Route path="reportes" element={<ReportesPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function RoleDashboardWrapper() {
  const { empleado } = useAuth();
  return <RoleDashboard cargo={empleado?.cargo} />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;