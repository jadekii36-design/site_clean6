# Fly.io / container deployment for the Django app
FROM python:3.12.8-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /app

# psycopg2-binary needs libpq at runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build static assets into the image (collectstatic does not need the DB)
RUN python manage.py collectstatic --noinput

EXPOSE 8080

# Run migrations on boot, then serve. Bind explicitly to 0.0.0.0:$PORT.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application -c config/gunicorn.conf.py -b 0.0.0.0:${PORT}"]
