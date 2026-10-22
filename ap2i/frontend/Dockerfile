# syntax=docker/dockerfile:1
# AP²I web application — multi-stage build producing a Next.js standalone server.

FROM node:22-alpine AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

FROM node:22-alpine AS build
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# public/africa.geojson is committed; `npm run geo` regenerates it from world-atlas when needed.
RUN npm run build

FROM node:22-alpine AS run
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0 \
    AP2I_API_URL=http://api:8000/api/v1
RUN addgroup -S -g 1001 ap2i && adduser -S -u 1001 -G ap2i ap2i
COPY --from=build --chown=ap2i:ap2i /app/.next/standalone ./
COPY --from=build --chown=ap2i:ap2i /app/.next/static ./.next/static
COPY --from=build --chown=ap2i:ap2i /app/public ./public
USER ap2i
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD wget -qO- http://127.0.0.1:3000/ >/dev/null || exit 1
CMD ["node", "server.js"]
