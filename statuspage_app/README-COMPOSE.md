# 🐳 Status-Page Local Docker Compose Setup

## Services:
- `app`: Django + Gunicorn
- `db`: PostgreSQL 13
- `redis`: Redis 6

## How to Run:
```bash
docker-compose up --build
```

## DB Access:
- DB: statuspage
- User: statuspage
- Password: strongpassword

Make sure to configure `configuration.py` inside the Django app to match:
DB host: `db`
Redis host: `redis`

This is **only for local development/testing**.
