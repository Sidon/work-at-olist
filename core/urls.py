from django.conf.urls import url, include
from rest_framework import routers
# Old version
# from .views import ObjChannelViewSet, ObjCategoryViewSet, UrlChannelViewSet, UrlCategoryViewSet, CategViewSet
from .views import HomeView, CategoryViewSet, ChannelViewSet

app_name = 'core'

router = routers.DefaultRouter()
router.register(r'channels', ChannelViewSet, base_name='channel')
router.register(r'categories', CategoryViewSet, base_name='category')

# urlpatterns = router.urls
#urlpatterns += [url(r'^docs/', include('rest_framework_docs.urls'))]

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
