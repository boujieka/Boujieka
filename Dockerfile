# ---------------------------------------------------------------------------
# ATEN — image de production (Next.js 14 + Prisma + PostgreSQL)
# Build : docker build -t aten .
# Run   : docker run -p 3000:3000 --env-file .env aten
# ---------------------------------------------------------------------------

FROM node:20-bookworm-slim AS base
WORKDIR /app
# openssl est requis par le moteur de requêtes Prisma.
RUN apt-get update && apt-get install -y --no-install-recommends openssl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# --- Dépendances (toutes, dev incluses : nécessaires au build) --------------
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci

# --- Build (prisma generate + next build via le script "build") -------------
FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# --- Runtime ----------------------------------------------------------------
FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000
# node_modules contient le client Prisma généré et la CLI prisma (migrations).
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/.next ./.next
COPY --from=build /app/prisma ./prisma
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/next.config.mjs ./next.config.mjs

EXPOSE 3000
# Applique les migrations puis démarre. (Retirer `migrate deploy` si les
# migrations sont gérées par un job séparé — voir DEPLOYMENT.md.)
CMD ["sh", "-c", "npx prisma migrate deploy && npm run start"]
