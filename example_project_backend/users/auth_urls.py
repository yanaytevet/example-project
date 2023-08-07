from django.urls import path

from users.views.auth_views.auth_view import AuthView
from users.views.auth_views.change_password_views import ChangePasswordView
from users.views.auth_views.login_view import LoginView
from users.views.auth_views.logout_view import LogoutView
from users.views.forgot_my_password_views.forgot_my_password_view import ForgotMyPasswordView
from users.views.forgot_my_password_views.change_password_by_access_id_view import ChangePasswordByAccessIdView
from users.views.user_social_auth.user_auth_with_linkedin import LinkedInAuthRegisterView, LinkedInAuthLoginView

urlpatterns = [
    path(r"", AuthView.as_view(), name="auth"),
    path(r"login/", LoginView.as_view(), name="login"),
    path(r"change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(r"logout/", LogoutView.as_view(), name="logout"),
    path(r"forgot-my-password/", ForgotMyPasswordView.as_view()),
    path(r"change-password-by-access-id/", ChangePasswordByAccessIdView.as_view()),
    path(r"register-with-linkedin/", LinkedInAuthRegisterView.as_view(), name="register-with-linkedin"),
    path(r"login-with-linkedin/", LinkedInAuthLoginView.as_view(), name="login-with-linkedin"),
]
