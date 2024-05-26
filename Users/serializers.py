from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining JWT token pair (access token and refresh token) by providing user credentials.
    Extends TokenObtainPairSerializer to customize token generation with additional user information.
    """
    @classmethod
    def get_token(cls, user):
        """
        Method to customize the token generation process by adding extra user information to the token payload.
        Args:
            user: The user instance for which the token is generated.

        Returns:
            dict: Token payload including user's email, role, and full name.
        """
        token = super().get_token(user)
        token['email'] = user.email
        token['rol'] = user.rol
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user instance.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'rol']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        """
        Method to create a new user instance with the provided validated data.
        Hashes the password before saving the user instance.
        Args:
            validated_data: Validated data for creating the user instance.

        Returns:
            User: Newly created user instance.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}
        }

    def update(self, instance, validated_data):
        """
        Method to update an existing user instance with the provided validated data.
        Args:
            instance: The user instance to be updated.
            validated_data: Validated data for updating the user instance.

        Returns:
            User: Updated user instance.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating user password.
    """
    current_password = serializers.CharField(max_length=200, write_only=True)
    new_password = serializers.CharField(max_length=200, write_only=True)
    confirm_new_password = serializers.CharField(max_length=200, write_only=True)

    def validate(self, data):
        """
        Method to validate the new password and confirm password before updating.
        Args:
            data: Dictionary containing new password, current password, and confirm password.

        Returns:
            dict: Validated data.
        """
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("New passwords do not match.")

        user = self.context['request'].user
        if not check_password(current_password, user.password):
            raise serializers.ValidationError("Current password is incorrect.")
        try:
            validate_password(new_password, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'new_password': e.messages})
        return data
