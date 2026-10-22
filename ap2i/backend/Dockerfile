# syntax=docker/dockerfile:1
# PYTHON_IMAGE can point at a registry mirror (e.g. mirror.gcr.io/library/python:3.12-slim).
ARG PYTHON_IMAGE=python:3.12-slim
FROM ${PYTHON_IMAGE} AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /srv/ap2i/backend
COPY backend/pyproject.toml ./
# Optional build secret "extra_ca": a CA bundle for build environments behind a TLS-intercepting proxy.
RUN --mount=type=secret,id=extra_ca,required=false \
    if [ -f /run/secrets/extra_ca ]; then export PIP_CERT=/run/secrets/extra_ca; fi; \
    pip install --upgrade pip && pip install "fastapi>=0.115" "uvicorn[standard]>=0.30" "sqlalchemy>=2.0" "alembic>=1.13" \
    "psycopg[binary]>=3.2" "pydantic>=2.7" "pydantic-settings>=2.3" "email-validator>=2.1" "httpx>=0.27" "lxml>=5.0" \
    "argon2-cffi>=23.1" "pyjwt>=2.8" "pyotp>=2.9" "celery[redis]>=5.4" "redis>=5.0" "openpyxl>=3.1" "reportlab>=4.0" \
    "python-multipart>=0.0.9" "pymupdf>=1.24" "pdfplumber>=0.11" "python-docx>=1.1" "beautifulsoup4>=4.12" "pandas>=2.2" "pytest>=8"
COPY backend/ ./
COPY brand/ /srv/ap2i/brand/
RUN useradd --create-home --uid 10001 ap2i && mkdir -p /srv/ap2i/backend/var && chown -R ap2i /srv/ap2i/backend/var
USER ap2i
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header", "--proxy-headers"]
