import os
import shutil

from common.files_generators.paths_manager import PathsManager


class FilesCopier:
    PYTHON_INIT_FILE_NAME = '__init__.py'

    def __init__(self):
        self.paths_manager = PathsManager()

    def create_django_init_file(self, full_path: str, should_override: bool = False) -> None:
        init_full_path = os.path.join(full_path, self.PYTHON_INIT_FILE_NAME)
        if os.path.exists(init_full_path) and not should_override:
            return
        open(init_full_path, 'w+').close()

    def copy_template_file_or_directory(self, template_relative_path: str, full_path: str,
                                        should_override: bool = False) -> None:
        if os.path.exists(full_path) and not should_override:
            print(f'Path {full_path} already exists. Skipping...')
            return
        print(f'Copying {template_relative_path} to {full_path}')
        template_full_path = os.path.join(self.paths_manager.get_django_templates_directory(), template_relative_path)
        if os.path.isfile(template_full_path):
            shutil.copyfile(template_full_path, full_path)
        else:
            shutil.copytree(template_full_path, full_path)

    def copy_template_file_or_directory_to_relative_django(self, template_relative_path: str, relative_path: str,
                                                           should_override: bool = False) -> None:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        self.copy_template_file_or_directory(template_relative_path, full_path, should_override)

    def copy_template_file_or_directory_to_relative_new_generated_ts(
            self, template_relative_path: str, relative_path: str, should_override: bool = False) -> None:
        full_path = os.path.join(self.paths_manager.get_new_generated_ts_path(), relative_path)
        self.copy_template_file_or_directory(template_relative_path, full_path, should_override)
