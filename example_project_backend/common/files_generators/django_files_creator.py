import os.path

from django.core.management import call_command

from common.files_generators.directories_creator import DirectoriesCreator
from common.files_generators.files_copier import FilesCopier
from common.files_generators.files_text_replacer import FilesTextReplacer
from common.files_generators.paths_manager import PathsManager
from common.string_utils import StringUtils


class DjangoFilesCreator:
    INIT_FILE = '__init__.py'

    ENUMS_DIRECTORY = 'enums'
    ENUM_EXAMPLE_FILE_PATH = 'example_enum.py'

    MODELS_DIRECTORY = 'models'
    MODEL_EXAMPLE_FILE_PATH = 'example_model.py'

    ITEM_ACTIONS_DIRECTORY = 'item_actions'
    ITEM_ACTION_EXAMPLE_FILE_PATH = 'example_item_action.py'

    QUERY_FILTERS_DIRECTORY = 'query_filters'
    QUERY_FILTER_EXAMPLE_FILE_PATH = 'example_query_filter.py'

    SERIALIZERS_DIRECTORY = 'serializers'
    SERIALIZER_EXAMPLE_FILE_PATH = 'example_serializer.py'

    APP_URL_FILE = 'urls.py'
    URL_EXAMPLE_FILE_PATH = 'example_urls.py'

    ADMIN_EXAMPLE_FILE_PATH = 'example_admin.py'
    ADMIN_FILE = 'admin.py'

    TESTS_DIRECTORY = 'tests'
    VIEWS_DIRECTORY = 'views'
    TASKS_DIRECTORY = 'tasks'
    PERMISSIONS_CHECKERS_DIRECTORY = 'permissions_checkers'

    FILES_TO_REMOVE_ON_CREATE_APP = ['tests.py', 'views.py', 'models.py', ADMIN_FILE]
    DIRECTORIES_TO_CREATE_ON_CREATE_APP = [ENUMS_DIRECTORY, MODELS_DIRECTORY, ITEM_ACTIONS_DIRECTORY,
                                           QUERY_FILTERS_DIRECTORY, SERIALIZERS_DIRECTORY, TESTS_DIRECTORY,
                                           VIEWS_DIRECTORY, TASKS_DIRECTORY, PERMISSIONS_CHECKERS_DIRECTORY]

    def __init__(self):
        self.directories_creator = DirectoriesCreator()
        self.files_copier = FilesCopier()
        self.files_text_replacer = FilesTextReplacer()
        self.paths_manager = PathsManager()

    def exit_if_app_doesnt_exist(self, app_name: str) -> bool:
        if not self.directories_creator.does_app_exists(app_name):
            print(f"app {app_name} doesn't exist")
            return True
        return False

    def create_app(self, app_name: str) -> None:
        if self.directories_creator.does_app_exists(app_name):
            print(f"app {app_name} already exists")
            return
        call_command('startapp', app_name)
        self.init_app_urls(app_name)
        self.init_app_settings(app_name)
        for file_name in self.FILES_TO_REMOVE_ON_CREATE_APP:
            self.files_copier.remove_relative_django(f'{app_name}/{file_name}')
        for dir_name in self.DIRECTORIES_TO_CREATE_ON_CREATE_APP:
            self.directories_creator.create_django_directory_path(f'{app_name}/{dir_name}')
        admin_file_path = f'{app_name}/{self.ADMIN_FILE}'
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.ADMIN_EXAMPLE_FILE_PATH, admin_file_path, should_override=True)
        self.files_text_replacer.replace_text_in_relative_django(admin_file_path, {
            'example_app': app_name,
        })

    def init_app_urls(self, app_name: str) -> None:
        urls_relative_path = os.path.join(app_name, self.APP_URL_FILE)
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.URL_EXAMPLE_FILE_PATH, urls_relative_path, should_override=True)
        general_urls_relative_path = self.paths_manager.get_django_project_general_urls_relative_path()
        app_url = app_name.replace('_', '-')
        url_file_line = f"    path(r'api/{app_url}/', include('{app_name}.urls')),\n]"
        self.files_text_replacer.replace_text_in_relative_django(general_urls_relative_path,
                                                                 {']': url_file_line})

    def init_app_settings(self, app_name: str) -> None:
        installed_apps_relative_path = self.paths_manager.get_django_project_general_installed_apps()
        url_file_line = f"    '{app_name}',\n]"
        self.files_text_replacer.replace_text_in_relative_django(installed_apps_relative_path,
                                                                 {']': url_file_line})

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

    def create_item_action_file(self, app_name: str, model_name: str, action_name: str, action_file_path: str = None
                                ) -> None:
        if self.exit_if_app_doesnt_exist(app_name):
            return
        action_class_name = f'{action_name}{model_name}'
        if action_file_path is None:
            action_name_lower = StringUtils.pascal_case_to_lower_case(action_name)
            model_name_lower = StringUtils.pascal_case_to_lower_case(model_name)
            lower_case_name = f'{action_name_lower}_{model_name_lower}_item_action'
            model_item_actions_directory_name = f'{model_name_lower}s_item_actions'
            action_file_relative_path = os.path.join(app_name, self.ITEM_ACTIONS_DIRECTORY,
                                                     model_item_actions_directory_name, f'{lower_case_name}.py')
        else:
            action_file_relative_path = os.path.join(app_name, self.ITEM_ACTIONS_DIRECTORY, action_file_path)
        actions_relative_path = os.path.split(action_file_relative_path)[0]
        self.directories_creator.create_django_directory_path(actions_relative_path)
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.ITEM_ACTION_EXAMPLE_FILE_PATH, action_file_relative_path, should_override=False)
        self.files_text_replacer.replace_text_in_relative_django(action_file_relative_path, {
            'ExampleModel': model_name,
            'ExampleActionModel': action_class_name,
            'example_app': app_name,
        })

    def create_query_filter_file(self, app_name: str, model_name: str, filter_name: str, filter_file_path: str = None
                                 ) -> None:
        if self.exit_if_app_doesnt_exist(app_name):
            return
        filter_class_name = f'{filter_name}{model_name}'
        if filter_file_path is None:
            filter_name_lower = StringUtils.pascal_case_to_lower_case(filter_name)
            model_name_lower = StringUtils.pascal_case_to_lower_case(model_name)
            lower_case_name = f'{filter_name_lower}_{model_name_lower}_query_filter'
            model_query_filters_directory_name = f'{model_name_lower}s_query_filters'
            filter_file_relative_path = os.path.join(app_name, self.QUERY_FILTERS_DIRECTORY,
                                                     model_query_filters_directory_name, f'{lower_case_name}.py')
        else:
            filter_file_relative_path = os.path.join(app_name, self.QUERY_FILTERS_DIRECTORY, filter_file_path)
        filters_relative_path = os.path.split(filter_file_relative_path)[0]
        self.directories_creator.create_django_directory_path(filters_relative_path)
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.QUERY_FILTER_EXAMPLE_FILE_PATH, filter_file_relative_path, should_override=False)
        self.files_text_replacer.replace_text_in_relative_django(filter_file_relative_path, {
            'ExampleModel': model_name,
            'ExampleFilterModel': filter_class_name,
            'example_app': app_name,
        })

    def create_serializer_file(self, app_name: str, model_name: str, serializer_name_prefix: str = None,
                               serializer_name_suffix: str = None,
                               serializer_file_path: str = None):
        if self.exit_if_app_doesnt_exist(app_name):
            return
        if serializer_name_prefix is None:
            serializer_name_prefix = 'Full'
        serializer_class_name = f'{serializer_name_prefix}{model_name}{serializer_name_suffix or ""}'
        if serializer_file_path is None:
            serializer_name_prefix_lower = StringUtils.pascal_case_to_lower_case(serializer_name_prefix)
            serializer_name_suffix_lower = ''
            if serializer_name_suffix:
                serializer_name_suffix_lower = f'_{StringUtils.pascal_case_to_lower_case(serializer_name_suffix)}'
            model_name_lower = StringUtils.pascal_case_to_lower_case(model_name)
            lower_case_name = (f'{serializer_name_prefix_lower}_{model_name_lower}'
                               f'{serializer_name_suffix_lower}_serializer')
            model_query_filters_directory_name = f'{model_name_lower}s_serializers'
            serializer_file_relative_path = os.path.join(app_name, self.SERIALIZERS_DIRECTORY,
                                                         model_query_filters_directory_name, f'{lower_case_name}.py')
        else:
            serializer_file_relative_path = os.path.join(app_name, self.SERIALIZERS_DIRECTORY, serializer_file_path)
        serializers_relative_path = os.path.split(serializer_file_relative_path)[0]
        self.directories_creator.create_django_directory_path(serializers_relative_path)
        self.files_copier.copy_template_file_or_directory_to_relative_django(
            self.SERIALIZER_EXAMPLE_FILE_PATH, serializer_file_relative_path, should_override=False)
        self.files_text_replacer.replace_text_in_relative_django(serializer_file_relative_path, {
            'ExampleModel': model_name,
            'ExampleName': serializer_class_name,
            'example_app': app_name,
        })
