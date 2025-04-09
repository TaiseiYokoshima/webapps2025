from decimal import Decimal
from enum import Enum

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden, HttpResponseServerError
from services.currency import CurrencyAmount, call_conversion_api
from django.db import IntegrityError, transaction


from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect


from django.db.models import Q


from django.contrib import messages


from typing import Union, Type

from accounts.models import Account
from .models import Payment
from .models import Request
from .models import Notification



from .forms import TransferForm


class TransferResult(Enum):
    Ok = "success"
    InsufficientFunds = "Failed to make payment due to insufficient funds"
    CurrencyExchangFaillure = "Server error due to currency conversion"
    InvalidStringValueForAmount = "Invalid string value for currency amount"
    TransactionFailure = "Server error due to transaction failure"


def non_atomic_make_payment(request, sender: Account, receiver: Account, amount_input: CurrencyAmount) -> TransferResult:
    rate = CurrencyAmount(1)

    source: str = sender.currency
    target: str = receiver.currency


    amount = amount_input.into()

    if amount > sender.balance:
        return TransferResult.InsufficientFunds

    if (source != target):
        amount_str = CurrencyAmount(amount).to_api_str()

        try:
            result_json = call_conversion_api(request, source, target, amount_str)
            rate = CurrencyAmount(result_json["rate"])
        except Exception as e:
            print(e)
            return TransferResult.CurrencyExchangFaillure


    amount = CurrencyAmount(amount)
    
    sender_amount = amount
    receiver_amount = CurrencyAmount((amount * rate).into())


    sender_balance = (CurrencyAmount(sender.balance) - sender_amount).into()
    receiver_balance = (CurrencyAmount(receiver.balance) + receiver_amount).into()



    sender.balance = sender_balance
    receiver.balance = receiver_balance


    sender.save()
    receiver.save()



    sender_amount = sender_amount.into()
    receiver_amount = receiver_amount.into()


    payment: Payment = Payment(
            sender=sender, receiver=receiver, 
            sender_amount=sender_amount, receiver_amount=receiver_amount, rate=rate.into()) 


    payment.save()


    return TransferResult.Ok


def non_atomic_make_request(request, sender: Account, receiver: Account, amount_input: CurrencyAmount) -> TransferResult:
    rate = CurrencyAmount(1)

    source: str = receiver.currency
    target: str = sender.currency

    amount = amount_input.into()

    if (source != target):
        amount_str = CurrencyAmount(amount).to_api_str()

        try:
            result_json = call_conversion_api(request, source, target, amount_str)
            rate = CurrencyAmount(result_json["rate"])
        except Exception as e:
            print(e)
            return TransferResult.CurrencyExchangFaillure


    amount = CurrencyAmount(amount)
    
    receiver_amount = amount.into()
    sender_amount = (amount * rate).into()

    payment_request: Request = Request(
            sender=sender, receiver=receiver, 
            sender_amount=sender_amount, receiver_amount=receiver_amount, rate=rate.into()) 

    payment_request.save()

    return TransferResult.Ok


def make_payment(request, sender: Account, receiver: Account, amount_input: CurrencyAmount) -> TransferResult:
    try:
        with transaction.atomic():
            return non_atomic_make_payment(request, sender, receiver, amount_input)
    except Exception as e:
        print(e)
        return TransferResult.TransactionFailure


def make_request(request, sender: Account, receiver: Account, amount_input: CurrencyAmount) -> TransferResult:
    try:
        with transaction.atomic():
            return non_atomic_make_request(request, sender, receiver, amount_input)
    except Exception as e:
        print(e)
        return TransferResult.TransactionFailure


@login_required
def view_make_payment(request):
    transfer_type = "payment"
    if request.method == "GET":
        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type})

    if request.method != "POST":
        return HttpResponseForbidden()

    form = TransferForm(request.POST, user=request.user)
    form_invalid = not form.is_valid()
    if form_invalid:
        exception = (list(form.errors.as_data().values())[0][0]).messages[0]
        messages.error(request, exception)

        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type, "form": form})
    

    sender, receiver, amount = form.get_payment_data()


    result = make_payment(request, sender, receiver, amount)


    if result != TransferResult.Ok:
        messages.error(request, result.value)
        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type, "form": form})


    return redirect("home")


@login_required
def view_make_request(request):
    transfer_type = "request"
    if request.method == "GET":
        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type})

    if request.method != "POST":
        return HttpResponseForbidden()

    form = TransferForm(request.POST, user=request.user)
    form_invalid = not form.is_valid()
    if form_invalid:
        exception = (list(form.errors.as_data().values())[0][0]).messages[0]
        messages.error(request, exception)

        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type, "form": form})
    

    sender, receiver, amount = form.get_request_data()

    result = make_request(request, sender, receiver, amount)


    if result != TransferResult.Ok:
        messages.error(request, result.value)
        return render(request, "payapp/make_transfer.html", {"transfer_type": transfer_type, "form": form})


    return redirect("home")



