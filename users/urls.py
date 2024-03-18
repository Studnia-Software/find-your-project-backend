from django.urls import path
from . import views
from users.services import UserService

user_service = UserService()

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.LogoutView.as_view(), name='logout'),
    path(r'logoutall/', views.LogoutAllView.as_view(), name='logoutall'),
    path(r'check-auth/', views.CheckTokenView.as_view(), name='check-auth'),
    path(r'request-password-reset/', views.RequestPasswordResetView.as_view(user_service=user_service), name='request-password-reset'),
    path(r"reset-password/", views.ResetPasswordView.as_view(user_service=user_service), name='reset-password'),
]
