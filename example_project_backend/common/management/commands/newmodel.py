from django.core.management.base import BaseCommand, CommandParser

from common.files_generators.django_files_creator import DjangoFilesCreator


class Command(BaseCommand):
    help = 'Creates a new model'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_class_name', type=str)
        parser.add_argument('model_file_name', type=str, nargs='?', default=None)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        model_class_name = options['model_class_name']
        model_file_name = options['model_file_name']
        DjangoFilesCreator().create_model_file(app_name, model_class_name, model_file_name)