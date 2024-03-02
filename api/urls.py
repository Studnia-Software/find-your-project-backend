from django.urls import path
from .views import View

urlpatterns = [
    path('view/', View.as_view(), name='view'),
]