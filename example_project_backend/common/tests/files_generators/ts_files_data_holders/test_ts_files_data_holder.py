
from django.test import TestCase

from common.files_generators.ts_files_data_holders.ts_file_data_holder import TsFileDataHolder


class TestTsFileDataHolder(TestCase):
    def test_get_relative_path_from_another_path(self):
        obj = TsFileDataHolder('aaa/bbb/ccc', 'CCC')
        self.assertIsNone(
            obj.get_relative_path_from_another_path('aaa/bbb/ccc')
        )
        self.assertEqual(
            obj.get_relative_path_from_another_path('aaa/bbb/ddd'),
            './ccc'
        )
        self.assertEqual(
            obj.get_relative_path_from_another_path('aaa/bbb/eee/ddd'),
            '../ccc'
        )
        self.assertEqual(
            obj.get_relative_path_from_another_path('aaa/ddd'),
            './bbb/ccc'
        )
        self.assertEqual(
            obj.get_relative_path_from_another_path('aaa/fff/ddd'),
            '../bbb/ccc'
        )
        self.assertEqual(
            obj.get_relative_path_from_another_path('zzz/yyy/www'),
            '../../aaa/bbb/ccc'
        )
