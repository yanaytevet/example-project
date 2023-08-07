from django.urls import path

from users.views.client_registration_views.register_client_by_linkedin_view import RegisterClientByLinkedinView
from users.views.client_registration_views.register_client_view import RegisterClientView
from users.views.client_registration_views.send_email_verification_view import SendEmailVerificationEmailView
from users.views.client_registration_views.verify_email_by_pin_view import VerifyEmailByPinView

urlpatterns = [
    path(r"", RegisterClientView.as_view()),
    path(r"verify-email/", SendEmailVerificationEmailView.as_view()),
    path(r"verify-pin/", VerifyEmailByPinView.as_view()),
    path(r"linkedin/", RegisterClientByLinkedinView.as_view()),
]
