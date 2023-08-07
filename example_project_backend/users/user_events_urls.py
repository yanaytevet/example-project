from django.urls import path

from users.views.user_events_views.user_events_list_by_admin_view import UserEventsListByAdminView
from users.views.user_events_views.user_events_list_view import UserEventsListView

urlpatterns = [
    path(r"", UserEventsListView.as_view()),
    path(r"by-admin/", UserEventsListByAdminView.as_view()),
]
