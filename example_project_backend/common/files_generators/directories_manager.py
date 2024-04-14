import os
import shutil
from typing import Iterable

from django.conf import settings

from common.files_generators.files_copier import FilesCopier
from common.files_generators.paths_manager import PathsManager


class DirectoriesManager:
    def __init__(self):
        self.paths_manager = PathsManager()

    def does_app_exists(self, app_name: str) -> bool:
        app_full_path = os.path.join(self.paths_manager.get_django_base_path(), app_name)
        return os.path.exists(app_full_path)

    def clear_new_generated_ts_directory(self) -> None:
        new_generated_files = self.paths_manager.get_new_generated_ts_path()
        if os.path.exists(new_generated_files):
            shutil.rmtree(new_generated_files)
        self.create_empty_directory(new_generated_files)

    def move_new_generated_to_generated(self) -> None:
        new_generated_files = self.paths_manager.get_new_generated_ts_path()
        generated_files = self.paths_manager.get_generated_ts_path()
        if os.path.exists(generated_files):
            shutil.rmtree(generated_files)
        shutil.move(new_generated_files, generated_files)

    def create_new_generated_ts_directory_sub_directory(self, relative_path: str) -> None:
        directory_full_path = os.path.join(self.paths_manager.get_new_generated_ts_path(), relative_path)
        self.create_empty_directory(directory_full_path)

    def replace_new_generated_ts_directory_with_existing(self) -> None:
        generated_files = self.paths_manager.get_generated_ts_path()
        new_generated_files = self.paths_manager.get_new_generated_ts_path()
        if os.path.exists(generated_files):
            shutil.rmtree(generated_files)
        shutil.move(new_generated_files, generated_files)

    def create_django_directory_path(self, relative_path: str) -> None:
        directory_full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        self.create_empty_directory(directory_full_path)
        temp_dir = directory_full_path
        while temp_dir != '/':
            FilesCopier().create_django_init_file(temp_dir, should_override=False)
            temp_dir = os.path.split(temp_dir)[0]

    def create_empty_directory(self, full_path: str) -> None:
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    def get_all_django_apps_containing_directory(self, directory_name: str) -> Iterable[str]:
        for app_name in settings.INSTALLED_APPS:
            directory_path = os.path.join(settings.BASE_DIR, app_name, directory_name)
            if os.path.exists(directory_path):
                yield app_name
