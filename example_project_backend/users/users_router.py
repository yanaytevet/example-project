from ninja import Router

from users.views.users_views.my_user_view import MyUserItemView

router = Router()

MyUserItemView.register_get(router, 'my/')
