from rest_framework import routers
from .views import ObjChannelViewSet, ObjCategoryViewSet, UrlChannelViewSet, UrlCategoryViewSet

router1 = routers.DefaultRouter()
#router2 = routers.DefaultRouter()

router1.register(r'channels', ObjChannelViewSet, base_name='channel')
router1.register(r'categories', ObjCategoryViewSet, base_name='category')
router1.register(r'url-channels', UrlChannelViewSet, base_name='url-channel')
router1.register(r'url-categories', UrlCategoryViewSet, base_name='url-category')


