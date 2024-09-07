from rest_framework import viewsets
from .models import PostGallery
from .serializers import PostGallerySerializer

class PostGalleryViewSet(viewsets.ModelViewSet):
    queryset = PostGallery.objects.all()
    serializer_class = PostGallerySerializer