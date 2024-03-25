from typing import Union

from .permissions_checker import PermissionsChecker
from ..api_request import APIRequest
from ..async_api_request import AsyncAPIRequest
from ..enums.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException


class MissingQueryParamsFieldAPIException(RestAPIException):
    def __init__(self, field: str):
        super().__init__(StatusCode.HTTP_400_BAD_REQUEST,
                         f'field_{field}_is_missing',
                         f'Field "{field}" is missing')


class RequestQueryParamsFieldsAPIChecker(PermissionsChecker):
    def __init__(self, required_fields: list[str]):
        self.required_fields = required_fields

    async def async_raise_exception_if_not_valid(self, request: Union[AsyncAPIRequest, APIRequest]) -> None:
        for field in self.required_fields:
            if field not in request.query_params:
                raise MissingQueryParamsFieldAPIException(field)
