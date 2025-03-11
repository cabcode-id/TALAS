# Gunakan image Node.js sebagai base untuk membangun aplikasi
FROM node:16 AS builder
WORKDIR /app

# Salin file proyek ke dalam container
COPY package*.json ./
COPY . .

# Install dependensi dan build aplikasi
RUN npm install
RUN npm run build

# Gunakan image Nginx untuk menyajikan file statis
FROM nginx:1.21
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Jalankan Nginx
CMD ["nginx", "-g", "daemon off;"]
