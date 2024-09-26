from rest_framework.serializers import ModelSerializer
from .models import Order
from produce.serializers import ProduceSerializer
from accounts.serializers import ProfileSerializer


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderReadSerializer(ModelSerializer):
    farmer= ProfileSerializer(read_only=True)
    produce = ProduceSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'