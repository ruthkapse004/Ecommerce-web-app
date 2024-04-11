from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from store.models import Customer
from .decorators import anonymous_user


# Create your views here.
@anonymous_user
def signup(request: HttpRequest):
    """
    Create new account.
    """

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        cnf_password = request.POST['cnf_password']

        if User.objects.filter(username=username).exists():
            messages.warning(
                request, "Account already exists with this username.")
            return redirect("signup")

        if password != cnf_password:
            messages.warning(request, "Passwords don't match.")
            return redirect("signup")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )

                Customer.objects.create(user=user, phone=phone)
                messages.success(request, "Account created sucessfully!")
                return redirect("signin")
        except Exception as e:
            print(e)
            messages.success(request, "Something went wrong.")
            return redirect("signup")

    return render(request, "authentication/signup.html")


@anonymous_user
def signin(request: HttpRequest):
    """
    This view log in the user.
    """

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.warning(request, "Invalid Credentials!")
            return redirect("signin")

        login(request, user)
        return redirect("store")

    return render(request, "authentication/signin.html")


@login_required(login_url="signin")
def signout(request: HttpRequest):
    """
    This view log out the current logged in user.
    """

    logout(request)
    messages.success(request, "Signed out sucessfully!")
    return redirect("signin")


def reset_password(request: HttpRequest):
    """
    This view is used to reset the password.
    """

    return render(request, "authentication/reset_password.html")


@login_required(login_url="signin")
def profile(request: HttpRequest):
    return render(request, 'authentication/profile.html')
