FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi.py \
    # Bind to Render’s $PORT in prod, fall back to 8000 locally
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 2 --timeout 60"

WORKDIR /app

# Install deps first (cache-friendly)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser -m appuser
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000

# Apply migrations (no-op if up-to-date), then start app
CMD bash -lc "flask db upgrade || true; gunicorn wsgi:app"
