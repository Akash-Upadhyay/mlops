// API URL configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://catvsdog-backend-service:8000';

// Helper function to get the full API URL
export const getApiUrl = (endpoint: string): string => {
  // Make sure the endpoint starts with a slash if not already
  const formattedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${API_BASE_URL}${formattedEndpoint}`;
}; 