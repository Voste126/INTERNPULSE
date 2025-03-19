from django.urls import path
from .views import PaymentCreateView, PaymentDetailView

urlpatterns = [
    # Endpoint to initiate a payment
    path('payments', PaymentCreateView.as_view(), name='payment-create'),
    # Endpoint to retrieve payment status by id
    path('payments/<int:pk>', PaymentDetailView.as_view(), name='payment-detail'),
]
