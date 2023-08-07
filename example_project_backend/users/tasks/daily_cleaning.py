from configurations.manager.latest_tags_updater import LatestTagsUpdater
from emails.manager.bad_emails_cleaner import BadEmailsCleaner
from emails.manager.emails_histories_cleaner import EmailsHistoriesCleaner
from experts.managers.projects_manager.projects_cleaner import ProjectsCleaner
from experts.managers.sub_projects_managers.sub_projects_cleaner import SubProjectsCleaner
from external.storage.tmp_directory_cleaner import TmpDirectoryCleaner
from operations_tasks.managers.operation_tasks_solver import OperationsTasksSolver
from users.managers.organization_subscriptions_manager import OrganizationSubscriptionsManager
from xperiti_backend import celery
from xperiti_backend.celery import AsyncTask


@celery.app.task(base=AsyncTask, queue=celery.SEARCHERS_QUEUE_NAME)
def daily_cleaning() -> None:
    SubProjectsCleaner.clean()
    ProjectsCleaner.clean()
    EmailsHistoriesCleaner.clean()
    LatestTagsUpdater().update()
    OrganizationSubscriptionsManager.check_notify_analysts_for_all()
    OperationsTasksSolver().resolve_all_old_tasks()
    BadEmailsCleaner().clean()
    TmpDirectoryCleaner().clean()
