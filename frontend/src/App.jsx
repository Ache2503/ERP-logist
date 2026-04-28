import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import EmpleadosPage from './pages/EmpleadosPage';
import ClientesPages from './pages/ClientesPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* La ruta "/" usa el Layout como envoltorio */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="empleados" element={<EmpleadosPage />} />
          <Route path="clientes" element={<ClientesPages />} />
          {/* Próximamente: clientes, productos, etc. */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;