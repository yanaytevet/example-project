import os


class TsFileDataHolder:
    def __init__(self, ts_relative_path: str, class_name: str):
        self.ts_relative_path = ts_relative_path
        self.class_name = class_name

    def get_relative_path_from_another_path(self, another_path: str) -> str | None:
        if another_path == self.ts_relative_path:
            return None
        self_dir_arr = os.path.split(self.ts_relative_path)
        self_file_dir = self_dir_arr[0]
        self_file_name = self_dir_arr[1].split('.')[0]
        another_file_dir = os.path.split(another_path)[0]
        res = f'{os.path.relpath(self_file_dir, another_file_dir)}/{self_file_name}'
        if not res.startswith('.'):
            res = f'./{res}'
        if res.endswith('.ts'):
            res = res[:-3]
        return res
