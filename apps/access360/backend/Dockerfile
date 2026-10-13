FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .
RUN useradd --create-home appuser && mkdir -p /app/storage && chown appuser /app/storage
USER appuser
EXPOSE 8000
# PORT is honoured for hosts that assign one. Migrations are a separate step (see docs/deployment.md):
#   alembic upgrade head   (with A360_DATABASE_OWNER_URL set)
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers"]
