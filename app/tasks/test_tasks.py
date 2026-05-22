from app.tasks.celery_app import celery

@celery.task
def test_task():
    print("Worker executed task")
    return "worker alive"
