FROM python:3.11-slim
WORKDIR /app
# poppler-utils provides `pdftotext -layout`, used to read official result reports (Phase 2).
RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml ./
COPY app ./app
RUN pip install --no-cache-dir .
COPY alembic.ini ./
COPY alembic ./alembic
RUN useradd --create-home abi
USER abi
EXPOSE 8000
# --no-server-header: do not advertise the server stack. Behind a reverse proxy add
# --proxy-headers --forwarded-allow-ips=<proxy ip> so rate limits see real client IPs.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
