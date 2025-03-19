from rest_framework import generics
from .models import Payment
from .serializers import VendorPaysSerializer

class PaymentCreateView(generics.CreateAPIView):
    """
    POST /api/v1/payments
    Initiate a payment transaction.
    """
    queryset = Payment.objects.all()
    serializer_class = VendorPaysSerializer

    

class PaymentDetailView(generics.RetrieveAPIView):
    """
    GET /api/v1/payments/{id}
    Retrieve a payment's status.
    """
    queryset = Payment.objects.all()
    serializer_class = VendorPaysSerializer
