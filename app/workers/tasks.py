from celery import shared_task

from app.db.database import SessionLocal
from app.services.monitor_service import run_monitor_check


@shared_task
def run_monitor_check_task(monitor_id: int):

    db = SessionLocal()

    try:

        run_monitor_check(
            db=db,
            monitor_id=monitor_id
        )

    except Exception:
        db.rollback()
        raise 

    finally:

        db.close()