import axios from 'axios';

// Configure axios defaults
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const AegisAPI = {
  // Get dashboard status
  getStatus: () => api.get('/api/status'),

  // Get telemetry events
  getEvents: (limit = 100) => api.get(`/api/events?limit=${limit}`),

  // Execute commands
  executeCommand: (action) => api.post(`/api/command/${action}`),

  // Get specific event types
  getEventsByType: (eventType, limit = 100) =>
    api.get(`/api/events?type=${eventType}&limit=${limit}`),

  // Search events with filters
  searchEvents: (filters) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] !== null && filters[key] !== undefined) {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/api/events?${params.toString()}`);
  },

  // Test connection
  testConnection: () => api.get('/'),

  // Get dashboard data with fallback
  getDashboardData: async () => {
    try {
      const [statusResponse, eventsResponse] = await Promise.all([
        AegisAPI.getStatus(),
        AegisAPI.getEvents(50)
      ]);

      return {
        status: statusResponse.data,
        events: eventsResponse.data,
        success: true
      };
    } catch (error) {
      console.error('Dashboard data fetch failed:', error);
      return {
        status: {},
        events: [],
        success: false,
        error: error.message
      };
    }
  }
};

export default api;
