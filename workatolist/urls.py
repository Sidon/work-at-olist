from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from core.urls import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
    url(r'^markdownx/', include('markdownx.urls')),
    url(r'^', include('core.urls')),
    url(r'^docs/', include_docs_urls(title='My API title')),
]

print (urlpatterns)