from django.core.management.base import BaseCommand, CommandParser

from common.files_generators.django_files_creator import DjangoFilesCreator


class Command(BaseCommand):
    help = 'Create a new query filter'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_name', type=str)
        parser.add_argument('action_name', type=str)
        parser.add_argument('action_file_path', type=str, nargs='?', default=None)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        model_name = options['model_name']
        action_name = options['action_name']
        action_file_path = options['action_file_path']
        DjangoFilesCreator().create_item_action_file(app_name, model_name, action_name, action_file_path)
