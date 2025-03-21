from django.db import models
from django.db import models

class Payment(models.Model):
    PAYMENT_GATEWAYS = (
        ('paypal', 'PayPal'),
        ('paystack', 'Paystack'),
        ('flutterwave', 'Flutterwave'),
    )

    name = models.CharField(max_length=100,default='Anonymous')
    email = models.EmailField(default='user@example.com')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAYS, default='paystack')
    status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"
