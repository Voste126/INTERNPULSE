# serilaization of data to the database
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'name', 'email', 'amount', 'gateway',
            'status', 'transaction_id'
        ]
        read_only_fields = ['status', 'transaction_id']
