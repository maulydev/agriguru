from rest_framework import serializers
from .models import PostGallery

class PostGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostGallery
        fields = '__all__'