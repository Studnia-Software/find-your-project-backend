from django.urls import path
from . import views
from users.services import UserService, EmailService

user_service = UserService()
email_service = EmailService()

urlpatterns = [
    path(
        'register/',
        views.RegisterView.as_view(user_service=user_service),
        name='register'
    ),
    path(
        'login/',
        views.LoginView.as_view(user_service=user_service),
        name='login'
    ),
    path(
        r'logout/',
        views.LogoutView.as_view(user_service=user_service),
        name='logout'
    ),
    path(
        r'logoutall/',
        views.LogoutAllView.as_view(user_service=user_service),
        name='logoutall'
    ),
    path(
        r'check-auth/',
        views.CheckTokenView.as_view(),
        name='check-auth'
    ),
    path(
        r'request-password-reset/',
        views.RequestPasswordResetView.as_view(user_service=user_service, email_service=email_service),
        name='request-password-reset'
    ),
    path(
        r"reset-password/",
        views.ResetPasswordView.as_view(user_service=user_service),
        name='reset-password'
    ),
]
