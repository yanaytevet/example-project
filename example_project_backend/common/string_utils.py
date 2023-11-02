import random
import string


class StringUtils:
    @classmethod
    def create_random_hash(cls, hash_length: int) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=hash_length))
