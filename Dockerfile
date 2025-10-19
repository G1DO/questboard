FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi.py \
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --workers 3 --threads 2 --timeout 60"

WORKDIR /app

# Install deps first (better layer cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user + group
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Copy code as that user (no chown needed later)
COPY --chown=appuser:appuser . .

USER appuser

# Run migrations (no-op if none) then start gunicorn
CMD bash -lc "flask db upgrade || true; gunicorn wsgi:app"
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi.py \
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --workers 3 --threads 2 --timeout 60"

WORKDIR /app

# Install deps first (better layer cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user + group
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Copy code as that user (no chown needed later)
COPY --chown=appuser:appuser . .

USER appuser

# Run migrations (no-op if none) then start gunicorn
CMD bash -lc "flask db upgrade || true; gunicorn wsgi:app"
