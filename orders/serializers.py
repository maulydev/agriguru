from rest_framework.serializers import ModelSerializer
from .models import Order
from posts.serializers import PostReadSerializer


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderReadSerializer(ModelSerializer):
    post = PostReadSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'