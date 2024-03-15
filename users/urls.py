from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.LogoutView.as_view(), name='logout'),
    path(r'logoutall/', views.LogoutAllView.as_view(), name='logoutall'),
    path(r'check-auth/', views.CheckTokenView.as_view(), name='check')
]
