from django.shortcuts import render

from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, logout, login

from django.shortcuts import render, redirect

from django.contrib import messages

from utils.currency import CurrencyAmount

from django.contrib.auth.decorators import user_passes_test

from .forms import LoginForm
from .models import Account



def is_non_superuser(user):
    return user.is_authenticated and not user.is_superuser


login_required = user_passes_test(is_non_superuser)


@login_required
def home(request):
    user = request.user
    passon = {"balance": CurrencyAmount(user.balance).to_api_str(), "currency": user.currency }
    return render(request, "accounts/home.html",  passon)

@login_required
def sign_out(request):
    print("\n\nlogging out\n\n")
    logout(request)
    return redirect('login')


def sign_in(request):
    if is_non_superuser(request.user): 
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            
            

        print(form.errors.as_data())
        messages.error(request, "Invalid login")
    
    else:
        form = LoginForm()



    
    return render(request, "accounts/login.html", {"form": form})



