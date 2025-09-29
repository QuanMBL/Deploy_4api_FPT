from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_id', 'order_id', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'created_at']
