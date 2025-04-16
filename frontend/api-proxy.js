// Simple API proxy to communicate with the backend service
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Backend service URL (can be configured via environment variables)
const BACKEND_SERVICE = process.env.BACKEND_SERVICE || 'http://catvsdog-service.catvsdog.svc.cluster.local:8000';

// Enable CORS for all routes
app.use(cors());

// Proxy API requests to backend
app.use('/api', createProxyMiddleware({
  target: BACKEND_SERVICE,
  pathRewrite: {
    '^/api': '/'  // Remove the /api prefix when forwarding
  },
  changeOrigin: true,
  logLevel: 'debug'
}));

// Serve static files from the build folder
app.use(express.static(path.join(__dirname, 'build')));

// For any other requests, serve the React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Frontend server with API proxy running on port ${PORT}`);
  console.log(`Proxying API requests to ${BACKEND_SERVICE}`);
}); 