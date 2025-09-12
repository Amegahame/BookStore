from rest_framework import serializers

from product.models import Product
from product.serializers.product_serializer import ProductSerializer
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, many=True)
    products_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total
    
    class Meta:
        model = Order
        fields = ['product', 'total', 'user', 'products_id']
        extra_kwargs = {'product': {'required': False}}

    def create(self, validated_data):
        products = validated_data.pop('products_id')
        user = validated_data.pop('user')

    
        order = Order.objects.create(user=user)
        order.product.set(products) 

        return order