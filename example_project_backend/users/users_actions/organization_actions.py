from typing import List

from common.time_utils import TimeUtils
from users.models import Organization, User


class OrganizationActions:
    def __init__(self, organization: Organization):
        self.organization = organization

    def get_all_org_managers(self) -> List[User]:
        res = []
        for user in self.organization.user_set.all():
            if user.is_org_manager():
                res.append(user)
        return res

    def update_last_call_created_time(self) -> None:
        self.organization.last_call_created_time = TimeUtils.now()
        self.organization.save()

    def update_last_sub_project_created_time(self):
        self.organization.last_sub_project_created_time = TimeUtils.now()
        self.organization.save()
