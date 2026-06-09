import os
from celery import Celery

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

celery = Celery(
    "sentinel",
    broker=REDIS_URL,
    backend=REDIS_URL
)


celery.conf.timezone = "UTC"


celery.conf.beat_schedule = {
    "scan-monitors-every-10-seconds": {
        "task": "app.workers.beat_tasks.scan_monitors_task",
        "schedule": 10.0,
    }
}


import app.workers.tasks
import app.workers.beat_tasks