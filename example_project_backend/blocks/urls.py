
from django.urls import path

from blocks.views.blocks_views.delete_block_item_view import DeleteBlockItemView
from blocks.views.blocks_views.get_block_item_view import GetBlockItemView
from blocks.views.blocks_views.get_pagination_blocks_list_view import GetPaginationBlockListView
from blocks.views.blocks_views.patch_block_item_view import PatchBlockItemView
from blocks.views.blocks_views.post_action_build_block_item_view import PostActionBuildBlockItemView
from blocks.views.blocks_views.post_create_block_item_view import PostCreateBlockItemView
from blocks.views.post_sample_websocket_view import PostSampleWebsocketView
from common.simple_rest.async_views.async_compose_api_views import async_compose_api_views

urlpatterns = [
   path('', async_compose_api_views(GetPaginationBlockListView(), PostCreateBlockItemView()).as_view()),
   path(r'<int:object_id>/', async_compose_api_views(GetBlockItemView(), PatchBlockItemView(),
                                                     DeleteBlockItemView()).as_view()),
   path(r'<int:object_id>/build/', PostActionBuildBlockItemView.as_view()),
   path(r'websocket-test/', PostSampleWebsocketView.as_view()),
]
    