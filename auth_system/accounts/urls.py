from django.urls import path
from .views import (LoginView, IndexView)
from . import views as account_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/register/', account_views.register, name='register'),
    path('activate/<uidb64>/<token>/', account_views.activate, name='activate'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', account_views.logout_view, name='logout'),
    path('success/', account_views.success_page, name='success'),


    # change password
    path('accounts/password_change/',
         account_views.password_change, name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='change_password_done.html'
    ), name='password_change_done'),


    # reset password
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
    ), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html',
    ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_reset_complete.html',
    ), name='password_reset_complete'),
]
