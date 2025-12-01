FROM node:18-alpine AS builder

WORKDIR /app

COPY index.html .

FROM nginx:alpine

COPY --from=builder /app/index.html /usr/share/nginx/html/

EXPOSE 80

USER 1000
