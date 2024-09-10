from rest_framework import viewsets
from .models import Order
from .serializers import OrderCreateSerializer, OrderReadSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    filterset_fields = {
        'farmer': ['iexact', 'icontains'],
        'produce__name': ['iexact', 'icontains'],
        'order_status': ['iexact'],
        'order_date': ['exact', 'gte', 'lte'],
    }
    

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OrderCreateSerializer
        return OrderReadSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
