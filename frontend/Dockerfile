# Stage 1: Build the React application
FROM node:18-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Hardcode the API URL directly in the .env file before building
# We're using the host's port 8000 which is mapped to the backend container
RUN echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Build the app (outputs to /app/build)
RUN npm run build

# Stage 2: Serve the app with nginx
FROM nginx:alpine

# Copy the build output to nginx's serve directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Simple entrypoint that just starts nginx
CMD ["nginx", "-g", "daemon off;"] 