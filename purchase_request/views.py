from rest_framework import viewsets
from .models import PurchaseRequest, PurchaseResponse
from .serializers import PurchaseRequestSerializer, PurchaseRequestDetailSerializer, PurchaseResponseSerializer

class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequest.objects.all()
    serializer_class = PurchaseRequestSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PurchaseRequestDetailSerializer
        return PurchaseRequestSerializer


class PurchaseResponseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseResponse.objects.all()
    serializer_class = PurchaseResponseSerializer
    filterset_fields = ['farmer', 'accepted', 'rejected']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'farmer'):  # Check if the user is a farmer
            return PurchaseResponse.objects.filter(farmer=user)
        return PurchaseResponse.objects.all()