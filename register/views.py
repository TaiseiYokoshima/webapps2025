from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login


from . forms import RegisterForm
from accounts.models import Account
from services.currency import call_conversion_api


from decimal import Decimal


from accounts.models import Account


from django.contrib import messages


def register_user_from_form(request, form: RegisterForm):
    default_currency = Account.get_default("currency")
    chosen_currency = form.cleaned_data["currency"]

    if (default_currency == chosen_currency):
        user = form.save()
        return user
    

    email = form.cleaned_data["email"]
    default_balance = str(Account.get_default("balance"))

    result = call_conversion_api(request, default_currency, chosen_currency, default_balance)


    balance = result["amount"]
    password = form.cleaned_data["password1"]



    user = Account(email=email, balance=Decimal(balance), currency=chosen_currency)
    user.set_password(password)
    user.save()
    

    return user





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # print(form)

        if form.is_valid():
            try:
                user = register_user_from_form(request, form)

            except Exception as e:
                return HttpResponseServerError("Internal server error, try again later")


            login(request, user)
            return redirect('home')


        messages.error(request, "Error")
        print(form.errors.as_data(), end="\n\n\n\n")
    else:
        form = RegisterForm()
    
    return render(request, 'register/register.html', {'form': form})


def index(request):
    return HttpResponse("hello, world. you are at index")

