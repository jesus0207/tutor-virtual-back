from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core import validators
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating and managing users.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Method to create a new user instance with the provided email and password.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields to include in the user creation.

        Returns:
            User: The newly created user instance.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Method to create a new superuser instance with the provided email and password.

        Args:
            username (str): The username of the superuser.
            email (str): The email of the superuser.
            password (str): The password of the superuser.
            **extra_fields: Additional fields to include in the superuser creation.

        Returns:
            User: The newly created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """
    Custom user model extending AbstractUser and PermissionsMixin.
    """
    ROL_TYPE = (
        ('Estudiante', 'Estudiante'),
        ('Profesor', 'Profesor')
    )

    username = None
    first_name = models.CharField(max_length=60, blank=False, null=False)
    last_name = models.CharField(max_length=60, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=200, validators=[validators.MinLengthValidator(8)])
    rol = models.CharField(choices=ROL_TYPE, max_length=60, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Method to return a string representation of the user.

        Returns:
            str: The email of the user.
        """
        return f'user email: {self.email}'
