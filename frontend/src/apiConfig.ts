// API URL configuration for ingress-based Kubernetes deployment
// With ingress, all requests go through the same domain with /api prefix

// Helper function to get the full API URL
export const getApiUrl = (endpoint: string): string => {
  // Make sure the endpoint starts with a slash if not already
  const formattedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  
  // Make sure endpoint ends with a trailing slash for backend compatibility
  const withTrailingSlash = formattedEndpoint.endsWith('/') 
    ? formattedEndpoint 
    : `${formattedEndpoint}/`;
    
  // Add /api prefix to all requests (this will be routed by the ingress controller)
  return `/api${withTrailingSlash}`;
}; 