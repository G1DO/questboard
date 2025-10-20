# ==========================
#   QuestBoard – Dockerfile
# ==========================
FROM python:3.12-slim

# Environment configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=wsgi.py \
    PORT=8080 \
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:8080 --workers 2 --threads 2 --timeout 60"

WORKDIR /app

# Install dependencies (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Copy source code as non-root user
COPY --chown=appuser:appuser . .
USER appuser

EXPOSE 8080

# Run migrations (if present) and start Gunicorn
CMD ["bash", "-lc", "flask db upgrade || true && exec gunicorn wsgi:app"]
