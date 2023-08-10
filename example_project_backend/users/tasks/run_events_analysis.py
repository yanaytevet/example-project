from configurations.managers.user_events_analyzer import UserEventsAnalyzer
from configurations.models import UsersEventsConfigurations
from users.models import UserEvent
from example_project_backend import celery
from example_project_backend.celery import AsyncTask


@celery.app.task(base=AsyncTask, queue=celery.EVENTS_QUEUE_NAME)
def run_events_analysis(event_id: int) -> None:
    if not event_id:
        return
    conf = UsersEventsConfigurations.get()
    if not conf.should_analyze_events:
        return
    event = UserEvent.objects.get(id=event_id)
    UserEventsAnalyzer(conf.events_analysis_params).analyze(event)
