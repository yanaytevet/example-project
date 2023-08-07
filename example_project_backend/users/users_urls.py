from django.urls import path

from users.views.users_views.admin_users_list_by_admin_view import AdminUsersListByAdminView
from users.views.users_views.my_admin_data_view import MyAdminDataView
from users.views.users_views.my_full_user_view import MyFullUserItemView
from users.views.users_views.my_profile_pic_user_view import MyProfilePicUserItemView
from users.views.users_views.my_status_view import MyStatusView
from users.views.users_views.my_timezone_by_secret_id_view import MyTimezoneBySecretIdView
from users.views.users_views.my_timezone_view import MyTimezoneView
from users.views.users_views.my_user_for_payment_item_view import MyUserForPaymentItemView
from users.views.users_views.my_user_view import MyUserItemView
from users.views.users_views.table_users_list_by_manager_view import TableUsersListByManagerView
from users.views.users_views.timelines_by_admin_view import TimelinesByAdminView
from users.views.users_views.user_item_by_admin_view import UserItemByAdminView
from users.views.users_views.user_item_by_manager_view import UserItemByManagerView
from users.views.users_views.user_item_by_username_by_admin_view import UserItemByUsernameByAdminView
from users.views.users_views.users_list_by_admin_view import UsersListByAdminView
from users.views.users_views.users_list_by_client_view import UsersListByClientView
from users.views.users_views.users_list_by_manager_view import UsersListByManagerView
from users.views.users_views.persona_list_by_admin_view import PersonaListByAdminView
urlpatterns = [
    path(r"", UsersListByClientView.as_view()),
    path(r"my/", MyUserItemView.as_view()),
    path(r"my-admin-data/", MyAdminDataView.as_view()),
    path(r"my/timezone/", MyTimezoneView.as_view()),
    path(r"my/timezone/<int:expert_id>/by-secret-id/", MyTimezoneBySecretIdView.as_view()),
    path(r"my/full/", MyFullUserItemView.as_view()),
    path(r"my/for-payment/", MyUserForPaymentItemView.as_view()),
    path(r"my/profile-pic/", MyProfilePicUserItemView.as_view()),
    path(r"my-status/", MyStatusView.as_view()),
    path(r"by-manager/", UsersListByManagerView.as_view()),
    path(r"table/by-manager/", TableUsersListByManagerView.as_view()),
    path(r"<int:object_id>/by-manager/", UserItemByManagerView.as_view()),
    path(r"by-admin/", UsersListByAdminView.as_view()),
    path(r"table/by-admin/", UsersListByAdminView.as_view()),
    path(r"<int:object_id>/by-admin/", UserItemByAdminView.as_view()),
    path(r"admin-users/by-admin/", AdminUsersListByAdminView.as_view()),
    path(r"by-username/by-admin/", UserItemByUsernameByAdminView.as_view()),
    path(r"timelines/by-admin/", TimelinesByAdminView.as_view()),
    path(r"persona/by-admin/", PersonaListByAdminView.as_view()),
]
