import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegisterForm, LoginForm
from .models import User
from .utils import send_confirmation_email
from django.contrib.auth import logout

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_confirmation_code = str(uuid.uuid4())[:6].upper()  # confirmation code
            user.email_confirmed = False
            user.save()

            send_confirmation_email(user)

            request.session['user_id'] = user.id  # for confirmation

            return redirect('econfirm')
    else:
        form = RegisterForm()
    return render(request, 'accounts/registration.html', {'form': form})

def login(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.email_confirmed:
                    error = "Please confirm your email before logging in."
                else:
                    auth_login(request, user)
                    return redirect('home')  # or another page
            else:
                error = 'Invalid email or password'
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'error': error})

def econfirm(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('registration')

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect('registration')

    error = None
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.email_confirmation_code:
            user.email_confirmed = True
            user.email_confirmation_code = ''
            user.save()
            auth_login(request, user)
            return redirect('home')
        else:
            error = "Invalid confirmation code"
    return render(request, 'accounts/e-confirm.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page after logout
