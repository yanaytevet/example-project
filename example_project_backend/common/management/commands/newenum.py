from django.core.management.base import BaseCommand, CommandParser

from common.files_generators.django_files_creator import DjangoFilesCreator


class Command(BaseCommand):
    help = 'Creates a new enum'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('enum_class_name', type=str)
        parser.add_argument('enum_file_path', type=str, nargs='?', default=None)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        enum_class_name = options['enum_class_name']
        enum_file_path = options['enum_file_path']
        DjangoFilesCreator().create_enum_file(app_name, enum_class_name, enum_file_path)
