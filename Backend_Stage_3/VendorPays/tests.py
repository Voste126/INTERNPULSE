from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Payment

class PaymentAPITests(APITestCase):
    def test_create_payment(self):
        # Use the namespaced URL
        url = reverse('payments:payment-list')
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "amount": "100.00",
            "gateway": "paypal"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'completed')
        self.assertTrue(response.data['transaction_id'].startswith('PAYPAL-TX-'))

    def test_get_payment(self):
        # Create a payment directly in the database.
        payment = Payment.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            amount="50.00",
            gateway="flutterwave",
            status="completed",
            transaction_id="FLUTTERWAVE-TX-1"
        )
        url = reverse('payments:payment-detail', kwargs={'pk': payment.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Jane Doe")
