from django.test import TestCase
from django.contrib.auth.models import User
from product.models.category import Category
from product.models.product import Product
from order.serializers.order_serializer import OrderSerializer
from order.models import Order

class OrderSerializerTest(TestCase):
    def test_order_serializer_returns_expected_fields(self):
        user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpass123'
        )
        
        category = Category.objects.create(title="Books")
        product = Product.objects.create(title="Django 101", price=50)
        product.category.set([category])  
        order = Order.objects.create(user=user) 
        order.product.set([product])  

        serializer = OrderSerializer(order)
        self.assertIn('product', serializer.data)
        self.assertIn('total', serializer.data)