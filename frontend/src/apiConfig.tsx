// API URL configuration for local Docker development
const apiUrl = 'http://192.168.49.2:30800';  // Hard-coded to ensure it works

// Helper function to get the full API URL
export const getApiUrl = (endpoint: string): string => {
  // Make sure the endpoint starts with a slash if not already
  const formattedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  
  // Make sure endpoint ends with a trailing slash for backend compatibility
  const withTrailingSlash = formattedEndpoint.endsWith('/') 
    ? formattedEndpoint 
    : `${formattedEndpoint}/`;
  
  return `${apiUrl}${withTrailingSlash}`;
}; 