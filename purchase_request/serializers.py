from rest_framework import serializers
from .models import PurchaseRequest, PurchaseResponse


class PurchaseRequestSerializer(serializers.ModelSerializer):
    farmers_responded = serializers.SerializerMethodField()
    produce_details = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseRequest
        fields = '__all__'

    def get_farmers_responded(self, obj):
        return [
            {
                'id': response.farmer.id,
                'username': response.farmer.user.username,
                'first_name': response.farmer.user.first_name,
                'last_name': response.farmer.user.last_name,
                'accepted': response.accepted,
                'rejected': response.rejected,
                'price_per_ton': float(response.price_per_ton) if response.price_per_ton else None,
                'response_date': response.response_date
            }
            for response in obj.purchaseresponse_set.all()
        ]

    def get_produce_details(self, obj):
        return {
            'id': obj.produce.id,
            'name': obj.produce.name,
            'description': obj.produce.description,
            'image': obj.produce.image.url if obj.produce.image else None,
        }


class PurchaseResponseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseResponse
        fields = '__all__'
        

class PurchaseResponseSerializer(serializers.ModelSerializer):
    quantity_requested = serializers.IntegerField(source='purchase_request.quantity_requested', read_only=True)
    produce = serializers.CharField(source='purchase_request.produce.name', read_only=True)
    proposed_price = serializers.CharField(source='purchase_request.proposed_price', read_only=True)
    pickup_date = serializers.DateField(source='purchase_request.pickup_date', read_only=True)
    message = serializers.CharField(source='purchase_request.message', read_only=True)
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