// API URL configuration - single source of truth for backend URL
export const API_BASE_URL = 'http://catvsdog.example.com/backend';

// Helper function to get the full API URL
export const getApiUrl = (endpoint: string): string => {
  // Make sure the endpoint starts with a slash if not already
  const formattedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  
  // Make sure endpoint ends with a trailing slash for backend compatibility
  const withTrailingSlash = formattedEndpoint.endsWith('/') 
    ? formattedEndpoint 
    : `${formattedEndpoint}/`;
    
  return `${API_BASE_URL}${withTrailingSlash}`;
}; 