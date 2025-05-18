from ninja import Router

from blocks.views.blocks_views.create_block_item_view import PostCreateBlockItemView
from blocks.views.blocks_views.delete_block_item_view import DeleteBlockItemView
from blocks.views.blocks_views.pagination_blocks_view import PaginationBlockView
from blocks.views.blocks_views.read_block_item_view import ReadBlockItemView
from blocks.views.blocks_views.run_action_build_block_item_view import RunActionBuildBlockItemView
from blocks.views.blocks_views.update_block_item_view import UpdateBlockItemView
from blocks.views.post_sample_websocket_view import PostSampleWebsocketView

router = Router()

PaginationBlockView.register_get(router, '')
PostCreateBlockItemView.register_post(router)
ReadBlockItemView.register_get_by_id(router)
UpdateBlockItemView.register_patch_by_id(router)
DeleteBlockItemView.register_delete_by_id(router)
RunActionBuildBlockItemView.register_post_by_id(router, 'build/')

PostSampleWebsocketView.register_post(router, 'websocket-test/')