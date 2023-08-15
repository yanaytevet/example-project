from django.db.models import QuerySet

from users.models import User, EmailAddress


class UserEmailsManager:
    def __init__(self, user: User):
        self.user = user

    def get_primary_email(self) -> EmailAddress:
        return self.user.email_addresses.filter(is_primary_email=True).first()

    def get_emails(self) -> QuerySet[EmailAddress]:
        return self.user.email_addresses.all()

    def add_email(self, email: str, is_primary: bool = None) -> EmailAddress | None:
        if not self.is_email_available(email):
            return None
        if is_primary is None:
            is_primary = not self.user.email_addresses.exists()
        return self.user.email_addresses.create(email=email, is_primary=is_primary)

    @classmethod
    def is_email_available(cls, email: str) -> bool:
        return not EmailAddress.objects.filter(email=email).exists()
