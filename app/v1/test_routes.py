from fastapi import APIRouter
from app.tasks.test_tasks import test_task

router = APIRouter()

@router.post("/test-task")
def trigger_task():
    test_task.delay()
    return {"message": "task queued"}