from django.urls import path
from channels.routing import URLRouter

from apps.gametables.routing import urlpatterns as tables_ws


websocket_urlpatterns = [
    path("ws/tables/", URLRouter(tables_ws)),
]
