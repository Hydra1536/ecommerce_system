import json
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase


class StripeWebhookTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("payments.views.stripe")
    @patch("payments.views.stripe.Event.construct_from")
    def test_stripe_webhook_success(self, mock_event, mock_stripe):
        mock_stripe.util = MagicMock()
        mock_stripe.util.json.loads = json.loads
        mock_event.return_value = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_123"}},
        }

        payload = {
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_test_123"}},
        }

        response = self.client.post(
            "/api/payments/stripe/webhook/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
