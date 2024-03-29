import os.path

from common.files_generators.directories_creator import DirectoriesCreator
from common.files_generators.files_copier import FilesCopier
from common.files_generators.files_text_replacer import FilesTextReplacer
from common.string_utils import StringUtils


class DjangoFilesCreator:
    INIT_FILE = '__init__.py'

    ENUMS_DIRECTORY = 'enums'
    ENUM_EXAMPLE_FILE_PATH = 'example_enum.py'

    MODELS_DIRECTORY = 'models'
    MODEL_EXAMPLE_FILE_PATH = 'example_model.py'

    def __init__(self):
        self.directories_creator = DirectoriesCreator()
        self.files_copier = FilesCopier()
        self.files_text_replacer = FilesTextReplacer()

    def exit_if_app_doesnt_exist(self, app_name: str) -> bool:
        if not self.directories_creator.does_app_exists(app_name):
            print(f"app {app_name} doesn't exist")
            return True
        return False

    def create_enums_directory(self, app_name: str) -> None:
        if self.exit_if_app_doesnt_exist(app_name):
            return
        enums_relative_path = os.path.join(app_name, self.ENUMS_DIRECTORY)
        self.directories_creator.create_django_directory_path(enums_relative_path)

    def create_enum_file(self, app_name: str, enum_class_name: str, enum_file_path: str = None) -> None:
        if self.exit_if_app_doesnt_exist(app_name):
            return
        lower_case_enum_name = StringUtils.pascal_case_to_lower_case(enum_class_name)
        if enum_file_path is None:
            enum_file_relative_path = os.path.join(app_name, self.ENUMS_DIRECTORY, f'{lower_case_enum_name}.py')
            enums_relative_path = os.path.join(app_name, self.ENUMS_DIRECTORY)
        else:
            enum_file_relative_path = os.path.join(app_name, self.ENUMS_DIRECTORY, enum_file_path)
            enums_relative_path = os.path.split(enum_file_relative_path)[0]
        self.directories_creator.create_django_directory_path(enums_relative_path)
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.ENUM_EXAMPLE_FILE_PATH, enum_file_relative_path, should_override=False)
        self.files_text_replacer.replace_text_in_relative_django(enum_file_relative_path, {
            'ExampleEnum': enum_class_name,
        })

    def create_models_directory(self, app_name: str) -> None:
        if self.exit_if_app_doesnt_exist(app_name):
            return
        enums_relative_path = os.path.join(app_name, self.MODELS_DIRECTORY)
        self.directories_creator.create_django_directory_path(enums_relative_path)

    def create_model_file(self, app_name: str, model_class_name: str, model_file_name: str = None) -> None:
        if self.exit_if_app_doesnt_exist(app_name):
            return
        if not model_file_name:
            model_file_name = f'{StringUtils.pascal_case_to_lower_case(model_class_name)}.py'
        model_file_name_without_py = model_file_name.replace('.py', '')
        model_file_relative_path = os.path.join(app_name, self.MODELS_DIRECTORY, model_file_name)
        models_relative_path = os.path.join(app_name, self.MODELS_DIRECTORY)
        self.directories_creator.create_django_directory_path(models_relative_path)
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.MODEL_EXAMPLE_FILE_PATH, model_file_relative_path, should_override=False)
        self.files_text_replacer.replace_text_in_relative_django(model_file_relative_path, {
            'ExampleModel': model_class_name,
        })
        init_file_path = os.path.join(models_relative_path, self.INIT_FILE)
        self.files_text_replacer.add_line_to_file_in_relative_django(
            init_file_path, f'from .{model_file_name_without_py} import {model_class_name}')
