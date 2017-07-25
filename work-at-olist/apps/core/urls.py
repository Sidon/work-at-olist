from rest_framework.routers import DefaultRouter
from .views import ChannelsViewSet

router = DefaultRouter()
router.register(r'channels', ChannelsViewSet)
