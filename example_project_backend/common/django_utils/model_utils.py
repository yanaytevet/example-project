import hashlib
from typing import Type

from django.db.models import Model
from django.forms import model_to_dict
from ninja import Schema

from common.type_hints import JSONType


class ModelUtils:

    @classmethod
    async def update_from_schema(cls, obj: Model, data: Schema) -> None:
        for key, value in data.model_dump(exclude_unset=True).items():
            if hasattr(obj, key):
                setattr(obj, key, value)

    @classmethod
    async def create_model_from_schema(cls, model_cls: Type[Model], data: Schema) -> Model:
        obj = model_cls()
        await cls.update_from_schema(obj, data)
        await obj.save()
        return obj

    @classmethod
    def to_json(cls, obj: Model) -> JSONType:
        data = model_to_dict(obj)
        del data['id']
        return data

    @classmethod
    def get_hash_by_fields(cls, obj: Model, fields: list[str]) -> str:
        string = ''.join(getattr(obj, field) for field in fields)
        sha256_hash = hashlib.sha256()
        sha256_hash.update(string.encode('utf-8'))
        return sha256_hash.hexdigest()
