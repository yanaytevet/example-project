import random
import string
from typing import Callable


class StringUtils:
    @classmethod
    def create_random_hash(cls, hash_length: int) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=hash_length))

    @classmethod
    def create_random_hash_func(cls, hash_length: int) -> Callable[[], str]:
        return lambda: cls.create_random_hash(hash_length)