@login_required
def view_payments(request):
    account = request.user

    payments = Payment.objects.filter( Q(sender=account) | Q(receiver=account) ).order_by("-date")

    for payment in payments:
        payment.incoming = payment.receiver == account
        payment.sender_amount = CurrencyAmount(payment.sender_amount).to_api_str()
        payment.receiver_amount = CurrencyAmount(payment.receiver_amount).to_api_str()

    return render(request, "payapp/payments.html", {'payments': payments} )

@login_required
def view_requests(request):
    http_request = request
    account = request.user


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



    return render(http_request, "payapp/requests.html", { "requests": requests, "user": account })




def non_atomic_apply_request(request: Request) -> TransferResult:
    sender = request.sender
    receiver = request.receiver


    sender_amount = CurrencyAmount(request.sender_amount)
    receiver_amount = CurrencyAmount(request.receiver_amount)
    rate = request.rate

    
    sender_balance = (CurrencyAmount(sender.balance) - sender_amount).into()
    receiver_balance = (CurrencyAmount(receiver.balance) + receiver_amount).into()


    sender.balance = sender_balance
    receiver.balance = receiver_balance

    sender.save()
    receiver.save()


    payment: Payment = Payment(
        sender=sender, 
        receiver=receiver, 
        sender_amount=sender_amount, 
        receiver_amount=receiver_amount, 
        rate=rate, 
        from_request=True
    ) 

    payment.save()

    request.status = "A"
    request.save()

    return TransferResult.Ok


def apply_request(request: Request) -> TransferResult:
    if request.sender_amount > request.sender.balance:
        return TransferResult.InsufficientFunds

    try:
        with transaction.atomic():
            return non_atomic_apply_request(request)

    except Exception as e:
        print(e)
        return TransferResult.TransactionFailure





@login_required
def approve_request(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    user = request.user
    request_id = request.POST.get("request_id")

    approved_request: Request | None = Request.objects.filter(id=request_id).first()


    if approved_request is None:
        messages.error(request, "Accepted request does not exist")
        return redirect("requests")

    if approved_request.status != "P":
        messages.error(request, "Request can only be accepted if pending")
        return redirect("requests")


    if approved_request.sender != user:
        messages.error(request, "Sender mismatch")
        return redirect("requests")


    result: TransferResult = apply_request(approved_request)


    if result == TransferResult.InsufficientFunds:
        messages.error(request, "Failed due to insufficient funds.")
        return redirect("requests")


    if result == TransferResult.TransactionFailure:
        messages.error(request, "Failed due to server error. Try again later.")
        return redirect("requests")

    if approved_request.sender != request.user:
        messages.error(request, "Sender mismatch")
        return redirect("requests")

    return redirect("requests")



@login_required
def deny_request(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    user = request.user
    request_id = request.POST.get("request_id")

    approved_request: Request | None = Request.objects.filter(id=request_id).first()


    if approved_request is None:
        messages.error(request, "Accepted request does not exist")
        return redirect("requests")

    if approved_request.status != "P":
        messages.error(request, "Request can only be denied if pending")
        return redirect("requests")

    if approved_request.sender != request.user:
        messages.error(request, "Sender mismatch")
        return redirect("requests")


    try:
        with transaction.atomic():
            approved_request.status = "D"
            approved_request.save()

    except Exception as e:
        print(e)
        messages.error(request, "Failed to deny request due to transaction error")



    return redirect("requests")




@login_required
def view_notifications(request):
    account = request.user

    notifcations = Notification.objects.filter( Q(user=account)  ).order_by("-date")

    return render(request, "payapp/notifications.html", { 'notifications': notifcations } )



@login_required
def mark_read(request):
    if request.method != "POST":
        return HttpResponseForbidden()


    notification_id = request.POST.get("notification_id")

    
    notification = Notification.objects.filter(id=notification_id).first()

    if notification is None:
        messages.error(request, "Notification not found")
        return redirect("notifications")

    if notification.status == "R":
        return redirect("notifications")



    notification.status = "R"

    try:
        with transaction.atomic():
            notification.save()

    except Exception as e:
        print(e)
        messages.error(request, "Failed to mark notificaition as read")



    return redirect("notifications")




@login_required
def mark_unread(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    notification_id = request.POST.get("notification_id")

    
    notification = Notification.objects.filter(id=notification_id).first()

    if notification is None:
        messages.error(request, "Notification not found")
        return redirect("notifications")

    if notification.status == "U":
        return redirect("notifications")



    notification.status = "U"

    try:
        with transaction.atomic():
            notification.save()

    except Exception as e:
        print(e)
        messages.error(request, "Failed to mark notificaition as read")



    return redirect("notifications")


@login_required
def delete_notifications(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    notification_id = request.POST.get("notification_id")

    
    notification = Notification.objects.filter(id=notification_id).first()

    if notification is None:
        messages.error(request, "Notification not found")
        return redirect("notifications")


    try:
        with transaction.atomic():
            notification.delete()

    except Exception as e:
        print(e)
        messages.error(request, "Failed to delete notificaition")



    return redirect("notifications")


def unread_notifications(request):
    if not request.user.is_authenticated:
        return {}

    count = Notification.objects.filter(user=request.user, status="U").count()
    if count < 1:
        return {}

    return {"unread_notifications": count}

