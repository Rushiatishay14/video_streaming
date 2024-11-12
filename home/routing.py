from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/interview/(?P<room_name>\w+)/$", consumer.InterviewConsumer.as_asgi()),
]
