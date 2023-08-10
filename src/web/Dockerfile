# Build stage
FROM node:20-alpine3.18 as builder

ARG SERVER_BASE_URL=https://dev.encyclo-flower.com/api/v1
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine3.18 as production

WORKDIR /app
COPY package*.json .
RUN npm ci --omit=dev
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD [ "npm", "run", "start" ]
