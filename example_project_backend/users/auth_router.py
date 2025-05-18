from ninja import Router

from users.views.auth_views.auth_view import AuthView
from users.views.auth_views.change_password_views import ChangePasswordView
from users.views.auth_views.login_view import LoginView
from users.views.auth_views.logout_view import LogoutView
from users.views.forgot_my_password_views.change_password_by_access_id_view import ChangePasswordByAccessIdView
from users.views.forgot_my_password_views.check_temporary_access_view import CheckTemporaryAccessView
from users.views.forgot_my_password_views.forgot_my_password_view import ForgotMyPasswordView

router = Router()

AuthView.register_get(router, '')
LoginView.register_post(router, 'login/')
LogoutView.register_post(router, 'logout/')
ChangePasswordView.register_post(router, 'change-password/')

CheckTemporaryAccessView.register_post(router, 'check-temporary-access/')
ForgotMyPasswordView.register_post(router, 'forgot-my-password/')
ChangePasswordByAccessIdView.register_post(router, 'change-password-by-access-id/')
