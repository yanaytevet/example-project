from common.files_generators.ts_files_data_holders.ts_file_data_holder import TsFileDataHolder


class InterfaceTsFileDataHolder(TsFileDataHolder):
    def __init__(self, file_relative_path: str, class_name: str):
        super().__init__(file_relative_path, class_name)
        self.annotations: list[tuple[str, type]] = []

    def set_annotations(self, annotations: list[tuple[str, type]]) -> None:
        self.annotations = annotations

