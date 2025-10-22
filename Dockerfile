FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi.py \
    PORT=8080 \
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:8080 --workers 2 --threads 2 --timeout 60"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# ✅ FIX: make /app writable for non-root user
RUN groupadd -r appuser && useradd -r -g appuser -m appuser && \
    mkdir -p /app/instance && chown -R appuser:appuser /app

COPY --chown=appuser:appuser . .
USER appuser

EXPOSE 8080
CMD ["sh", "-c", "flask db upgrade || true && exec gunicorn --bind 0.0.0.0:8080 wsgi:app"]

