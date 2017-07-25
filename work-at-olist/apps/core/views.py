from django.core.exceptions import ValidationError
from rest_framework import authentication, permissions, viewsets, filters
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog
from .models import Channel, Category
from .serializers import ChannelSerializer, CategorySerializer


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

    # authentication_classes = ()
    # permission_classes = ()

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class ChannelsViewSet(DefaultsMixin, LoggingMixin, viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    search_fields = ('name', )
    # ordering_fields = ()
    queryset = Channel.objects.all()


    def get_queryset(self):
        queryset = Channel.objects.all()
        uuid = self.request.query_params.get('uuid', None)
        name = self.request.query_params.get('name', None)

        if uuid is not None:
            return queryset.filter(uuid=uuid)
        elif name is not None:
            queryset.filter(name=name)

        return queryset

