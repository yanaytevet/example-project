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
        if os.path.exists(full_path) and should_override:
            print(f'Path {full_path} already exists. Overriding...')
            shutil.rmtree(full_path)
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

    def remove_relative_django(self, relative_path: str) -> None:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        os.remove(full_path)

    def remove_relative_new_generated_ts(self, relative_path: str) -> None:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        os.remove(full_path)

    def create_file_with_content(self, full_path: str, content: str, should_override: bool = False) -> None:
        if os.path.exists(full_path) and not should_override:
            print(f'Path {full_path} already exists. Skipping...')
            return
        if os.path.exists(full_path) and should_override:
            print(f'Path {full_path} already exists. Overriding...')
            shutil.rmtree(full_path)
        print(f'setting content to {full_path}')
        with open(full_path, 'w') as file:
            file.write(content)

    def create_file_with_content_in_relative_new_generated_ts(self, relative_path: str, content: str) -> None:
        full_path = os.path.join(self.paths_manager.get_new_generated_ts_path(), relative_path)
        self.create_file_with_content(full_path, content)
