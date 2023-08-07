from django.urls import path

from users.views.teams_views.my_teams_list_view import MyTeamsListView
from users.views.teams_views.team_item_by_admin_view import TeamItemByAdminView
from users.views.teams_views.team_item_by_manager_view import TeamItemByManagerView
from users.views.teams_views.teams_list_by_admin_view import TeamsListByAdminView
from users.views.teams_views.teams_list_by_manager_view import TeamsListByManagerView

urlpatterns = [
    path(r"my/", MyTeamsListView.as_view()),
    path(r"<int:object_id>/by-manager/", TeamItemByManagerView.as_view()),
    path(r"by-manager/", TeamsListByManagerView.as_view()),
    path(r"<int:object_id>/by-admin/", TeamItemByAdminView.as_view()),
    path(r"by-admin/", TeamsListByAdminView.as_view()),
]
