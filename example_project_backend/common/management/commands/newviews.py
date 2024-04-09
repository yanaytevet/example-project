from django.core.management.base import BaseCommand, CommandParser

from common.files_generators.django_files_creator import DjangoFilesCreator


class Command(BaseCommand):
    help = 'Create some new views...'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_name', type=str)
        parser.add_argument('name_suffix', type=str, nargs='?', default=None)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        model_name = options['model_name']
        name_suffix = options['name_suffix']
        DjangoFilesCreator().create_views(app_name, model_name, name_suffix)
