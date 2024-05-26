from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['rol'] = user.rol
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'rol']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class PasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=200, write_only=True)
    new_password = serializers.CharField(max_length=200, write_only=True)
    confirm_new_password = serializers.CharField(max_length=200, write_only=True)

    def validate(self, data):
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
