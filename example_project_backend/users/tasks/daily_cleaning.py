from example_project_backend import celery
from example_project_backend.celery import AsyncTask


@celery.app.task(base=AsyncTask, queue=celery.X_QUEUE_NAME)
def daily_cleaning() -> None:
    pass
