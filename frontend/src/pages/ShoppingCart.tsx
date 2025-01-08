import React from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemSecondaryAction, 
  Container, 
  Paper 
} from '@mui/material';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const ShoppingCart: React.FC = () => {
  const { cart, removeFromCart, clearCart } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const calculateTotal = () => {
    return cart.reduce((total, product) => total + product.price, 0).toFixed(2);
  };

  if (!isAuthenticated) {
    return (
      <Container maxWidth="md" sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="h6" gutterBottom>
          Please log in to view your cart
        </Typography>
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => navigate('/login')}
        >
          Go to Login
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Shopping Cart
        </Typography>

        {cart.length === 0 ? (
          <Typography variant="body1">Your cart is empty</Typography>
        ) : (
          <>
            <List>
              {cart.map((product) => (
                <ListItem key={product.id} divider>
                  <ListItemText 
                    primary={product.name} 
                    secondary={`$${product.price.toFixed(2)}`} 
                  />
                  <ListItemSecondaryAction>
                    <Button 
                      color="secondary" 
                      variant="outlined"
                      onClick={() => removeFromCart(product.id)}
                    >
                      Remove
                    </Button>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                Total: ${calculateTotal()}
              </Typography>
              <Button 
                color="secondary" 
                variant="outlined"
                onClick={clearCart}
              >
                Clear Cart
              </Button>
              <Button 
                variant="contained" 
                color="primary"
              >
                Checkout
              </Button>
            </Box>
          </>
        )}
      </Paper>
    </Container>
  );
};

export default ShoppingCart;
