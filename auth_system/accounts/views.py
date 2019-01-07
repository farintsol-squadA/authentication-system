from django.views.generic import FormView, TemplateView
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'email_verification_sent.html', {'email': to_email})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/accounts/login/')
    else:
        return HttpResponse('Activation link is invalid!')


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('done/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def success_page(request):
    return render(request, 'success.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        # import pdb
        # pdb.set_trace()
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        # bug here user is returned none - fixed
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'success.html')
        return super(LoginView, self).form_invalid(form)


# todo: password reset
# commenting below as used inbuilt password reset views

'''
class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'password_reset_form.html'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        user = get_object_or_404(User, email=email)
        if user is not None:
            current_site = get_current_site(request)
            mail_subject = 'Passport Reset - DHFL'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('done/')
        return super(PasswordResetView, self).form_invalid(form)

'''
'''
def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_complete(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('done/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'password_reset_complete.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        form = SetPasswordForm(request.user)
        return render(request, 'password_reset_confirm.html', {'form' : form})
    else:
        return HttpResponse('Password reset link is invalid!')

'''
