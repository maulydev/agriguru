from rest_framework.viewsets import ModelViewSet
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ['payment_method', 'payment_status', 'payment_date', 'order__id']
    search_fields = ['payment_reference', 'order__order_number', 'payment_description']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']