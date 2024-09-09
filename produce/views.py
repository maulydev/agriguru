from rest_framework import viewsets, filters
from .models import Produce, Inventory
from .serializers import ProduceSerializer, InventorySerializer

class ProduceViewSet(viewsets.ModelViewSet):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'produce_id'