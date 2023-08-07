from configurations.models import RemindersConfigurations
from users.managers.events_analyzer import EventsAnalyzer
from users.models import UserEvent
from xperiti_backend import celery
from xperiti_backend.celery import AsyncTask


@celery.app.task(base=AsyncTask, queue=celery.EVENTS_QUEUE_NAME)
def run_events_analysis(event_id: int) -> None:
    if not event_id:
        return
    conf = RemindersConfigurations.get()
    if not conf.analyze_events:
        return
    event = UserEvent.objects.get(id=event_id)
    EventsAnalyzer(event, conf.events_to_notify).run()
