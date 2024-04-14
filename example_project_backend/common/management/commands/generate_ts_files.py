from django.core.management.base import BaseCommand

from common.files_generators.ts_files_creator import TsFilesCreator


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        TsFilesCreator().create_all()
