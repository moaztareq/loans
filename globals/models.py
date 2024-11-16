from django.db import models
from mutual.models import TimeStampedModel

# Create your models here.


class BankSettings(TimeStampedModel):
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_duration_in_months = models.PositiveIntegerField()

    class Meta:
        ordering = ['-id']