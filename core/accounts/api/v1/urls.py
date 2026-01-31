from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "api-v1"

urlpatterns = [
    path("registration", views.RegistrationApiView.as_view(), name="registration"),
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path("profile/", views.ProfileAPIView.as_view(), name="profile"),
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("test-email/", views.EmailTesting.as_view(), name="test-email"),
    path('activation/<str:token>', views.ActivationAPIView.as_view(), name="activation"),
    path('activation/resend/', views.ActivationResendAPIView.as_view(), name="activation-resend"),
    path('reset-password/email/', views.EmailResetPasswordView.as_view(), name="reset-password-email"),
    path('reset-password/<str:token>', views.ResetPasswordView.as_view(), name="reset-password"),
]
