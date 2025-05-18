from enum import StrEnum


class BaseEnum(StrEnum):
    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(value, value) for value in cls.get_list()]

    @classmethod
    def get_list(cls) -> list[str]:
        return list(cls)
