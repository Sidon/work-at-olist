from django.conf.urls import url, include
from rest_framework import routers
# Old version
# from .views import ObjChannelViewSet, ObjCategoryViewSet, UrlChannelViewSet, UrlCategoryViewSet, CategViewSet
from .views import CategoryViewSet, ChannelViewSet


router1 = routers.DefaultRouter()
router1.register(r'channels', ChannelViewSet, base_name='channel')
router1.register(r'categories', CategoryViewSet, base_name='category')
urlpatterns = router1.urls
urlpatterns += [url(r'^docs/', include('rest_framework_docs.urls'))]

