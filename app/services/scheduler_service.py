from datetime import datetime, timezone, timedelta

from app.models.monitor import Monitor
from app.workers.tasks import run_monitor_check_task 

def scan_due_monitors(db):

    current_time = datetime.now(timezone.utc)

    due_monitors = (
        db.query(Monitor)
        .filter(Monitor.next_check_at <= current_time)
        .all()
    )

    for monitor in due_monitors:

        monitor.next_check_at = (
            current_time +
            timedelta(seconds=monitor.interval_sec)
        )

        run_monitor_check_task.delay(monitor.id)

    db.commit()

    return len(due_monitors)
