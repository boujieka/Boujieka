# syntax=docker/dockerfile:1
FROM node:22-slim AS build
WORKDIR /src
COPY package.json package-lock.json ./
# Secret optionnel « extra_ca » : certificat d'un proxy TLS d'entreprise (sans effet s'il est absent).
RUN --mount=type=secret,id=extra_ca,required=false \
    if [ -f /run/secrets/extra_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/extra_ca; fi; \
    npm ci --no-audit --no-fund
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/dist /usr/share/nginx/html
EXPOSE 80
