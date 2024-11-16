from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from .permissions import IsBankStaff
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter


# Create your views here.


User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if not all(k in data for k in ("username", "password", "role")):
            return Response({"error": "Missing fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                role=data["role"],
            )
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_superuser=False)
    serializer_class = CustomUserSerializer
    permission_classes = [IsBankStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
    http_method_names = ['get']