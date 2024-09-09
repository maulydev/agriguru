from rest_framework import serializers
from .models import Produce, Inventory

class ProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produce
        fields = '__all__'
        
        
        
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'produce', 'quantity', 'created_at', 'updated_at']
