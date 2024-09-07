from rest_framework import viewsets, filters
from .models import Produce
from .serializers import ProduceSerializer

class ProduceViewSet(viewsets.ModelViewSet):
    queryset = Produce.objects.all()
    serializer_class = ProduceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']