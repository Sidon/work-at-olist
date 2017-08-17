from django.core.exceptions import ValidationError

# DRF
from rest_framework import authentication, permissions, viewsets, filters, pagination
from .models import Channel, Category
from .serializers import ChannelSerializer, CategorySerializer
from rest_framework import viewsets


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

    # pagination_class = pagination.PageNumberPagination
    # paginate_by = 10

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class ChannelViewSet(DefaultsMixin, viewsets.ModelViewSet):
    '''
     
    API endpoint that allows channels to ve viewed or edited 
    
    retrieve:    
    Return a channel instance.
        
    list:    
    Return a list of all channel with categories and subcategories.
    For to view a instance, click in *self* link
    
          
    [ref]: http://127.0.0.1:8087/channels/Shop1/
    
    '''


    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    search_fields = ('name', )
    lookup_field = 'name'


class CategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    #queryset = Category.objects.root_nodes()
    serializer_class = CategorySerializer
    search_fields = ('name', )

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

