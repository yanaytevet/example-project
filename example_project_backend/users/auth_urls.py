from django.urls import path

from users.views.auth_views.auth_view import AuthView
from users.views.auth_views.change_password_views import ChangePasswordView
from users.views.auth_views.login_view import LoginView
from users.views.auth_views.logout_view import LogoutView
from users.views.forgot_my_password_views.check_temporary_access_view import CheckTemporaryAccessView
from users.views.forgot_my_password_views.forgot_my_password_view import ForgotMyPasswordView
from users.views.forgot_my_password_views.change_password_by_access_id_view import ChangePasswordByAccessIdView

urlpatterns = [
    path(r'', AuthView.as_view(), name='auth'),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'change-password/', ChangePasswordView.as_view(), name='change-password'),
    path(r'logout/', LogoutView.as_view(), name='logout'),

    path(r'forgot-my-password/', ForgotMyPasswordView.as_view()),
    path(r'check-temporary-access/', CheckTemporaryAccessView.as_view()),
    path(r'change-password-by-access-id/', ChangePasswordByAccessIdView.as_view()),
]
