from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from .models import *
from .forms import *
import json

# Create your views here.


# authentication views
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "registration sucessfull! welcome to transport logistics"
            )
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render(request, "core/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Wecome back, {username}!")
                return redirect("dashboard")
        messages.error(request, "invalid username or password")
    else:
        form = LoginForm()
    return render(request, "core/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "you have been logged out")
    return redirect("login")


@login_required
def dashboard(request):
    context = {}
    return render(request, "core/dashboard.html", context)
