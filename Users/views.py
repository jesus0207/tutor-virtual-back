from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsOwnerPermission
from .serializers import (
    CreateUserSerializer,
    MyTokenObtainPairSerializer,
    UpdateUserSerializer,
    PasswordUpdateSerializer
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]


class UpdateUserPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = PasswordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        user = self.get_object()
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
