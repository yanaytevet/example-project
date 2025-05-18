import json
import os
import typing
from typing import get_type_hints, TypedDict

from common.base_enum import BaseEnum
from common.files_generators.classes_finder import ClassesFinder
from common.files_generators.directories_manager import DirectoriesManager
from common.files_generators.django_files_creator import DjangoFilesCreator
from common.files_generators.files_copier import FilesCopier
from common.files_generators.files_text_replacer import FilesTextReplacer
from common.files_generators.paths_manager import PathsManager
from common.files_generators.ts_files_data_holders.interface_ts_file_data_holder import InterfaceTsFileDataHolder
from common.files_generators.ts_files_data_holders.ts_file_data_holder import TsFileDataHolder
from common.simple_api.serializers.serializer import Serializer
from common.type_utils import TypeUtils


class TsFilesCreator:
    ENUM_EXAMPLE_FILE_PATH = 'example_enum.ts'
    ENUMS_DIRECTORY = 'enums'
    INTERFACES_DIRECTORY = 'interfaces'

    INTERFACE_CONTENT = '''import {{z}} from "zod";
{imports_str}

export const Z{class_name} = z.object({{
  {interface_str}
}});

export type {class_name} = z.infer<typeof Z{class_name}>;
'''

    def __init__(self):
        self.directories_manager = DirectoriesManager()
        self.classes_finder = ClassesFinder()
        self.paths_manager = PathsManager()
        self.files_copier = FilesCopier()
        self.files_text_replacer = FilesTextReplacer()

        self.enum_class_name_to_ts_file_data_holder: dict[str, TsFileDataHolder] = {}
        self.interface_class_name_to_ts_file_data_holder: dict[str, InterfaceTsFileDataHolder] = {}

    def create_all(self) -> None:
        self.directories_manager.clear_new_generated_ts_directory()
        self.load_and_create_all_enums()
        self.load_all_serializers()
        self.create_all_serializers()
        self.directories_manager.move_new_generated_to_generated()

    def load_and_create_all_enums(self) -> None:
        for app_name in self.directories_manager.get_all_django_apps_containing_directory(
                DjangoFilesCreator.ENUMS_DIRECTORY):
            self.load_and_create_all_enums_in_app(app_name)

    def load_and_create_all_enums_in_app(self, app_name: str) -> None:
        enums_relative_path = os.path.join(app_name, DjangoFilesCreator.ENUMS_DIRECTORY)
        for klass, partial_path in self.classes_finder.find_all_classes_in_relative_django(enums_relative_path,
                                                                                           BaseEnum):
            klass: type[BaseEnum]
            if klass.__name__ in self.enum_class_name_to_ts_file_data_holder:
                raise ValueError(f'Duplicate enum name: {klass.__name__}')
            ts_partial_path = self.get_ts_path(partial_path)
            ts_relative_path = os.path.join(self.ENUMS_DIRECTORY, app_name, ts_partial_path)
            self.enum_class_name_to_ts_file_data_holder[klass.__name__] = TsFileDataHolder(ts_relative_path, klass.__name__)
            self.create_ts_file_for_enum(klass)

    def get_ts_path(self, partial_path: str) -> str:
        return partial_path.replace('_', '-').replace('.py', '.ts')

    def create_ts_file_for_enum(self, klass: type[BaseEnum]) -> None:
        ts_file_data_holder = self.enum_class_name_to_ts_file_data_holder[klass.__name__]
        values = klass.get_list()
        values_str = json.dumps(values)

        ts_relative_path = ts_file_data_holder.ts_relative_path
        directory_path = os.path.split(ts_relative_path)[0]
        self.directories_manager.create_new_generated_ts_directory_sub_directory(directory_path)
        self.files_copier.copy_template_file_or_directory_to_relative_new_generated_ts(
            self.ENUM_EXAMPLE_FILE_PATH, ts_relative_path, should_override=True)
        self.files_text_replacer.replace_text_in_relative_new_generated_ts(ts_relative_path, {
            'values_json': values_str,
            'enum_name': klass.__name__,
        })

    def load_all_serializers(self) -> None:
        for app_name in self.directories_manager.get_all_django_apps_containing_directory(
                DjangoFilesCreator.SERIALIZERS_DIRECTORY):
            self.load_all_serializers_in_app(app_name)

    def load_all_serializers_in_app(self, app_name: str) -> None:
        serializers_relative_path = os.path.join(app_name, DjangoFilesCreator.SERIALIZERS_DIRECTORY)
        for serializer_class, serializer_partial_path in self.classes_finder.find_all_classes_in_relative_django(
                serializers_relative_path, Serializer):
            serializer_class: type[Serializer]
            type_hints = get_type_hints(serializer_class.inner_serialize)
            return_type = type_hints.get('return')
            if not TypeUtils.is_typeddict(return_type):
                continue
            ts_class_name = self.get_ts_class_name_from_serializer_class(serializer_class)
            if ts_class_name in self.interface_class_name_to_ts_file_data_holder:
                raise ValueError(f'Duplicate serializer name: {ts_class_name}')
            ts_relative_path = self.get_ts_relative_path_from_serializer_partial_path(app_name, serializer_partial_path)
            ts_file_data_holder = InterfaceTsFileDataHolder(ts_relative_path, ts_class_name)
            ts_file_data_holder.set_annotations(return_type.__annotations__.data())
            self.interface_class_name_to_ts_file_data_holder[ts_class_name] = ts_file_data_holder

    def get_ts_class_name_from_serializer_class(self, serializer_class: type[Serializer]) -> str:
        ts_class_name = serializer_class.__name__
        if ts_class_name.endswith('Serializer'):
            ts_class_name = ts_class_name.split('Serializer')[0]
        return ts_class_name

    def get_ts_class_name_from_serializer_output_class(self, serializer_class: type[TypedDict]) -> str:
        ts_class_name = serializer_class.__name__
        if ts_class_name.endswith('SerializerOutput'):
            ts_class_name = ts_class_name.split('SerializerOutput')[0]
        return ts_class_name

    def get_ts_relative_path_from_serializer_partial_path(self, app_name: str, serializer_partial_path: str) -> str:
        if serializer_partial_path.endswith('_serializer.py'):
            serializer_partial_path = serializer_partial_path.replace('_serializer.py', '.py')
        ts_partial_path = self.get_ts_path(serializer_partial_path)
        return os.path.join(self.INTERFACES_DIRECTORY, app_name, ts_partial_path)

    def create_all_serializers(self):
        for ts_file_data_holder in self.interface_class_name_to_ts_file_data_holder.values():
            self.create_interface_ts_file_from_data_holder(ts_file_data_holder)

    def create_interface_ts_file_from_data_holder(self, ts_file_data_holder: InterfaceTsFileDataHolder) -> None:
        content = self.get_interface_content_from_ts_file_data_holder(ts_file_data_holder)
        ts_relative_path = ts_file_data_holder.ts_relative_path
        directory_path = os.path.split(ts_relative_path)[0]
        self.directories_manager.create_new_generated_ts_directory_sub_directory(directory_path)
        self.files_copier.create_file_with_content_in_relative_new_generated_ts(ts_relative_path, content)

    def get_interface_content_from_ts_file_data_holder(self, ts_file_data_holder: InterfaceTsFileDataHolder) -> str:
        return self.INTERFACE_CONTENT.format(
            imports_str=self.get_interface_imports_str(ts_file_data_holder),
            class_name=ts_file_data_holder.class_name,
            interface_str=self.get_interface_content_str(ts_file_data_holder),
        )

    def get_interface_imports_str(self, ts_file_data_holder: InterfaceTsFileDataHolder) -> str:
        imports_strs = []
        for name, field_type in ts_file_data_holder.annotations:
            imports_strs.extend(self.get_imports_strs_from_type(ts_file_data_holder, field_type))
        seen = set()
        imports_strs = [x for x in imports_strs if not (x in seen or seen.add(x))]
        return '\n'.join(imports_strs)

    def get_imports_strs_from_type(self, ts_file_data_holder: InterfaceTsFileDataHolder, field_type: type) -> list[str]:
        imports_strs = []
        if (not TypeUtils.is_typeddict(field_type)) and (not issubclass(field_type, BaseEnum)) and \
                (not typing.get_origin(field_type) in [list, dict]):
            return imports_strs

        if typing.get_origin(field_type) == list:
            return self.get_imports_strs_from_type(ts_file_data_holder, typing.get_args(field_type)[0])
        if typing.get_origin(field_type) == dict:
            return (self.get_imports_strs_from_type(ts_file_data_holder, typing.get_args(field_type)[0]) +
                    self.get_imports_strs_from_type(ts_file_data_holder, typing.get_args(field_type)[1]))

        ts_class_name = self.get_ts_class_name_from_serializer_output_class(field_type)
        other_ts_file_data_holder = None
        if ts_class_name in self.interface_class_name_to_ts_file_data_holder:
            other_ts_file_data_holder = self.interface_class_name_to_ts_file_data_holder[ts_class_name]
        if ts_class_name in self.enum_class_name_to_ts_file_data_holder:
            other_ts_file_data_holder = self.enum_class_name_to_ts_file_data_holder[ts_class_name]
        if other_ts_file_data_holder is None:
            return imports_strs
        relative_path = other_ts_file_data_holder.get_relative_path_from_another_path(
            ts_file_data_holder.ts_relative_path)
        imports_strs.append(f'import {{Z{ts_class_name}}} from "{relative_path}";')
        return imports_strs

    def get_interface_content_str(self, ts_file_data_holder: InterfaceTsFileDataHolder) -> str:
        content_strs = []
        for name, field_type in ts_file_data_holder.annotations:
            # ts_name = StringUtils.lower_case_to_camel_case(name)
            ts_name = name
            ts_type = self.get_field_zod_type(field_type)
            content_strs.append(f'{ts_name}: {ts_type},')
        return '\n  '.join(content_strs)

    def get_field_zod_type(self, field_type: type) -> str:
        if field_type == str:
            return 'z.string()'
        if field_type == int or field_type == float:
            return 'z.number()'
        if field_type == bool:
            return 'z.boolean()'
        if issubclass(field_type, BaseEnum):
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
            ts_class_name = self.get_ts_class_name_from_serializer_output_class(field_type)
            return f'Z{ts_class_name}'
        return ''
