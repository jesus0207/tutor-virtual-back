from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', TokenBlacklistView.as_view(), name='logout'),
    path('create', Create.as_view(), name='create'),
    path('update/<int:pk>', Update.as_view(), name='update'),
    path('update-password/<int:pk>', UpdatePassword.as_view(), name='update_password'),
]