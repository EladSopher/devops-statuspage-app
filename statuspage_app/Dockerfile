# ───────────── STAGE 1: Build dependencies ─────────────
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libxml2-dev libxslt1-dev libffi-dev libssl-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# ───────────── STAGE 2: Final App Image ─────────────
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH="/app:/app/statuspage"
ENV DJANGO_SETTINGS_MODULE=statuspage.settings

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

RUN python statuspage/manage.py collectstatic --noinput

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]