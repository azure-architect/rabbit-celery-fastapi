"""
Celery application configuration and setup
"""
from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "rabbit-celery-fastapi",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks"]  # Import task modules
)

# Configure Celery
celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=True,
    
    # Task routing
    task_routes={
        "app.tasks.*": {"queue": "default"},
    },
    
    # Task execution settings
    task_always_eager=False,  # Set to True for testing
    task_eager_propagates=True,
    task_ignore_result=False,
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Beat scheduler settings (for periodic tasks)
    beat_schedule={
        # Example periodic task
        # "example-periodic-task": {
        #     "task": "app.tasks.example_task",
        #     "schedule": 30.0,  # Run every 30 seconds
        # },
    },
)

# Auto-discover tasks from installed apps
celery_app.autodiscover_tasks(["app.tasks"])

if __name__ == "__main__":
    celery_app.start()
