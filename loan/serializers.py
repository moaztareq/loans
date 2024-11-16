from rest_framework import serializers
from .models import Loan, LoanPayment, LoanProvider


class LoanSerializer(serializers.ModelSerializer):
    monthly_payment = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = '__all__'

    def get_monthly_payment(self, obj):
        # Calculate monthly payment
        if obj.term_in_months > 0:  # Avoid division by zero
            total_amount = obj.amount + (obj.amount * (obj.interest_rate / 100))
            return round(total_amount / obj.term_in_months, 2)
        return 0.0  # Default if term_in_months is not valid

class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'
        read_only_fields = ['loan']


class LoanProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProvider
        fields = '__all__'