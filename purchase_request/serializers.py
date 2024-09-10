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
    responses = PurchaseResponseSerializer(many=True, read_only=True, source='purchaseresponse_set')
    produce_name = serializers.CharField(source='produce.name', read_only=True)
    total_responses = serializers.IntegerField(source='purchaseresponse_set.count', read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = ['id', 'produce', 'produce_name', 'quantity_requested', 'proposed_price', 'pickup_date', 'status', 'created_at', 'total_responses', 'responses']
        read_only_fields = ['id', 'created_at', 'total_responses']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['proposed_price'] = float(representation['proposed_price']) if representation['proposed_price'] else None
        return representation