from rest_framework import serializers
from .models import BankSettings


class BankSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankSettings
        fields = '__all__'