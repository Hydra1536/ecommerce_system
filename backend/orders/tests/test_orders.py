from categories.models import Category
from django.contrib.auth import get_user_model
from products.models import Product
from rest_framework.test import APITestCase

User = get_user_model()


class OrderTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", full_name="Test User", password="user123"
        )
        self.client.force_authenticate(user=self.user)

        cat = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Phone",
            sku="PHN",
            description="Smart phone",
            price=500,
            stock=10,
            status="active",
            category=cat,
        )

    def test_create_order(self):
        payload = {"items": [{"product_id": self.product.id, "quantity": 2}]}

        response = self.client.post("/api/orders/create/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_amount"], "1000.00")

    def test_user_orders(self):
        # First, create an order
        self.client.post(
            "/api/orders/create/",
            {"items": [{"product_id": self.product.id, "quantity": 1}]},
            format="json",
        )

        response = self.client.get("/api/orders/my-orders/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def tearDown(self):
        self.client.logout()
