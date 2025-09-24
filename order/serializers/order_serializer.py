from rest_framework import serializers
from product.models import Product
from product.serializers.product_serializer import ProductSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)  
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        many=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'product', 'total', 'user', 'products_id']
        read_only_fields = ['id', 'total']

    def get_total(self, instance):
        return sum(product.price for product in instance.product.all())  

    def create(self, validated_data):
        products = validated_data.pop('products_id')
        order = Order.objects.create(**validated_data)
        order.product.set(products)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('products_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if products is not None:
            instance.product.set(products)

        return instance
