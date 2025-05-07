// API URL configuration for local Docker development
export const API_BASE_URL = 'http://localhost:8000';  // Hard-coded to ensure it works

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