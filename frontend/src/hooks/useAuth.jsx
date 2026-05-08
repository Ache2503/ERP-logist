import { useState, useEffect, useContext, createContext } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [empleado, setEmpleado] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedEmpleado = localStorage.getItem('empleado');
    const storedToken = localStorage.getItem('token');
    if (storedEmpleado && storedToken) {
      setEmpleado(JSON.parse(storedEmpleado));
      setToken(storedToken);
    }
    setLoading(false);
  }, []);

  const login = (token, empleadoData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('empleado', JSON.stringify(empleadoData));
    setToken(token);
    setEmpleado(empleadoData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('empleado');
    setToken(null);
    setEmpleado(null);
  };

  return (
    <AuthContext.Provider value={{ empleado, token, login, logout, isAuthenticated: !!token }}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
}
