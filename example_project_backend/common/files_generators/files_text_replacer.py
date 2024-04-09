import os
import re

from common.files_generators.paths_manager import PathsManager


class FilesTextReplacer:
    def __init__(self):
        self.paths_manager = PathsManager()

    def replace_text(self, full_path: str, replace_dict: dict[str, str]) -> None:
        with open(full_path) as f:
            s = f.read()
        for old_text, new_text in replace_dict.items():
            s = s.replace(old_text, new_text)
        with open(full_path, "w") as f:
            f.write(s)

    def replace_text_in_directory(self, directory_full_path: str, replace_dict: dict[str, str]) -> None:
        for root, _, files_names in os.walk(directory_full_path):
            for file_name in files_names:
                file_full_path = os.path.join(root, file_name)
                self.replace_text(file_full_path, replace_dict)
                new_file_name = file_name
                for old_text, new_text in replace_dict.items():
                    new_file_name = new_file_name.replace(old_text, new_text)
                if new_file_name != file_name:
                    os.rename(file_full_path, os.path.join(root, new_file_name))

    def replace_text_in_relative_django(self, relative_path, replace_dict: dict[str, str]) -> None:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        self.replace_text(full_path, replace_dict)

    def replace_text_in_relative_new_generated_ts(self, relative_path, replace_dict: dict[str, str]) -> None:
        full_path = os.path.join(self.paths_manager.get_new_generated_ts_path(), relative_path)
        self.replace_text(full_path, replace_dict)

    def replace_text_in_relative_django_directory(self, relative_path, replace_dict: dict[str, str]) -> None:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        self.replace_text_in_directory(full_path, replace_dict)

    def add_line_to_file(self, full_path: str, line: str) -> None:
        with open(full_path, 'r') as f:
            s = f.read()
        s = s.strip()
        s = f'{s}\n{line}\n'
        with open(full_path, 'w') as f:
            f.write(s)

    def add_line_to_file_in_relative_django(self, relative_path, line: str) -> None:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        self.add_line_to_file(full_path, line)

    def add_line_to_file_in_relative_new_generated_ts(self, relative_path, line: str) -> None:
        full_path = os.path.join(self.paths_manager.get_new_generated_ts_path(), relative_path)
        self.add_line_to_file(full_path, line)
