# Sentinel

A distributed uptime monitor — add a URL, Sentinel checks it on a schedule, logs the results, and opens an incident when something goes down.

Built this to get real hands-on experience with async task processing and distributed systems, not just another CRUD app. The scheduling/worker split (Celery Beat deciding what's due, workers actually doing the checks) was the main thing I wanted to get right.

## How it works

You register a monitor with a URL and a check interval → Celery Beat periodically scans for monitors that are due → those get pushed onto a Redis queue → Celery workers pick them up and run the actual HTTP health check → results get written to PostgreSQL → if a check fails, an incident gets created and the monitor status flips.

## Stack

**Backend:** FastAPI, PostgreSQL (SQLAlchemy), Celery + Redis, HTTPX, JWT auth

## API

```
POST   /auth/register
POST   /auth/login

POST   /monitors
GET    /monitors
GET    /monitors/{id}
DELETE /monitors/{id}

GET    /incidents
GET    /incidents/{id}

GET    /results
GET    /results/{monitor_id}
```

## Running it locally

```bash
git clone https://github.com/YSR99/Sentinel_uptime_monitor.git
cd Sentinel_uptime_monitor
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Add a `.env`:
```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379/0
```

Run everything (three separate terminals):
```bash
uvicorn app.main:app --reload
celery -A app.workers.celery_app:celery worker --loglevel=info
celery -A app.workers.celery_app:celery beat --loglevel=info
```

## What's next

- Email / Slack / SMS alerts on incidents
- Analytics dashboard
- Multi-region checks
- Docker + Kubernetes deployment

## Author

Yuvraj Rana — Computer Science Engineering
