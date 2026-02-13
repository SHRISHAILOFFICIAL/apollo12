FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy project
COPY . .

# Set API URL at build time (relative URL works with any IP)
ENV NEXT_PUBLIC_API_URL=/api

# Build the Next.js app
RUN npm run build

# Expose port
EXPOSE 3000

# Start production server
CMD ["npm", "start"]
