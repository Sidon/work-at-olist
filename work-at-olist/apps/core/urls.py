from rest_framework.routers import DefaultRouter
from .views import ChannelsViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'channels', ChannelsViewSet)
router.register(r'categories', CategoryViewSet)