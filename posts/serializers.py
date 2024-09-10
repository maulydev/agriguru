from rest_framework import serializers
from .models import Post
from produce.serializers import ProduceSerializer
from accounts.serializers import ProfileSerializer

class PostReadSerializer(serializers.ModelSerializer):
    farmer = ProfileSerializer(read_only=True)
    produce = ProduceSerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']