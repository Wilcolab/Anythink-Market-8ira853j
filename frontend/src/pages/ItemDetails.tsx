import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Card,
  CardMedia,
  Box,
  Button,
  CircularProgress,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions
} from '@mui/material';
import { ShoppingCart, RemoveShoppingCart } from '@mui/icons-material';
import { api } from '../config/api';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
  description: string;
  detailedDescription: string;
}

export default function ItemDetails() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [loginDialogOpen, setLoginDialogOpen] = useState(false);
  const { addToCart, removeFromCart, isInCart } = useCart();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        if (id) {
          const response = await api.get(`/api/products/${id}`);
          setProduct(response.data);
          setLoading(false);
        }
      } catch (err) {
        console.error('Failed to fetch product:', err);
        setError('Failed to load product details');
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleCartAction = () => {
    if (!product) return;

    if (!isAuthenticated) {
      setLoginDialogOpen(true);
      return;
    }

    if (isInCart(product.id)) {
      removeFromCart(product.id);
      setSnackbarMessage(`${product.name} removed from cart`);
    } else {
      addToCart(product);
      setSnackbarMessage(`${product.name} added to cart`);
    }
    setSnackbarOpen(true);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const handleLoginDialogClose = () => {
    setLoginDialogOpen(false);
  };

  const handleGoToLogin = () => {
    setLoginDialogOpen(false);
    navigate('/login');
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Typography color="error">{error}</Typography>
      </Container>
    );
  }

  if (!product) {
    return (
      <Container sx={{ mt: 4 }}>
        <Typography>No product found</Typography>
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardMedia
              component="img"
              height="400"
              image={product.imageUrl || 'https://via.placeholder.com/400'}
              alt={product.name}
            />
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Typography variant="h4" gutterBottom>
            {product.name}
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            ${product.price.toFixed(2)}
          </Typography>
          <Typography variant="body1" paragraph>
            {product.description}
          </Typography>
          <Typography variant="body2" paragraph>
            {product.detailedDescription}
          </Typography>
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Button 
              variant="contained" 
              color={isAuthenticated && isInCart(product.id) ? 'secondary' : 'primary'} 
              startIcon={isAuthenticated && isInCart(product.id) ? <RemoveShoppingCart /> : <ShoppingCart />}
              onClick={handleCartAction}
            >
              {isAuthenticated 
                ? (isInCart(product.id) ? 'Remove from Cart' : 'Add to Cart')
                : 'Add to Cart'}
            </Button>
            {isAuthenticated && (
              <Button 
                variant="outlined" 
                color="primary"
                onClick={() => navigate('/cart')}
              >
                Go to Cart
              </Button>
            )}
          </Box>
        </Grid>
      </Grid>
      <Snackbar
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        message={snackbarMessage}
      />
      <Dialog
        open={loginDialogOpen}
        onClose={handleLoginDialogClose}
      >
        <DialogTitle>Login Required</DialogTitle>
        <DialogContent>
          <DialogContentText>
            You need to log in to add items to your cart.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleLoginDialogClose}>Cancel</Button>
          <Button onClick={handleGoToLogin} color="primary">
            Go to Login
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
