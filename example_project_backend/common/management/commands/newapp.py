from django.core.management.base import BaseCommand, CommandParser

from common.files_generators.django_files_creator import DjangoFilesCreator


class Command(BaseCommand):
    help = 'Create a new app, but with more...'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        DjangoFilesCreator().create_app(app_name)
