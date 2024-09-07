from rest_framework import serializers
from .models import PurchaseRequest, PurchaseResponse


class PurchaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequest
        fields = '__all__'


class PurchaseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseResponse
        fields = '__all__'


class PurchaseRequestDetailSerializer(serializers.ModelSerializer):
    responses = PurchaseResponseSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = '__all__'