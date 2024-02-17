from typing import get_type_hints


class TypeUtils:
    @classmethod
    def is_typeddict(cls, obj: any) -> bool:
        if hasattr(obj, '__total__'):
            return True
        try:
            return '__annotations__' in get_type_hints(obj)
        except Exception:
            return False
