
from django.urls import path

from blocks.views.post_sample_block_view import PostSampleBlockView

urlpatterns = [
   path(r'', PostSampleBlockView.as_view(), name='sample'),
]
    