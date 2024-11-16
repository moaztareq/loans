from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import CustomUser

# Create your tests here.


class BankSettingsTestCase(APITestCase):
    def setUp(self):
        # Create bank staff
        self.bank_staff = CustomUser.objects.create_user(
            username="staff1",
            password="password123",
            role="bank_staff"
        )
        self.client.login(username="staff1", password="password123")

    def test_create_bank_settings(self):
        # Create valid bank settings
        response = self.client.post("/global/settings/", {
            "min_loan_amount": 1000,
            "max_loan_amount": 50000,
            "interest_rate": 5,
            "max_duration_in_months": 60
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["max_loan_amount"], 50000)

    def test_invalid_min_max_loan_amount(self):
        # Min amount greater than max amount
        response = self.client.post("/global/settings/", {
            "min_loan_amount": 50000,
            "max_loan_amount": 1000,
            "interest_rate": 5,
            "max_duration_in_months": 60
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Minimum loan amount must be less than or equal to maximum loan amount.", str(response.data))
