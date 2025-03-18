from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login


from . forms import RegisterForm

from accounts.models import Account


from services.currency import call_conversion_api



def handle_currency_choice(request, form: RegisterForm):
    default = Account.get_default("currency")
    currency = form.cleaned_data["currency"]

    if (default == currency):
        user = form.save()
        return user

    
    amount = "750.00"


    try:
        result = call_conversion_api(request, default, currency, amount)
    except ValueError as e:
        message = str(e)
        











    














def register(request):
    # print(Account._meta.get_field("currency").default)
    print(Account.get_default("email"))

    if request.method == 'POST':
        print("\n\npost data:\n" + str(request.POST), end="\n\n")
        form = RegisterForm(request.POST)


        if form.is_valid():
            user = handle_currency_choice(request, form)
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()
    
    return render(request, 'register/register.html', {'form': form})


def index(request):
    return HttpResponse("hello, world. you are at index")

