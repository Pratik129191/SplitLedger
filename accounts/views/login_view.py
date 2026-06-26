from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from accounts.forms import LoginForm


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                request=request,
                username=email,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('core:dashboard')
            messages.error(
                request,
                'Invalid credentials.'
            )
    return render(
        request,
        'accounts/login.html',
        {
            'form': form,
        }
    )
