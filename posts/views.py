# from rest_framework import viewsets
# from .models import Post
# from .serializers import PostReadSerializer, PostCreateSerializer

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     filterset_fields = ['farmer__user__id', 'farmer', 'is_negotiable', 'is_sold_out']
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return PostCreateSerializer
#         return PostReadSerializer

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post
from .serializers import PostReadSerializer, PostCreateSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filterset_fields = ['farmer__user__id', 'farmer', 'is_negotiable', 'is_sold_out']
    parser_classes = (MultiPartParser, FormParser)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostReadSerializer