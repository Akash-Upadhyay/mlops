# Stage 1: Build the React application
FROM node:18-alpine as build

WORKDIR /app

# Define build argument for API URL - this will be set when building for k8s
ARG REACT_APP_API_URL=http://localhost:8000

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Set the API URL from build argument
RUN echo "REACT_APP_API_URL=$REACT_APP_API_URL" > .env
RUN cat .env

# Build the app (outputs to /app/build)
RUN npm run build

# Stage 2: Serve the app with nginx
FROM nginx:alpine

# Copy the build output to nginx's serve directory
COPY --from=build /app/build /usr/share/nginx/html

# Copy a custom nginx config for Kubernetes
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Add health check endpoint
RUN mkdir -p /usr/share/nginx/html/health && \
    echo "OK" > /usr/share/nginx/html/health/index.html

# Expose port 80
EXPOSE 80

# Simple entry point that starts nginx
CMD ["nginx", "-g", "daemon off;"] 