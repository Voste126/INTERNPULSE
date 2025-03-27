from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'price', 'stock_status',
            'sku', 'description', 'created_at', 'updated_at'
        ]
