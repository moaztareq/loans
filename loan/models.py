from django.db import models
from core.models import CustomUser
from mutual.models import TimeStampedModel

# Create your models here.
class LoanProvider(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='provider_user',limit_choices_to={'role': 'provider'})
    total_funds = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-id']


class Loan(TimeStampedModel):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='loan_user', limit_choices_to={'role': 'customer'})
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    term_in_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan for {self.customer.username}: {self.amount} over {self.term_in_months} months"
    
    class Meta:
        ordering = ['-id']


class LoanPayment(TimeStampedModel):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    # date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Loan ID {self.loan.id}"
    
    class Meta:
        ordering = ['-id']