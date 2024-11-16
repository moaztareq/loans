from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('provider', 'Loan Provider'),
        ('customer', 'Loan Customer'),
        ('bank_staff', 'Bank Personnel'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    class Meta:
        ordering = ['-id']