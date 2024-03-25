from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = 'Create a new model'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options) -> None:
        app_name = options['app_name']
        model_name = options['model_name']
