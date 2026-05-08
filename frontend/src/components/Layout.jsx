import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

export default function Layout() {
  console.log('Layout rendering...');
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 flex-col min-h-screen">
        <Header />
        <main className="flex-1 bg-gray-100 p-6">
          <Outlet />  {/* Aquí se renderiza la página actual */}
        </main>
      </div>
    </div>
  );
}
