# serilaization of data to the database
from rest_framework import serializers
from .models import Payment

class VendorPaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'