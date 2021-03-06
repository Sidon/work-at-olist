from django.core.exceptions import ValidationError

# DRF
from rest_framework import viewsets
from django.views.generic import TemplateView
from rest_framework import authentication, permissions, viewsets, filters, pagination
from markdownx.utils import markdownify
from .models import Channel, Category
from .serializers import ChannelSerializer, CategorySerializer
from .forms import ChannelFilter, CategoryFilter


class HomeView(TemplateView):

    template_name = 'core/home.html'
    context_object_name = 'markdown'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        with open('README.md', 'r') as f:
            data = f.read()
        context['markdwon'] = markdownify(data)

        print ("====>",context)


        return context

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
     
    API endpoint that allows channels to view  
    
    retrieve:    
    Return a channel instance.
        
    list:    
    Return a list of all channel with categories and subcategories.
    For to view a instance, click in *instance* link
    
    '''
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    search_fields = ('name', )
    lookup_field = 'name'
    http_method_names = ['get', 'head']
    filter_class = ChannelFilter



class CategoryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    '''

    API endpoint that allows categories to view  

    retrieve:    
    Return a category instance.

    list:    
    Return a list of all categories and subcategories.
    For to view a instance, click in *instance* link

    '''

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name', )

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    http_method_names = ['get', 'head']
    filter_class = CategoryFilter


