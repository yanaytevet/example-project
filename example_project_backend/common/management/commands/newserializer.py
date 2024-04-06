from django.core.management.base import BaseCommand, CommandParser

from common.files_generators.django_files_creator import DjangoFilesCreator


class Command(BaseCommand):
    help = 'Create a new serializer'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_name', type=str)
        parser.add_argument('serializer_name_prefix', type=str)
        parser.add_argument('serializer_name_suffix', type=str, nargs='?', default=None)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        model_name = options['model_name']
        serializer_name_prefix = options['serializer_name_prefix']
        serializer_name_suffix = options['serializer_name_suffix']
        DjangoFilesCreator().create_serializer_file(app_name, model_name, serializer_name_prefix,
                                                    serializer_name_suffix)
