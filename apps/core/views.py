from django.core.exceptions import ValidationError

# DRF
from rest_framework import authentication, permissions, viewsets, filters, pagination
from .models import Channel, Category
from .serializers import ObjChannelSerializer, ObjCategorySerializer
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
    serializer_class = ObjChannelSerializer
    search_fields = ('name', )
    lookup_field = 'name'


class CategViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    #queryset = Category.objects.root_nodes()
    serializer_class = ObjCategorySerializer
    search_fields = ('name', )

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'


'''    
# Old Version
class UrlChannelViewSet(DefaultsMixin, viewsets.ModelViewSet):
    lookup_field = 'name'
    lookup_url_kwarg = 'name'
    queryset = Channel.objects.all()
    serializer_class = UrlChannelSerializer
    search_fields = ('name', )


class UrlCategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):

    queryset =  Category.objects.root_nodes()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = UrlCategorySerializer
    search_fields = ('name', )
    
class ObjCategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    # queryset = Category.objects.all()
    queryset = Category.objects.root_nodes()
    serializer_class = ObjCategorySerializer
    search_fields = ('name', )

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    

class CategViewSet(DefaultsMixin, viewsets.ModelViewSet):
    # queryset = Category.objects.all()

    # lookup_field = 'uuid'
    # lookup_url_kwarg = 'uuid'


    def list(self, request):
        queryset =Category.objects.root_nodes()
        serializer = ObjCategorySerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset=Category.objects.all()
        categ = get_object_or_404(queryset, pk=pk)
        serializer = ObjCategorySerializer(categ)
        return Response(serializer.data)    
    
'''


'''
class CategViewSet(DefaultsMixin, viewsets.ModelViewSet):
    # queryset = Category.objects.all()

    # lookup_field = 'uuid'
    # lookup_url_kwarg = 'uuid'
    # lookup_value_regex = '[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z'


    def list(self, request):
        queryset=Category.objects.root_nodes()
        serializer = ObjCategorySerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, uuid=None):
        queryset=Category.objects.all()
        categ = get_object_or_404(queryset, uuid=uuid)
        serializer = ObjCategorySerializer(categ)
        return Response(serializer.data)

'''

