# Build stage
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the code
COPY . .

# Build the app
RUN npm run build

# Production stage - using serve instead of nginx
FROM node:18-alpine

# Install serve package globally
RUN npm install -g serve

# Set working directory
WORKDIR /app

# Copy built assets from the build stage
COPY --from=build /app/build ./build

# Expose port
EXPOSE 3000

# Set environment variable for API URL if needed
# ENV REACT_APP_API_URL=http://backend:8000

# Start serve
CMD ["serve", "-s", "build", "-l", "3000"] 