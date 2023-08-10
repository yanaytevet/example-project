from django.urls import path

from users.views.user_events_views.post_create_user_event_view import PostCreateUserEventView

urlpatterns = [
    path(r'', PostCreateUserEventView.as_view()),
]
