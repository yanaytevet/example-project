import hashlib
from typing import Type, Optional, Set, TypeVar

from asgiref.sync import async_to_sync, sync_to_async
from django.db import models
from django.forms import model_to_dict

from common.type_hints import JSONType

T = TypeVar('T')


class ModelUtils:
    @classmethod
    def create_from_json(cls, model_cls: Type[T],
                         json_data: JSONType,
                         allowed_attributes_set: Optional[Set[str]] = None) -> T:
        return async_to_sync(cls.async_create_from_json)(model_cls, json_data, allowed_attributes_set)

    @classmethod
    async def async_create_from_json(cls, model_cls: Type[T],
                                     json_data: JSONType,
                                     allowed_attributes_set: Optional[Set[str]] = None) -> T:
        obj = model_cls()
        await cls.async_update_from_json(obj, json_data, allowed_attributes_set)
        return obj

    @classmethod
    def update_from_json(cls,
                         obj: models.Model,
                         json_data: JSONType,
                         allowed_attributes_set: Optional[Set[str]] = None) -> None:
        return async_to_sync(cls.async_update_from_json)(obj, json_data, allowed_attributes_set)

    @classmethod
    async def async_update_from_json(cls,
                         obj: models.Model,
                         json_data: JSONType,
                         allowed_attributes_set: Optional[Set[str]] = None) -> None:
        for key, value in json_data.items():
            if allowed_attributes_set is not None and key in allowed_attributes_set:
                setattr(obj, key, value)
        await obj.asave()

    @classmethod
    def to_json(cls, obj: models.Model) -> JSONType:
        data = model_to_dict(obj)
        del data['id']
        return data

    @classmethod
    def get_hash_by_fields(cls, obj: models.Model, fields: list[str]) -> str:
        string = ''.join(getattr(obj, field) for field in fields)
        sha256_hash = hashlib.sha256()
        sha256_hash.update(string.encode('utf-8'))
        return sha256_hash.hexdigest()
