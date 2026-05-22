from celery import Celery

celery = Celery("sentinel" , 
                broker = "redis://localhost:6379/0",  
                backend = "redis://localhost:6379/0")

celery.autodiscover_tasks(["app.tasks.test_tasks"])


# broker: where task message go
# backend: wehre should task must be stored 