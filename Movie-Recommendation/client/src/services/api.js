import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only clear auth and redirect if it's actually an auth error
    // and not a network error or other 401 that might be temporary
    // if (error.response?.status === 401 && error.response?.data?.error?.includes('Authentication')) {
    //   console.log('Authentication error, clearing token and redirecting to login');
    //   localStorage.removeItem('token');
    //   localStorage.removeItem('user');
    //   window.location.href = '/login';
    // }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  signup: (userData) => api.post('/auth/signup', userData),
};

// Movies API
export const moviesAPI = {
  getMovies: (params = {}) => api.get('/movies', { params }),
  getMovie: (movieId) => api.get(`/movies/${movieId}`),
  searchMovies: (query, params = {}) => api.get('/movies/search', { 
    params: { q: query, ...params } 
  }),
  getRatedMovies: (params = {}) => api.get('/movies/rated', { params }),
  rateMovie: (movieId, rating) => api.post('/movies/rate', {
    movie_id: movieId,
    rating: rating
  }),
};

// Recommendations API
export const recommendationsAPI = {
  getRecommendations: (params = {}) => api.get('/recommendations', { params }),
  getProfile: () => api.get('/recommendations/profile'),
  getSimilarity: (movieId1, movieId2) => api.get('/recommendations/similarity', {
    params: { movie_id1: movieId1, movie_id2: movieId2 }
  }),
  explainRecommendation: (movieId) => api.get('/recommendations/explain', {
    params: { movie_id: movieId }
  }),
};

export default api;
