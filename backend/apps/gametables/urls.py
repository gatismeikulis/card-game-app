from rest_framework.routers import DefaultRouter
from .views import GameTableViewSet

router = DefaultRouter()
router.register("", GameTableViewSet, basename="gametable")

urlpatterns = router.urls
