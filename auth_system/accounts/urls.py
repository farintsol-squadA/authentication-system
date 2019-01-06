from django.urls import path
from .views import (RegisterView, LoginView, IndexView)
from . import views as account_views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('dashboard/', account_views.success_page, name='success'),
]