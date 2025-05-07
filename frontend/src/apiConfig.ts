// API URL configuration - respect environment variables
const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:30800';

// Helper function to get the full API URL
export const getApiUrl = (endpoint: string): string => {
  // Make sure the endpoint starts with a slash if not already
  const formattedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  
  // Make sure endpoint ends with a trailing slash for backend compatibility
  const withTrailingSlash = formattedEndpoint.endsWith('/') 
    ? formattedEndpoint 
    : `${formattedEndpoint}/`;
  
  // If we're using a full URL with path (like http://catvsdogclasifier.com/backend)
  // we need to be careful not to duplicate the path
  if (apiUrl.includes('/backend')) {
    // Remove trailing slash from apiUrl if present
    const baseUrl = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
    return `${baseUrl}${withTrailingSlash}`;
  }
  
  return `${apiUrl}${withTrailingSlash}`;
}; 