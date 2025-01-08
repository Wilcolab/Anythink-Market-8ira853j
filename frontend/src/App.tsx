import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Catalog from './pages/Catalog';
import ItemDetails from './pages/ItemDetails';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import UserProfile from './pages/UserProfile';
import ShoppingCart from './pages/ShoppingCart';
import { ProductProvider } from './contexts/ProductContext';
import { AuthProvider } from './contexts/AuthContext';
import { CartProvider } from './contexts/CartContext';

const theme = createTheme({
  palette: {
    background: {
      default: '#ffffff'
    },
    primary: {
      main: '#090E3C'
    },
    secondary: {
      main: '#5B64F6'
    },
    text: {
      primary: '#000000'
    }
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <ProductProvider>
          <CartProvider>
            <Router>
              <Navbar />
              <Routes>
                {/* Public routes */}
                <Route path="/" element={<Catalog />} />
                <Route path="/item/:id" element={<ItemDetails />} />
                <Route path="/login" element={<Login />} />
                
                {/* Protected routes */}
                <Route element={<ProtectedRoute />}>
                  <Route path="/profile" element={<UserProfile />} />
                  <Route path="/cart" element={<ShoppingCart />} />
                </Route>
              </Routes>
            </Router>
          </CartProvider>
        </ProductProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
