import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Payment

@pytest.mark.django_db
def test_create_payment():
    client = APIClient()
    url = reverse('payment-create')
    data = {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": "50.00"
    }
    response = client.post(url, data, format='json')
    # Check that the payment is created (HTTP 201 Created)
    assert response.status_code == 201
    assert Payment.objects.count() == 1
    payment = Payment.objects.first()
    assert payment.customer_name == "John Doe"

@pytest.mark.django_db
def test_retrieve_payment():
    client = APIClient()
    # Create a payment instance
    payment = Payment.objects.create(
        customer_name="John Doe",
        customer_email="john@example.com",
        amount="50.00",
        status="completed"
    )
    url = reverse('payment-detail', args=[payment.id])
    response = client.get(url, format='json')
    # Check that the payment details are correctly returned
    assert response.status_code == 200
    # The response should contain the payment details
    data = response.data
    assert data['id'] == payment.id
    assert data['customer_name'] == "John Doe"
    assert data['status'] == "completed"
