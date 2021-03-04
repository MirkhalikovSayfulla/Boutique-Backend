from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from .forms import UserRegisterForm


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user and user is not None:
        login(request, user)
        return redirect('products:home')

    context = {
        'active': 'login'
    }

    return render(request, "users/login.html", context)


def register_view(request):
    forms = UserRegisterForm(request.POST or None)
    if forms.is_valid():
        forms.save()
        return redirect('users:login')

    context = {
        'forms': forms,
        'active': 'register'
    }
    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('products:home')
