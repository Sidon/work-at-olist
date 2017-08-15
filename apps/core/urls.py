from django.conf.urls import url, include
from rest_framework import routers
# Old version
# from .views import ObjChannelViewSet, ObjCategoryViewSet, UrlChannelViewSet, UrlCategoryViewSet, CategViewSet
from .views import CategViewSet, ChannelViewSet


router1 = routers.DefaultRouter()
router1.register(r'channels', ChannelViewSet, base_name='channel')
router1.register(r'categ', CategViewSet, base_name='categ')

urlpatterns = router1.urls

urlpatterns += [url(r'^docs/', include('rest_framework_docs.urls'))]

#  (r'^category/(?<uuid>.+)/$', CatViewSet.as_view())

# Old Version
# router1.register(r'categories', ObjCategoryViewSet, base_name='category')
# router1.register(r'url-channels', UrlChannelViewSet, base_name='url-channel')
# router1.register(r'url-categories', UrlCategoryViewSet, base_name='url-category')


