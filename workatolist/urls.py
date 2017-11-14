from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token

from core.urls import router1

urlpatterns = [
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^', include(router1.urls)),

]

