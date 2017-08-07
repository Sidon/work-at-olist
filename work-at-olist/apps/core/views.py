from django.core.exceptions import ValidationError

# DRF
from rest_framework import authentication, permissions, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from .models import Channel, Category
from .serializers import ObjChannelSerializer, ObjCategorySerializer, UrlChannelSerializer, UrlCategorySerializer


class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering
     and pagination."""

    authentication_classes = (
         authentication.BasicAuthentication,
         authentication.TokenAuthentication,
    )
    permission_classes = (
         permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )



class ObjChannelViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ObjChannelSerializer
    search_fields = ('name', )


class ObjCategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = ObjCategorySerializer
    search_fields = ('name', )


class UrlChannelViewSet(DefaultsMixin, viewsets.ModelViewSet):
    lookup_field = 'name'
    lookup_url_kwarg = 'name'
    queryset = Channel.objects.all()
    serializer_class = UrlChannelSerializer
    search_fields = ('name', )


class UrlCategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Category.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = UrlCategorySerializer
    search_fields = ('name', )




