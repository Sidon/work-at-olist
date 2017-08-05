from django.core.exceptions import ValidationError

# DRF
from rest_framework import authentication, permissions, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from .models import Channel, Category
from .serializers import ChannelSerializer, CategorySerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


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


class ChannelsViewSet(DefaultsMixin, viewsets.ModelViewSet):
    lookup_field = 'name'
    lookup_url_kwarg = 'name'
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    search_fields = ('name', )


class CategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset = Category.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = CategorySerializer
    search_fields = ('name', )




