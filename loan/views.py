from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets, permissions
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Loan, LoanPayment, LoanProvider
from .serializers import LoanSerializer, LoanPaymentSerializer, LoanProviderSerializer
from core.permissions import IsBankStaff
from globals.models import BankSettings
from decimal import Decimal, InvalidOperation


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'delete']:
            return [IsBankStaff()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            # Return loans related to the current customer
            return Loan.objects.filter(customer=user)
        elif user.role == 'bank_staff':
            # Return all loans for bank personnel
            return Loan.objects.all()
        else:
            # Return an empty queryset for other roles
            return Loan.objects.none()

    def perform_create(self, serializer):
        # Ensure loan amount is within limits
        settings = BankSettings.objects.first()
        if not settings:
            raise serializers.ValidationError("Bank settings are not configured.")

        if not (settings.min_loan_amount <= serializer.validated_data['amount'] <= settings.max_loan_amount):
            raise serializers.ValidationError("Loan amount is outside allowed limits.")

        # Check total loans against total funds
        total_loans = Loan.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_funds = LoanProvider.objects.aggregate(total=Sum('total_funds'))['total'] or 0
        loan_amount = serializer.validated_data['amount']

        if total_loans + loan_amount > total_funds:
            remaining_funds = total_funds - total_loans
            raise serializers.ValidationError(
                {"error": f"Total loans cannot exceed available funds. Remaining funds: {round(remaining_funds, 2)}."}
            )

        # Save the loan
        serializer.save(customer=self.request.user)

    def destroy(self, request, *args, **kwargs):
        # Get the loan object
        loan = self.get_object()

        # Check if the loan is approved
        if loan.approved and not request.user.is_superuser:
            raise serializers.ValidationError("Only superusers can delete approved loans.")

        # If not approved or the user is a superuser, allow deletion
        return super().destroy(request, *args, **kwargs)


class LoanPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = LoanPaymentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'delete']:
            return [IsBankStaff()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Get the loan ID from the URL
        loan_id = self.kwargs.get('loan_pk')
        if loan_id:
            # Return payments for the specified loan
            return LoanPayment.objects.filter(loan_id=loan_id)
        return LoanPayment.objects.none()  # Default to empty if no loan ID provided

    def perform_create(self, serializer):
        # Get the loan object
        loan_id = self.kwargs.get('loan_pk')
        loan = Loan.objects.get(id=loan_id)

        if not loan.approved:
            raise serializers.ValidationError({"error": "This loan isn't approved yet."})        

        # Calculate the total loan amount with interest
        total_loan_amount = loan.amount + (loan.amount * (loan.interest_rate / 100))
        monthly_payment = total_loan_amount / loan.term_in_months

        # Calculate the sum of all payments for this loan
        total_paid = LoanPayment.objects.filter(loan=loan).aggregate(total=Sum('amount'))['total'] or 0

        # Get the current payment amount
        payment_amount = serializer.validated_data['amount']

        # Validation 1: Ensure payment is not less than the monthly payment
        if payment_amount < monthly_payment:
            raise serializers.ValidationError(
                {"error": f"The payment cannot be less than the monthly payment of {round(monthly_payment, 2)}."}
            )

        # Validation 2: Ensure total payments do not exceed the loan amount
        remaining_amount = total_loan_amount - total_paid
        if payment_amount > remaining_amount:
            raise serializers.ValidationError(
                {
                    "error": f"You are exceeding the loan amount. You should pay only {round(remaining_amount, 2)}."
                }
            )

        # Save the payment if all validations pass
        serializer.save(loan=loan)


class LoanProviderViewSet(viewsets.ModelViewSet):
    queryset = LoanProvider.objects.all()
    serializer_class = LoanProviderSerializer
    permission_classes = [IsBankStaff]

    @action(detail=True, methods=['get'], url_path='amortization')
    def amortization_table(self, request, pk=None):
        provider = self.get_object()

        # Get parameters for amortization calculation
        total_funds = Decimal(provider.total_funds)
        annual_interest_rate = request.query_params.get('interest_rate', '5')  # Default to 5% if not provided
        loan_term_months = request.query_params.get('term', '12')  # Default to 12 months if not provided

        try:
            annual_interest_rate = Decimal(annual_interest_rate)
            loan_term_months = int(loan_term_months)
        except (InvalidOperation, ValueError):
            return Response({"error": "Invalid interest rate or term value."}, status=400)

        if annual_interest_rate <= 0 or loan_term_months <= 0:
            return Response({"error": "Interest rate and term must be greater than 0."}, status=400)

        # Calculate the monthly payment
        monthly_interest_rate = annual_interest_rate / Decimal(100) / Decimal(12)
        if monthly_interest_rate > 0:
            monthly_payment = total_funds * (
                monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months
            ) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
        else:
            # If interest rate is 0, the payment is simply the principal divided by the term
            monthly_payment = total_funds / loan_term_months

        # Generate the amortization table
        balance = total_funds
        table = []
        for i in range(1, loan_term_months + 1):
            interest_payment = balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            table.append({
                "payment_number": i,
                "monthly_payment": round(monthly_payment, 2),
                "principal_payment": round(principal_payment, 2),
                "interest_payment": round(interest_payment, 2),
                "remaining_balance": round(max(balance, 0), 2)
            })

        return Response(table, status=200)