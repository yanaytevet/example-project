import uuid

from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.org_manager_api_checker import OrgManagerAPIChecker
from external.storage.storage_manager import StorageManager
from users.serializers.organization_serializer import OrganizationSerializer


class MyOrganizationPicByManagerView(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)

    def post(self, request: Request) -> Response:
        user = get_user(request)
        OrgManagerAPIChecker().raise_exception_if_not_valid(user)
        file_obj = request.FILES['file']
        content = file_obj.read()
        organization = user.organization
        new_logo_url = StorageManager().upload('profile-pictures', f'organizations/{organization.id}_{uuid.uuid4()}.png',
                                              content)

        if organization.logo_url:
            StorageManager().remove_by_full_path('profile-pictures', organization.logo_url)
        organization.logo_url = new_logo_url
        organization.save()

        data = OrganizationSerializer().serialize(organization)
        return Response(data, status=status.HTTP_200_OK)
