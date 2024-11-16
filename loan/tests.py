from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Loan, LoanProvider, LoanPayment
from core.models import CustomUser
from globals.models import BankSettings

# Create your tests here.

#----------------------------------------------------Test cases for creating a loan---------------------------------------------
class LoanCreationTestCase(APITestCase):
    def setUp(self):
        # Create a customer
        self.customer = CustomUser.objects.create_user(
            username="customer1",
            password="password123",
            role="customer"
        )
        self.client.login(username="customer1", password="password123")

        # Create bank settings
        self.bank_settings = BankSettings.objects.create(
            min_loan_amount=1000,
            max_loan_amount=50000,
            interest_rate=5,
            max_duration_in_months=60
        )

        # Create loan provider with funds
        self.loan_provider = LoanProvider.objects.create(
            user=CustomUser.objects.create_user(username="provider1", password="password123", role="provider"),
            total_funds=100000
        )

    def test_create_valid_loan(self):
        # Valid loan creation
        response = self.client.post("/loan/loans/", {
            "amount": 5000,
            "term_in_months": 12
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 5000)
        self.assertEqual(response.data["approved"], False)

    def test_create_loan_outside_limits(self):
        # Loan amount less than min_loan_amount
        response = self.client.post("/loan/loans/", {
            "amount": 500,
            "term_in_months": 12
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Loan amount is outside allowed limits.", str(response.data))

    def test_create_loan_exceeding_total_funds(self):
        # Reduce available funds
        self.loan_provider.total_funds = 6000
        self.loan_provider.save()

        response = self.client.post("/loan/loans/", {
            "amount": 10000,
            "term_in_months": 12
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Total loans cannot exceed available funds.", str(response.data))
#----------------------------------------------------Test cases for creating a loan---------------------------------------------


#----------------------------------------------------Test cases for creating a loan payment---------------------------------------------
class LoanPaymentTestCase(APITestCase):
    def setUp(self):
        # Create a customer
        self.customer = CustomUser.objects.create_user(
            username="customer2",
            password="password123",
            role="customer"
        )
        self.client.login(username="customer2", password="password123")

        # Create bank settings
        self.bank_settings = BankSettings.objects.create(
            min_loan_amount=1000,
            max_loan_amount=50000,
            interest_rate=5,
            max_duration_in_months=60
        )

        # Create a loan
        self.loan = Loan.objects.create(
            customer=self.customer,
            amount=10000,
            term_in_months=12,
            interest_rate=5,
            approved=True
        )

    def test_make_valid_payment(self):
        # Valid loan payment
        response = self.client.post(f"/loans/{self.loan.id}/payments/", {
            "amount": 875
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], 875)

    def test_payment_below_monthly_payment(self):
        # Payment less than monthly payment
        response = self.client.post(f"/loans/{self.loan.id}/payments/", {
            "amount": 500
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The payment cannot be less than the monthly payment", str(response.data))

    def test_payment_exceeding_remaining_balance(self):
        # Make a large payment exceeding loan total
        LoanPayment.objects.create(loan=self.loan, amount=9500)
        response = self.client.post(f"/loans/{self.loan.id}/payments/", {
            "amount": 2000
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You are exceeding the loan amount", str(response.data))
#----------------------------------------------------Test cases for creating a loan payment---------------------------------------------