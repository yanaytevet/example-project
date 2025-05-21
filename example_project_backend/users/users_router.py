from common.django_utils.api_router_creator import ApiRouterCreator
from users.views.users_views.my_user_view import MyUserItemView

api, router = ApiRouterCreator.create_api_and_router('users')

MyUserItemView.register_get(router, 'my/')
