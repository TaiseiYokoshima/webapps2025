from django.http import HttpResponseForbidden

from django.db.models import Q

from urllib.parse import unquote


from django.shortcuts import render


from django.contrib.auth import authenticate, logout, login

from django.shortcuts import render, redirect

from django.contrib import messages

from utils.currency import CurrencyAmount


from accounts.models import Account


from django.contrib.auth.decorators import user_passes_test


from .forms import AdminCreationForm

from payapp.models import Request, Payment

def is_admin(user):
    return user.is_authenticated and user.is_superuser


admin = user_passes_test(is_admin, login_url='/admin/login')


@admin
def home(request):
    if request.method != "GET":
        return HttpResponseForbidden()


    users = Account.objects.filter(is_superuser=False)

    for customer in users:
        customer.balance = CurrencyAmount(customer.balance).to_api_str()



    return render(request, "admin/home.html", {"users": users} )

@admin
def sign_out(request):
    if request.method != "GET":
        return HttpResponseForbidden()

    print("\n\nlogging out\n\n")
    logout(request)
    return redirect('admin_login')

def signin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin_home")

    if request.method == "GET":
        return render(request, "admin/login.html")

    if request.method != "POST":
        return HttpResponseForbidden()


    form = request.POST
    username = form.get("username")
    password = form.get("password")


    user = authenticate(request, username=username, password=password)


    if user is not None and user.is_staff:
        login(request, user)
        return redirect("admin_home")
    else:
        messages.error(request, "Invalid Login")
        return render(request, "admin/login.html")


@admin
def admin_create(request):
    if request.method == "GET":
        return render(request, "admin/register.html")

    if request.method != "POST":
        return HttpResponseForbidden()

    form = request.POST

    print(form.get("email"))
    form = AdminCreationForm(request.POST)


    if form.is_valid():
        print("fomr is valid")
        user = form.save()
        login(request, user)
        return redirect("admin_home")


    exception = (list(form.errors.as_data().values())[0][0]).messages[0]
    messages.error(request, exception)


    
    return render(request, "admin/register.html")



@admin
def view_payments(request, user_email):
    if request.method != "GET":
        return HttpResponseForbidden()

    user_email = unquote(user_email)


    account = None

    try:
        account = Account.objects.get(email=user_email)
    except Exception as e:
        print(e)
        messages.error(request, "User not found")
        render(request, "admin/payments.html")

    payments = Payment.objects.filter( Q(sender=account) | Q(receiver=account) ).order_by("-date")

    
    for payment in payments:
        payment.incoming = payment.receiver == account
        payment.sender_amount = CurrencyAmount(payment.sender_amount).to_api_str()
        payment.receiver_amount = CurrencyAmount(payment.receiver_amount).to_api_str()


    passon = {'payments': payments, "current": account.email, "balance": CurrencyAmount(account.balance).to_api_str(), "currency": account.currency }



    return render(request, "admin/payments.html",  passon)



@admin
def view_requests(request, user_email):
    if request.method != "GET":
        return HttpResponseForbidden()

    user_email = unquote(user_email)

    http_request = request

    account = None

    try:
        account = Account.objects.get(email=user_email)
    except Exception as e:
        print(e)
        messages.error(request, "User not found")
        render(request, "admin/requets.html")

    requests = Request.objects.filter( Q(sender=account) | Q(receiver=account) ).order_by("-date")

    
    for request in requests:
        request.incoming = request.receiver == account

        status = request.status

        if status == "P":
            status = "Pending"
        elif status == "A":
            status = "Approved"
        elif status == "D":
            status = "Denied"
        else:
           return HttpResponseServerError() 

        request.status = status
        request.sender_amount = CurrencyAmount(request.sender_amount).to_api_str()
        request.receiver_amount = CurrencyAmount(request.receiver_amount).to_api_str()


    passon = {'requests': requests, "current": account.email, "balance": CurrencyAmount(account.balance).to_api_str(), "currency": account.currency }


    return render(http_request, "admin/requests.html",  passon)
