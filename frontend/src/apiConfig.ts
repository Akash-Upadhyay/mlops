// API URL configuration - use relative URLs so all requests go to the same host
export const API_BASE_URL = ''; // Empty string for relative URLs

// Helper function to get the full API URL
export const getApiUrl = (endpoint: string): string => {
  // Make sure the endpoint starts with a slash if not already
  const formattedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  
  // Make sure endpoint ends with a trailing slash for backend compatibility
  const withTrailingSlash = formattedEndpoint.endsWith('/') 
    ? formattedEndpoint 
    : `${formattedEndpoint}/`;
    
  // Add /api prefix to all requests
  return `/api${withTrailingSlash}`;
}; 