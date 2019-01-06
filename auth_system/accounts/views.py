from django.views.generic import CreateView, FormView, TemplateView
from .forms import RegisterForm, LoginForm
from django.shortcuts import render

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = '/login/'
    template_name = 'register.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/dashboard/'


class IndexView(TemplateView):
    template_name = 'index.html'


def success_page(request):
    return render(request, 'success.html')

# todo: logout view
# todo: password reset and change
# todo: verification email

