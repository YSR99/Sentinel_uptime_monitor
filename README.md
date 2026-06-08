# Sentinel - Uptime Monitoring System

## Overview

Sentinel is a distributed uptime monitoring system that continuously monitors websites and APIs, records health check results, tracks incidents, and executes monitoring tasks asynchronously using Celery workers.

The system allows users to create monitors for websites, schedule automated health checks, and store monitoring history for reliability analysis.

---

## Features

* User Authentication
* Website and API Monitoring
* Periodic Health Checks
* Incident Tracking
* URL Validation
* Background Task Processing with Celery
* Redis-Based Task Queue
* PostgreSQL Database Storage
* Monitoring History and Check Results
* RESTful API Architecture

---

## Architecture

```text
                ┌─────────────┐
                │   Client    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   FastAPI   │
                └──────┬──────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
 ┌─────────────┐             ┌─────────────┐
 │ PostgreSQL  │             │    Redis    │
 └─────────────┘             └──────┬──────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
              ┌─────────────┐              ┌─────────────┐
              │ Celery Beat │              │ Celery Worker│
              └──────┬──────┘              └──────┬──────┘
                     │                            │
                     └────────────┬───────────────┘
                                  ▼
                        Website Health Checks
```

---

## Tech Stack

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* SQLAlchemy ORM

### Task Queue

* Celery
* Redis

### Monitoring

* HTTPX

### Authentication

* JWT Authentication

---

## Monitoring Workflow

1. User creates a monitor.
2. Celery Beat periodically scans for monitors due for execution.
3. Due monitors are sent to Redis.
4. Celery Workers consume monitoring tasks.
5. Sentinel performs an HTTP health check.
6. Results are stored in PostgreSQL.
7. Monitor status is updated.
8. Incidents are created when failures are detected.

---

## API Endpoints

### Authentication

```http
POST /auth/register
POST /auth/login
```

### Monitors

```http
POST /monitors
GET /monitors
GET /monitors/{id}
DELETE /monitors/{id}
```

### Incidents

```http
GET /incidents
GET /incidents/{id}
```

### Check Results

```http
GET /results
GET /results/{monitor_id}
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YSR99/Sentinel_uptime_monitor.git
cd Sentinel_uptime_monitor
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379/0
```

### Run FastAPI

```bash
uvicorn app.main:app --reload
```

### Run Celery Worker

```bash
celery -A app.workers.celery_app:celery worker --loglevel=info
```

### Run Celery Beat

```bash
celery -A app.workers.celery_app:celery beat --loglevel=info
```

---

## Future Improvements

* Email Notifications
* Slack Alerts
* SMS Notifications
* Advanced Analytics Dashboard
* Multi-Region Monitoring
* Docker Deployment
* Kubernetes Support

---

## Author

Yuvraj Rana

Computer Science Engineering Student

