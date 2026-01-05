from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from orders.models import Order

User = get_user_model()


class PaymentTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", full_name="Test User", password="user123"
        )
        self.client.force_authenticate(user=self.user)

        self.order = Order.objects.create(
            user=self.user, total_amount=1500, status="pending"
        )

    def test_initiate_payment(self):
        response = self.client.post(
            f"/api/payments/pay/{self.order.id}/", {"provider": "stripe"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        # Check that the response is the client_secret string
        self.assertIsInstance(response.data, str)
        self.assertIn("_secret_", response.data)

    def tearDown(self):
        self.client.logout()
