from django.contrib import admin
from django.contrib import admin
from .models import Loan, LoanPayment, LoanProvider

# Register your models here.


admin.site.register(Loan)
admin.site.register(LoanPayment)
admin.site.register(LoanProvider)