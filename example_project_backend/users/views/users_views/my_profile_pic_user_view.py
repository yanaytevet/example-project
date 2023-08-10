import uuid

from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from external.storage.storage_manager import StorageManager
from users.serializers.user.full_user_serializer import FullUserSerializer


class MyProfilePicUserItemView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)

    def post(self, request: Request) -> Response:
        user = get_user(request)
        LoginAPIChecker().raise_exception_if_not_valid(user)
        file_obj = request.FILES['file']
        content = file_obj.read()
        new_pic_url = StorageManager().upload('profile-pictures', f'clients/{user.id}_{uuid.uuid4()}.png', content)

        if user.pic_url:
            StorageManager().remove_by_full_path('profile-pictures', user.pic_url)
        user.pic_url = new_pic_url
        user.save()

        data = FullUserSerializer().serialize(user)
        return Response(data, status=status.HTTP_200_OK)

    def delete_pic_url(self, pic_url: str) -> None:
        path = pic_url.split('profile-pictures/')[-1]
        StorageManager().remove('profile-pictures', path)
