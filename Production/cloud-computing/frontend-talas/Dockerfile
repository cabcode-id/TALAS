# Stage 1: Build aplikasi React
FROM node:16 AS builder

WORKDIR /app

# Salin hanya file package untuk caching yang lebih baik
COPY package*.json ./

# Install dependencies dengan npm ci (clean install)
RUN npm install

# Salin semua file lainnya
COPY . .

# Build aplikasi
RUN npm run build

# Stage 2: Serve aplikasi dengan Nginx
FROM nginx:1.21

# Copy hasil build dari stage sebelumnya
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 (default Nginx)
EXPOSE 8080

# Jalankan Nginx di foreground
CMD ["nginx", "-g", "daemon off;"]