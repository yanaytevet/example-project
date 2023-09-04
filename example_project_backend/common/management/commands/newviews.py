import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = 'Create some new views...'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.app_name: str = ''
        self.model_name_lower: str = ''
        self.model_name_camel: str = ''

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('app_name', type=str)
        parser.add_argument('model_name_lower', type=str)
        parser.add_argument('model_name_camel', type=str)
        parser.add_argument('skip_views', type=bool, default=False)

    def handle(self, *args, **options) -> None:
        self.app_name = options['app_name']
        self.model_name_lower = options['model_name_lower']
        self.model_name_camel = options['model_name_camel']
        self.create_serializers_package()
        if options['skip_views']:
            print('Skipping views creation...')
        else:
            self.create_views_package()

    def create_serializers_package(self) -> None:
        serializers_dir_name = f'{self.model_name_lower}s_serializers'

        data_path = os.path.join(settings.BASE_DIR, 'common', 'management', 'data', 'example_serializers')
        serializers_path = os.path.join(settings.BASE_DIR, self.app_name, 'serializers', serializers_dir_name)
        self.copy_data_directory_and_replace_texts(data_path, serializers_path)

    def create_views_package(self):
        views_dir_name = f'{self.model_name_lower}s_views'
        data_path = os.path.join(settings.BASE_DIR, 'common', 'management', 'data', 'example_views')
        serializers_path = os.path.join(settings.BASE_DIR, self.app_name, 'views', views_dir_name)
        self.copy_data_directory_and_replace_texts(data_path, serializers_path)

    def copy_data_directory_and_replace_texts(self, data_path: str, target_path: str) -> None:
        if os.path.exists(target_path):
            print(f'Path {target_path} already exists. Skipping...')
            return
        print(f'Copying {data_path} to {target_path}')
        shutil.copytree(data_path, target_path)
        self.replace_texts_in_files_names(target_path)
        self.replace_texts_in_files_content(target_path)

    def replace_texts_in_files_names(self, path: str) -> None:
        for root, dirs, files in os.walk(path):
            for name in files:
                full_current_file_path = os.path.join(root, name)
                new_name = self.fix_text(name)
                full_new_file_path = os.path.join(root, new_name)
                shutil.move(full_current_file_path, full_new_file_path)

    def fix_text(self, text: str) -> str:
        return (text.replace('example_model', self.model_name_lower)
                .replace('ExampleModel', self.model_name_camel)
                .replace('example_app', self.app_name))

    def replace_texts_in_files_content(self, path) -> None:
        for root, dirs, files in os.walk(path):
            for name in files:
                full_current_file_path = os.path.join(root, name)
                with open(full_current_file_path, 'r') as f:
                    content = f.read()
                    new_content = self.fix_text(content)
                with open(full_current_file_path, 'w') as f:
                    f.write(new_content)
