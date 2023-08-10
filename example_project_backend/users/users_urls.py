from django.urls import path

from users.views.users_views.my_user_view import MyUserItemView

urlpatterns = [
    path(r'my/', MyUserItemView.as_view()),
]
