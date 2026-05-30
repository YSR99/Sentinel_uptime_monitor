from celery import Celery


celery = Celery(
    "sentinel",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
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