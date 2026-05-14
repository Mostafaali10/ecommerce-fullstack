// frontend/src/lib/api.ts   (أو frontend/lib/api.ts)
import axios, { type InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';   // غيرها لـ localhost لو عايز

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add token if needed later
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

// ====================== Products ======================
export const productService = {
  getProducts: async (filters?: any) => {
    const response = await api.get('/products', { params: filters });
    return response.data;
  },

  getProductById: async (id: string) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  createProduct: async (data: any) => {
    const response = await api.post('/products', data);
    return response.data;
  },

  updateProduct: async (id: string, data: any) => {
    const response = await api.put(`/products/${id}`, data);
    return response.data;
  },

  deleteProduct: async (id: string) => {
    const response = await api.delete(`/products/${id}`);
    return response.data;
  },
};

// ====================== Categories ======================
export const categoryService = {
  getCategories: async () => {
    const response = await api.get('/categories');
    return response.data;
  },
};

// ====================== Auth ======================
export const authService = {
  login: async (credentials: { email: string; password: string }) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: any) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
};

// ====================== Orders ======================
export const orderService = {
  createOrder: async (orderData: any) => {
    const response = await api.post('/orders', orderData);
    return response.data;
  },

  getMyOrders: async () => {
    const response = await api.get('/orders/me');
    return response.data;
  },
};

// ====================== Cart (مؤقت) ======================
export const cartService = {
  // لو عندك cart في الباك إند، هنعدلها بعدين
  getCart: () => {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
  },
  addToCart: (product: any) => {
    // مؤقت محلي لحد ما نربط الباك إند
    let cart = cartService.getCart();
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    return cart;
  }
};

export { api };