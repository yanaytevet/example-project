import os
from typing import Iterable

from common.classes_loaders.modules_loader import ModulesLoader
from common.files_generators.paths_manager import PathsManager


class ClassesFinder:
    def __init__(self):
        self.paths_manager = PathsManager()

    def find_all_classes_in_relative_django(self, relative_path: str, base_klass: type) -> Iterable[tuple[type, str]]:
        full_path = os.path.join(self.paths_manager.get_django_base_path(), relative_path)
        for klass, relative_path in ModulesLoader().get_all_classes_and_path_from_directory(full_path):
            if issubclass(klass, base_klass):
                partial_path = relative_path.split(full_path)[-1][1:]
                yield klass, partial_path
