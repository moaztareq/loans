from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import BankSettings
from .serializers import BankSettingsSerializer
from core.permissions import IsBankStaff

# Create your views here.


class BankSettingsViewSet(viewsets.ModelViewSet):
    queryset = BankSettings.objects.all()
    serializer_class = BankSettingsSerializer
    permission_classes = [IsBankStaff]
    pagination_class = None
    http_method_names = ['get', 'patch', 'post']