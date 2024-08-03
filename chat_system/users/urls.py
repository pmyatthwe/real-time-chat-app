from django.urls import path
from .views import (
    UserRegistrationView, 
    PasswordResetView, 
    PasswordResetConfirmView, 
    EmailVerificationView,
    UserListView,
    UserRetrieveUpdateDeleteView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('email-verify/', EmailVerificationView.as_view(), name='email_verify'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveUpdateDeleteView.as_view(), name='user-retrieve-update-delete'),
]
