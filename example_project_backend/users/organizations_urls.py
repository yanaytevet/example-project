from django.urls import path

from users.views.organizations_views.my_organization_by_manager_view import MyOrganizationByManagerView
from users.views.organizations_views.my_organization_pic_by_manager_view import MyOrganizationPicByManagerView
from users.views.organizations_views.my_organization_view import MyOrganizationItemView
from users.views.organizations_views.organization_item_by_admin_view import OrganizationItemByAdminView
from users.views.organizations_views.organizations_list_by_admin_view import OrganizationsListByAdminView

urlpatterns = [
    path(r"my/", MyOrganizationItemView.as_view()),
    path(r"my/by-manager/", MyOrganizationByManagerView.as_view()),
    path(r"my/org-pic/by-manager/", MyOrganizationPicByManagerView.as_view()),
    path(r"<int:object_id>/by-admin/", OrganizationItemByAdminView.as_view()),
    path(r"by-admin/", OrganizationsListByAdminView.as_view()),
]
