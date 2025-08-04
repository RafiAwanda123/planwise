# Dockerfile for ERP Webapp Frontend
# Multi-stage build for optimized production image

# Build stage
FROM node:20-alpine AS builder
# FROM node:20

# Set working directory
WORKDIR /app

# Enable corepack
# RUN corepack enable
# RUN corepack prepare pnpm@latest --activate

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install pnpm
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN pnpm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

#RUN echo 'server {\
#    listen 80;\
#    location /{
#        root /usr/share/nginx/html; \
#        index index.html; \
#        try_files $uri $uri/ /index.html; \
#    } \
#    location /api/{
#        proxy_pass http://localhost:5000; \
#        proxy_set_header Host $host; \
#        proxy_set_header X-Real-IP $remote_addr; \
#    } \
#}' /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

# Health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    # CMD wget --no-verbose --tries=1 --spider http://localhost || exit 1
    # CMD curl -f http://localhost/ || exit 1

# Start nginx
#CMD ["nginx", "-g", "daemon off;"]
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0", "--port", "3000"]