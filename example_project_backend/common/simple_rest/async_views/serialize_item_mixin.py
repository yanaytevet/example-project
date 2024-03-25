from abc import ABC, abstractmethod

from django.db.models import Model

from ..async_api_request import AsyncAPIRequest
from ..enums.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException
from ..serializers.serializer import Serializer
from ...type_hints import JSONType


class SerializeItemMixin(ABC):
    QUERY_PARAM_NAME = 'serializer'
    DEFAULT_SERIALIZER_NAME = 'default'

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        wanted_serializer_name = request.query_params.get(cls.QUERY_PARAM_NAME, None) or \
                                 cls.DEFAULT_SERIALIZER_NAME
        if wanted_serializer_name == cls.DEFAULT_SERIALIZER_NAME:
            return await (await cls.get_default_serializer(request, obj, **kwargs)).async_serialize(obj)
        serializers_by_name = await cls.get_serializers_by_name(request, obj, **kwargs)
        if wanted_serializer_name not in serializers_by_name:
            raise RestAPIException(StatusCode.HTTP_501_NOT_IMPLEMENTED, 'unimplemented_serializer',
                                   'Serializer not implemented')
        return await serializers_by_name[wanted_serializer_name].async_serialize(obj)

    @classmethod
    @abstractmethod
    async def get_default_serializer(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> Serializer:
        raise NotImplementedError()

    @classmethod
    async def get_serializers_by_name(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> dict[str, Serializer]:
        return {}
