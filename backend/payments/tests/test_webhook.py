import json
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase


class StripeWebhookTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("payments.views.stripe.Webhook.construct_event")
    def test_stripe_webhook_success(self, mock_construct_event):
        mock_construct_event.return_value = {
            "type": "checkout.session.completed",
            "data": {"object": {"id": "cs_test_123", "payment_status": "paid"}},
        }

        payload = {
            "type": "checkout.session.completed",
            "data": {"object": {"id": "cs_test_123", "payment_status": "paid"}},
        }

        response = self.client.post(
            "/api/payments/stripe/webhook/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test_signature",
        )

        self.assertEqual(response.status_code, 200)
