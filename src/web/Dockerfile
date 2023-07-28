# Build stage
FROM node:20-alpine3.18 as builder

WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine3.18 as production

WORKDIR /app
COPY package*.json .
RUN npm ci --only=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD [ "npm", "run", "start" ]
