from django.db import models
class Payment(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"PAY-{self.id}"
