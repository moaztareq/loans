from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankSettingsViewSet

router = DefaultRouter()
router.register('settings', BankSettingsViewSet, basename='setting')

urlpatterns = [
    path('', include(router.urls)),
]