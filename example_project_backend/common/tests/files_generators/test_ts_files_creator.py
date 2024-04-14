from typing import TypedDict

from django.test import TestCase

from common.base_enum import BaseEnum
from common.files_generators.ts_files_creator import TsFilesCreator
from common.files_generators.ts_files_data_holders.interface_ts_file_data_holder import InterfaceTsFileDataHolder
from common.files_generators.ts_files_data_holders.ts_file_data_holder import TsFileDataHolder


class Shapes(BaseEnum):
    a = 'A'


class Tastes(BaseEnum):
    a = 'A'


class Smells(BaseEnum):
    a = 'A'


class ShortUserSerializerOutput(TypedDict):
    pass


class FullUserSerializerOutput(TypedDict):
    pass


class ShortInfoSerializerOutput(TypedDict):
    pass


class FullInfoSerializerOutput(TypedDict):
    pass


class TestTsFilesCreator(TestCase):
    maxDiff = None

    def test_get_interface_content_from_ts_file_data_holder(self):
        obj = TsFilesCreator()
        obj.enum_class_name_to_ts_file_data_holder = {
            'Shapes': TsFileDataHolder('enums/blocks/shapes.ts', 'Shapes'),
            'Tastes': TsFileDataHolder('enums/blocks/more-enums/tastes.ts', 'Tastes'),
            'Smells': TsFileDataHolder('enums/blocks/smells.ts', 'Smells'),
        }
        obj.interface_class_name_to_ts_file_data_holder = {
            'ShortUser': InterfaceTsFileDataHolder('interfaces/users/short-user.ts', 'ShortUser'),
            'FullUser': InterfaceTsFileDataHolder('interfaces/users/full-user.ts', 'FullUser'),
            'ShortInfo': InterfaceTsFileDataHolder('interfaces/info/short-info.ts', 'ShortInfo'),
            'FullInfo': InterfaceTsFileDataHolder('interfaces/info/full-info.ts', 'FullInfo'),
        }

        example_interface_holder_1 = InterfaceTsFileDataHolder('interfaces/example/full-example.ts',
                                                               'FullExample')
        example_interface_holder_1.set_annotations([
            ('a', str),
            ('b', int),
            ('c', float),
            ('d', bool),
            ('bool_list', list[bool]),
            ('dict_for_int', dict[str, int]),
        ])
        interface_content = obj.get_interface_content_from_ts_file_data_holder(example_interface_holder_1)
        wanted_content = '''import {z} from "zod";


export const ZFullExample = z.object({
  a: z.string(),
  b: z.number(),
  c: z.number(),
  d: z.boolean(),
  boolList: z.array(z.boolean()),
  dictForInt: z.record(z.string(), z.number()),
});

export type FullExample = z.infer<typeof ZFullExample>;
'''

        self.assertEqual(interface_content, wanted_content)

        example_interface_holder_1.set_annotations([
            ('a', str),
            ('b', Shapes),
            ('c', list[Tastes]),
            ('d', dict[int, Smells]),
            ('user', ShortUserSerializerOutput),
            ('users', list[ShortUserSerializerOutput]),
            ('info_obj', FullInfoSerializerOutput),
        ])
        interface_content = obj.get_interface_content_from_ts_file_data_holder(example_interface_holder_1)
        wanted_content = '''import {z} from "zod";
import {ZShapes} from "../../enums/blocks/shapes";
import {ZTastes} from "../../enums/blocks/more-enums/tastes";
import {ZSmells} from "../../enums/blocks/smells";
import {ZShortUser} from "../users/short-user";
import {ZFullInfo} from "../info/full-info";

export const ZFullExample = z.object({
  a: z.string(),
  b: ZShapes,
  c: z.array(ZTastes),
  d: z.record(z.number(), ZSmells),
  user: ZShortUser,
  users: z.array(ZShortUser),
  infoObj: ZFullInfo,
});

export type FullExample = z.infer<typeof ZFullExample>;
'''

        self.assertEqual(interface_content, wanted_content)
