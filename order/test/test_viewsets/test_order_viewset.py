import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from order.models import Order


class TestOrderViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(
            title='mouse',
            price=100,
            category=[self.category]
        )
        self.order = OrderFactory(user=self.user, product=[self.product])

    def test_get_all_orders(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)['results'][0]

        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['product'][0]['category'][0]['title'], self.category.title)

    def test_create_order(self):
        new_product = ProductFactory(price=200)
        data = json.dumps({
            'products_id': [new_product.id],
            'user': self.user.id
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.filter(user=self.user).order_by('-id').first()
        self.assertEqual(created_order.product.first().id, new_product.id)