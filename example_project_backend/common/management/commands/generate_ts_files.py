import json
import os
import shutil
import typing
from typing import Iterable, get_type_hints, TypedDict

from django.conf import settings
from django.core.management.base import BaseCommand

from common.base_choices import BaseChoices
from common.classes_loaders.modules_loader import ModulesLoader
from common.simple_rest.serializers.serializer import Serializer
from common.string_utils import StringUtils
from common.type_utils import TypeUtils


class Command(BaseCommand):
    help = 'Generates ts files for the api'

    CONSTS = 'consts'
    ENUMS = 'enums'
    ENUM_TEMPLATE = """
import {{ z }} from "zod"

export const Z{name} = z.enum({values});

export type {name} = z.infer<typeof Z{name}>;

    """

    SERIALIZERS = 'serializers'
    INTERFACES = 'interfaces'

    def __init__(self):
        super().__init__()
        app_files = os.path.realpath(os.path.join(settings.BASE_DIR, '..', settings.FRONT_DIR_NAME, 'src', 'app'))
        self.new_generated_files = os.path.join(app_files, 'new-generated-files')
        self.generated_files = os.path.join(app_files, 'generated-files')
        self.class_to_ts_import = {}
        self.interface_to_ts_import = {}

    def handle(self, *args, **options) -> None:
        self.clear_new_generated()
        self.create_enums()
        self.create_interfaces()
        self.move_new_generated_to_generated()

    def clear_new_generated(self) -> None:
        if os.path.exists(self.new_generated_files):
            shutil.rmtree(self.new_generated_files)
        os.mkdir(self.new_generated_files)

    def create_enums(self) -> None:
        for app_name in self.get_all_apps_containing_directory(self.CONSTS):
            self.create_enums_in_app_as_ts_files(app_name)

    def get_all_apps_containing_directory(self, directory_name: str) -> Iterable[str]:
        for app_name in settings.INSTALLED_APPS:
            directory_path = os.path.join(settings.BASE_DIR, app_name, directory_name)
            if os.path.exists(directory_path):
                yield app_name

    def move_new_generated_to_generated(self) -> None:
        if os.path.exists(self.generated_files):
            shutil.rmtree(self.generated_files)
        shutil.move(self.new_generated_files, self.generated_files)

    def create_enums_in_app_as_ts_files(self, app_name: str) -> None:
        consts_path = os.path.join(settings.BASE_DIR, app_name, self.CONSTS)
        for klass, partial_path in self.get_all_classes_in_app(consts_path, BaseChoices):
            klass: type[BaseChoices]
            ts_partial_path = self.get_ts_path(partial_path)
            ts_import_path = os.path.join(self.ENUMS, app_name, ts_partial_path)[:-3]
            ts_full_path = os.path.join(self.new_generated_files, self.ENUMS, app_name, ts_partial_path)
            self.class_to_ts_import[klass.__name__] = ts_import_path
            self.create_ts_file_for_enum(klass, ts_full_path)

    def get_all_classes_in_app(self, dir_path: str, base_klass: type) -> Iterable[tuple[type, str]]:
        for klass, path in ModulesLoader().get_all_classes_and_path_from_directory(dir_path):
            if issubclass(klass, base_klass):
                partial_path = path.split(dir_path)[-1][1:]
                yield klass, partial_path

    def get_ts_path(self, partial_path: str) -> str:
        return partial_path.replace('_', '-').replace('.py', '.ts')

    def create_ts_file_for_enum(self, klass: type[BaseChoices], ts_full_path: str) -> None:
        values = klass.get_list()
        values_str = json.dumps(values)
        ts_content = self.ENUM_TEMPLATE.format(name=klass.__name__, values=values_str)
        self.create_dir_for_file(ts_full_path)
        with open(ts_full_path, 'w+') as f:
            f.write(ts_content)

    def create_dir_for_file(self, ts_full_path: str) -> None:
        dir_path = os.path.dirname(ts_full_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def create_interfaces(self) -> None:
        for app_name in self.get_all_apps_containing_directory(self.SERIALIZERS):
            self.create_interfaces_in_app_as_ts_files(app_name)
        for z_class, partial_path in self.interface_to_ts_import.items():
            self.replace_z_imports_in_ts_files(z_class, partial_path)

    def create_interfaces_in_app_as_ts_files(self, app_name: str) -> None:
        consts_path = os.path.join(settings.BASE_DIR, app_name, self.SERIALIZERS)
        for serializer_class, partial_path in self.get_all_classes_in_app(consts_path, Serializer):
            serializer_class: type[Serializer]
            type_hints = get_type_hints(serializer_class.inner_serialize)
            return_type = type_hints.get('return')
            if TypeUtils.is_typeddict(return_type):
                self.create_ts_file_for_interface(serializer_class, return_type, partial_path, app_name)

    def create_ts_file_for_interface(self, serializer_class: type[Serializer], return_type: type[TypedDict],
                                     serializer_partial_path: str, app_name: str) -> None:
        ts_class_name = serializer_class.__name__
        if ts_class_name.endswith('Serializer'):
            ts_class_name = ts_class_name.split('Serializer')[0]
        if serializer_partial_path.endswith('_serializer.py'):
            serializer_partial_path = serializer_partial_path.replace('_serializer.py', '.py')
        ts_partial_path = self.get_ts_path(serializer_partial_path)
        self.interface_to_ts_import[f'PATH_Z{ts_class_name}'] = os.path.join(app_name, ts_partial_path)[:-3]
        ts_full_path = os.path.join(self.new_generated_files, self.INTERFACES, app_name, ts_partial_path)

        imports_arr = []
        fields_arr = []

        for field_name, field_type in return_type.__annotations__.items():
            ts_field_type_str = self.get_field_zod_type(field_type)
            depth = serializer_partial_path.count('/') + 2
            ts_field_type_import_str = self.get_field_ts_type_import(ts_field_type_str, field_type, depth)
            ts_field_name = self.get_field_ts_name(field_name)
            fields_arr.append(f'  {ts_field_name}: {ts_field_type_str},')
            if ts_field_type_import_str:
                imports_arr.append(ts_field_type_import_str)

        imports = 'import {z} from "zod"\n' + '\n'.join(imports_arr)
        interface_name_line = f'export const Z{ts_class_name} = z.object( {{'
        interface_content = '\n'.join(fields_arr)
        export_line = f'export type {ts_class_name} = z.infer<typeof Z{ts_class_name}>;'

        ts_content = f'{imports}\n\n{interface_name_line}\n{interface_content}\n}});\n\n{export_line}'

        self.create_dir_for_file(ts_full_path)
        with open(ts_full_path, 'w+') as f:
            f.write(ts_content)

    def get_field_zod_type(self, field_type: type) -> str:
        if field_type == str:
            return 'z.string()'
        if field_type == int or field_type == float:
            return 'z.number()'
        if field_type == bool:
            return 'z.boolean()'
        if issubclass(field_type, BaseChoices):
            return 'Z' + field_type.__name__
        if typing.get_origin(field_type) == list:
            type_a = self.get_field_zod_type(typing.get_args(field_type)[0])
            return f'z.array({type_a})'
        if typing.get_origin(field_type) == dict:
            type_args = typing.get_args(field_type)
            type_a = self.get_field_zod_type(type_args[0])
            type_b = self.get_field_zod_type(type_args[1])
            return f'z.record({type_a}, {type_b})'
        if TypeUtils.is_typeddict(field_type):
            ts_class_name = field_type.__name__
            if ts_class_name.endswith('SerializerOutput'):
                ts_class_name = ts_class_name.split('SerializerOutput')[0]
            return f'Z{ts_class_name}'
        return ''

    def get_field_ts_type_import(self, ts_field_type_str: str, field_type: type, depth: int) -> str | None:
        if issubclass(field_type, BaseChoices):
            dots = '../' * depth
            if dots == '':
                dots = './'
            path = self.class_to_ts_import.get(field_type.__name__)
            if not path:
                return None
            return f'import {{ {ts_field_type_str} }} from "{dots}{path}"'
        if TypeUtils.is_typeddict(field_type):
            if depth <= 1:
                dots = './'
            else:
                dots = '../' * (depth - 1)
            return f'import {{ {ts_field_type_str} }} from "{dots}<PATH_{ts_field_type_str}>"'
        return None

    def get_field_ts_name(self, field_name: str) -> str:
        return StringUtils.lower_case_to_title_case(field_name)

    def replace_z_imports_in_ts_files(self, z_class: str, partial_path: str) -> None:
        for path, dirs, files in os.walk(self.new_generated_files):
            for filename in files:
                filepath = os.path.join(path, filename)
                if filepath.endswith('.ts'):
                    with open(filepath) as f:
                        s = f.read()
                    s = s.replace(f'<{z_class}>', self.interface_to_ts_import[z_class])
                    with open(filepath, "w") as f:
                        f.write(s)
