from django.test import TestCase
from product.models.category import Category
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer

class ProductSerializerTest(TestCase):
    def test_product_serializer_returns_expected_fields(self):
        category = Category.objects.create(title="Books")
        product = Product.objects.create(title="Django 101", price=50)
        product.category.set([category])  

        serializer = ProductSerializer(product)
        self.assertIn('title', serializer.data)
        self.assertIn('price', serializer.data)
        self.assertIn('category', serializer.data)
