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
    """
    View for obtaining JWT token pair (access token and refresh token) by providing user credentials.
    """
    serializer_class = MyTokenObtainPairSerializer


class Create(generics.CreateAPIView):
    """
    View for creating a new user.
    """
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.AllowAny]


class Update(generics.UpdateAPIView):
    """
    View for updating user details.
    """
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]


class UpdatePassword(generics.UpdateAPIView):
    """
    View for updating user password.
    """
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = PasswordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        """
        Handle PUT request for updating user password.

        Args:
            request (HttpRequest): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response indicating the status of the password update operation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        user = self.get_object()
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    
class RetrieveUserInfo(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
