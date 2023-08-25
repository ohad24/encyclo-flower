# Build stage
FROM node:20-alpine3.18 as builder

ARG SERVER_BASE_URL
ARG IMAGE_BASE_URL
ARG IMAGE_USER_BASE_URL

ENV SERVER_BASE_URL=$SERVER_BASE_URL
ENV IMAGE_BASE_URL=$IMAGE_BASE_URL
ENV IMAGE_USER_BASE_URL=$IMAGE_USER_BASE_URL

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
