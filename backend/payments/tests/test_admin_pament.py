from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from orders.models import Order
from payments.models import Payment

User = get_user_model()


class AdminPaymentsTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email="admin@example.com", full_name="Admin User", password="admin123"
        )
        self.client.force_authenticate(user=self.admin)

        order = Order.objects.create(user=self.admin, total_amount=999, status="paid")

        Payment.objects.create(
            order=order,
            provider="stripe",
            transaction_id="pi_123",
            status="success",
            raw_response="{}",
        )

    def test_admin_payment_list(self):
        response = self.client.get("/api/payments/all/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["amount"], "999.00")
        self.assertEqual(response.data[0]["status"], "success")

    def tearDown(self):
        self.client.logout()
