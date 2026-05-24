from app.tasks.celery_app import celery
from app.services.monitor_service import perform_monitor_check


@celery.task
def monitor_url(url: str):
    result = perform_monitor_check(url)

    print(result)

    return result