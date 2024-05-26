from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core import validators
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        # Create and save a new user with the given email and password
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        # Create and save a new superuser with the given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
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
        return f'user email: {self.email}'
