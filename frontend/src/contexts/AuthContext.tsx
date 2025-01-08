import React, { createContext, useState, useContext, ReactNode, useEffect, useCallback } from 'react';
import { api } from '../config/api';

interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  login: async () => {},
  logout: () => {},
  isAuthenticated: false,
  error: null
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem('token')
  );
  const [error, setError] = useState<string | null>(null);

  const setAuthToken = (token: string) => {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post('/api/auth/login', { email, password });
      const { access_token, user: userData } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      
      // Set token in API headers
      setAuthToken(access_token);
      
      // Set user and token in state
      setToken(access_token);
      setUser(userData);
      setError(null);
    } catch (error) {
      setError('Login failed. Please check your credentials.');
      console.error('Login failed', error);
      throw error;
    }
  };

  const logout = useCallback(() => {
    // Remove token from localStorage
    localStorage.removeItem('token');
    
    // Clear user and token state
    setToken(null);
    setUser(null);
    
    // Remove Authorization header
    delete api.defaults.headers.common['Authorization'];
  }, []);

  // Fetch user details when component mounts
  useEffect(() => {
    const fetchUserDetails = async () => {
      if (token) {
        try {
          // Ensure token is set in headers before fetching
          setAuthToken(token);
          
          const response = await api.get('/api/auth/profile');
          setUser(response.data);
        } catch (error) {
          console.error('Failed to fetch user profile:', error);
          // If fetching profile fails, logout the user
          logout();
        }
      }
    };

    fetchUserDetails();
  }, [token, logout]);

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        token, 
        login, 
        logout, 
        isAuthenticated: !!token,
        error
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
