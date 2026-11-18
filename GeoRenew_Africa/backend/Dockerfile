# syntax=docker/dockerfile:1
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY backend/requirements.txt .
# Secret optionnel « extra_ca » : certificat d'un proxy TLS d'entreprise (sans effet s'il est absent).
RUN --mount=type=secret,id=extra_ca,required=false \
    if [ -f /run/secrets/extra_ca ]; then export PIP_CERT=/run/secrets/extra_ca; fi; \
    pip install --no-cache-dir -r requirements.txt
COPY backend/ /app/
# Fichiers d'exemple FICTIFS utilisés par « python -m app.demo load »
COPY examples/ /examples/
RUN useradd --create-home georenew
USER georenew
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && python -m app.demo load && uvicorn app.main:app --host 0.0.0.0 --port 8000 --no-server-header"]
