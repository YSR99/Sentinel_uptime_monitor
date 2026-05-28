from celery import shared_task

from app.db.database import SessionLocal
from app.services.scheduler_service import scan_due_monitors


@shared_task
def scan_monitors_task():

    db = SessionLocal()

    try:

        scheduled_count = scan_due_monitors(db)

        print(f"Scheduled {scheduled_count} monitors")

    finally:

        db.close()