import os

from django.conf import settings


class PathsManager:
    TS_NEW_GENERATED = 'new-generated-files'
    TS_GENERATED = 'generated-files'

    def get_ts_app_path(self) -> str:
        return os.path.realpath(os.path.join(settings.BASE_DIR, '..', settings.FRONT_DIR_NAME))

    def get_new_generated_ts_path(self) -> str:
        app_files = self.get_ts_app_path()
        return os.path.join(app_files, self.TS_NEW_GENERATED)

    def get_generated_ts_path(self) -> str:
        app_files = self.get_ts_app_path()
        return os.path.join(app_files, self.TS_GENERATED)

    def get_django_base_path(self) -> str:
        return settings.BASE_DIR

    def get_django_templates_directory(self) -> str:
        return os.path.join(self.get_django_base_path(), 'common', 'files_generators', 'data')

    def get_django_project_general_urls_relative_path(self) -> str:
        return settings.ROOT_URLCONF.replace('.', '/') + '.py'

    def get_django_project_general_installed_apps(self) -> str:
        urls_path = self.get_django_project_general_urls_relative_path()
        return urls_path.replace('urls.py', 'installed_apps.py')
