from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import LoanViewSet, LoanPaymentViewSet, LoanProviderViewSet

router = DefaultRouter()
router.register('loans', LoanViewSet, basename='loan')
router.register('providers', LoanProviderViewSet, basename='provider')

# Nested router for payments under loans
loans_router = NestedDefaultRouter(router, 'loans', lookup='loan')
loans_router.register('payments', LoanPaymentViewSet, basename='loan-payment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(loans_router.urls)),
]