import React, { createContext, useState, useContext, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { Product } from './ProductContext';

interface CartContextType {
  cart: Product[];
  addToCart: (product: Product) => void;
  removeFromCart: (productId: string) => void;
  isInCart: (productId: string) => boolean;
  clearCart: () => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [cart, setCart] = useState<Product[]>([]);

  const addToCart = (product: Product) => {
    if (!isAuthenticated) return;

    setCart(prevCart => {
      // Check if product is already in cart
      if (prevCart.some(item => item.id === product.id)) {
        return prevCart;
      }
      return [...prevCart, product];
    });
  };

  const removeFromCart = (productId: string) => {
    if (!isAuthenticated) return;

    setCart(prevCart => prevCart.filter(item => item.id !== productId));
  };

  const isInCart = (productId: string) => {
    if (!isAuthenticated) return false;

    return cart.some(item => item.id === productId);
  };

  const clearCart = () => {
    if (!isAuthenticated) return;

    setCart([]);
  };

  return (
    <CartContext.Provider value={{ 
      cart, 
      addToCart, 
      removeFromCart, 
      isInCart,
      clearCart 
    }}>
      {children}
    </CartContext.Provider>
  );
};

// Custom hook to use the cart context
export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
