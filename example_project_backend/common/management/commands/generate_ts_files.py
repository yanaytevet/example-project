from django.core.management.base import BaseCommand

from common.files_generators.ts_files_creator import TsFilesCreator


class Command(BaseCommand):
    """
    In [1]: from django.urls import get_resolver; res = get_resolver().url_patterns[-1]; g = res.url_patterns[0].callback.v
   ...: iew_class

In [2]: g
Out[2]: common.simple_rest.async_views.async_compose_api_views.async_compose_api_views.<locals>.AsyncComposedAPIView
    """

    def handle(self, *args, **options) -> None:
        TsFilesCreator().create_all()
