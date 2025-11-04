from django.urls import re_path
from .consumers import GameTableWebSocketConsumer

urlpatterns = [
    re_path(
        r"^(?P<table_id>[0-9a-zA-Z\-]+)/$",
        GameTableWebSocketConsumer.as_asgi(),
    ),
]
