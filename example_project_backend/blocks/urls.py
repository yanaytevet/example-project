
from django.urls import path

from blocks.views.post_sample_websocket_view import PostSampleWebsocketView

urlpatterns = [
   path(r'websocket-test/', PostSampleWebsocketView.as_view(), name='sample'),
]
    